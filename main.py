import os
import json
import argparse
from typing import Optional
from dotenv import load_dotenv
from deepagents import create_deep_agent
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from deepagents.backends import FilesystemBackend
from skill_tracking_backend import SkillTrackingBackend
from langchain_community.tools.shell import ShellTool
from langfuse.langchain import CallbackHandler
from planning_middleware import PlanningEnforcerMiddleware
from utils.code_validator import validate_script
import re

# Global reference to fixer agent (set during agent creation)
_fixer_agent = None

def set_fixer_agent(agent):
    """Set the global fixer agent reference."""
    global _fixer_agent
    _fixer_agent = agent

def extract_code_from_response(response) -> str:
    """Extract Python code from LLM response, handling markdown blocks."""
    # Handle dict with 'content' key (from FixerAgent)
    if isinstance(response, dict) and 'content' in response:
        text = response['content']
    elif hasattr(response, 'content'):
        text = response.content
    elif isinstance(response, dict) and 'messages' in response:
        messages = response.get('messages', [])
        for msg in reversed(messages):
            if hasattr(msg, 'content') and msg.content:
                text = msg.content
                break
        else:
            text = str(response)
    else:
        text = str(response)
    
    # Try to extract from markdown code block
    match = re.search(r'```(?:python)?\s*\n?(.*?)\n?```', text, re.DOTALL)
    if match:
        return match.group(1).strip()
    
    # If no code block, return as-is (assuming it's raw code)
    return text.strip()

class ValidatedShellTool(ShellTool):
    """
    Enhanced ShellTool that validates Python scripts before execution using AST.
    If validation fails, calls code-fixer subagent to auto-correct.
    """
    MAX_FIX_ATTEMPTS: int = 2  # ClassVar annotation for Pydantic compatibility
    
    def _run(self, commands: str | list[str]) -> str:
        """Run commands with pre-validation and auto-fix."""
        if isinstance(commands, str):
            cmds = [commands]
        else:
            cmds = commands

        # Process commands to add PYTHONPATH for Python scripts
        processed_cmds = []
        for cmd in cmds:
            # Detect Python execution in any part of command (handles cd ... && python3 ...)
            import re
            python_match = re.search(r'(python3?)\s+(\S+\.py)', cmd)
            
            if python_match:
                script_path = python_match.group(2)
                # Handle relative paths - strip ./ prefix if present
                if script_path.startswith('./'):
                    script_path = script_path[2:]
                
                # AST Validation (only if file exists)
                import os
                if os.path.exists(script_path):
                    is_valid, error = validate_script(script_path)
                    
                    if not is_valid:
                        # Try to auto-fix using subagent
                        fixed = self._try_auto_fix(script_path, error)
                        if not fixed:
                            return f"⛔ CODE INTEGRITY ERROR (Execution Blocked):\n{error}\n\nAuto-fix failed. You MUST manually fix the script."
                
                # Add PYTHONPATH=. at the START of the command
                cmd = f"PYTHONPATH=. {cmd}"
            
            processed_cmds.append(cmd)

        return super()._run(processed_cmds)
    
    def _try_auto_fix(self, script_path: str, error: str) -> bool:
        """Attempt to fix the script using the code-fixer subagent."""
        global _fixer_agent
        
        if not _fixer_agent:
            print("⚠️  No fixer agent configured, cannot auto-fix")
            return False
        
        try:
            with open(script_path, 'r') as f:
                broken_code = f.read()
        except Exception as e:
            print(f"⚠️  Could not read script: {e}")
            return False
        
        for attempt in range(self.MAX_FIX_ATTEMPTS):
            print(f"🔧 Auto-fix attempt {attempt + 1}/{self.MAX_FIX_ATTEMPTS} for {script_path}")
            
            # Call fixer agent
            fix_prompt = f"""Fix this Python script:

ERROR: {error}

BROKEN CODE:
```python
{broken_code}
```

Return ONLY the corrected Python code, no explanations."""
            
            try:
                response = _fixer_agent.invoke({
                    "messages": [{"role": "user", "content": fix_prompt}]
                })
                fixed_code = extract_code_from_response(response)
                
                # Save fixed code
                with open(script_path, 'w') as f:
                    f.write(fixed_code)
                
                # Re-validate
                is_valid, new_error = validate_script(script_path)
                if is_valid:
                    print(f"✅ Script fixed successfully!")
                    return True
                else:
                    print(f"⚠️  Fix attempt {attempt + 1} failed: {new_error}")
                    error = new_error
                    broken_code = fixed_code
                    
            except Exception as e:
                print(f"⚠️  Fixer agent error: {e}")
                return False
        
        print(f"❌ Could not fix script after {self.MAX_FIX_ATTEMPTS} attempts")
        return False

# Load API keys from .env file
load_dotenv()

# ============================================================================
# LLM Models Configuration (OpenAI, OpenRouter, Ollama)
# ============================================================================
MODELS = {
    # OpenAI Direct API
    "gpt-4o-openai": {"provider": "openai", "model": "gpt-4o"},
    "gpt-5-mini-openai": {"provider": "openai", "model": "gpt-5-mini"},
    "gpt-4-turbo": {"provider": "openai", "model": "gpt-4-turbo"},
    "o1-preview": {"provider": "openai", "model": "o1-preview"},
    "o1-mini": {"provider": "openai", "model": "o1-mini"},
    
    # OpenRouter Models
    "gemini-2.5-pro-high": {"provider": "openrouter", "model": "google/gemini-2.5-pro-preview-05-06"},
    "gemini-2.5-pro-low": {"provider": "openrouter", "model": "google/gemini-2.5-pro-preview-05-06"},
    "gemini-2.5-flash": {"provider": "openrouter", "model": "google/gemini-2.5-flash-preview-05-20"},
    "claude-3.5-sonnet": {"provider": "openrouter", "model": "anthropic/claude-sonnet-4-20250514"},
    "claude-3.5-sonnet-thinking": {"provider": "openrouter", "model": "anthropic/claude-sonnet-4-20250514"},
    "claude-3.5-opus-thinking": {"provider": "openrouter", "model": "anthropic/claude-opus-4-20250514"},
    "gpt-4o": {"provider": "openrouter", "model": "openai/gpt-4o"},
    "claude-haiku-4.5": {"provider": "openrouter", "model": "anthropic/claude-haiku-4.5"},
    "claude-sonnet-4.5": {"provider": "openrouter", "model": "anthropic/claude-sonnet-4.5"},
    "qwen3-coder-30b-a3b-instruct": {"provider": "openrouter", "model": "qwen/qwen3-coder-30b-a3b-instruct"},
    "gpt-oss-120b": {"provider": "openrouter", "model": "openai/gpt-oss-120b"},
    "ministral-14b-2512": {"provider": "openrouter", "model": "mistralai/ministral-14b-2512"},
    "qwen3-coder-flash": {"provider": "openrouter", "model": "qwen/qwen3-coder-flash"},
    "gpt-oss-20b": {"provider": "openrouter", "model": "openai/gpt-oss-20b"},
    "gpt-5-nano": {"provider": "openrouter", "model": "openai/gpt-5-nano"},
    "gpt-5-mini": {"provider": "openrouter", "model": "openai/gpt-5-mini"},
    
    # Ollama Local Models
    "deepseek-r1:8b": {"provider": "ollama", "model": "deepseek-r1:8b"},
    "qwen3:4b-instruct": {"provider": "ollama", "model": "qwen3:4b-instruct"},
    "qwen3:4b": {"provider": "ollama", "model": "qwen3:4b"},
    "qwen2.5:3b": {"provider": "ollama", "model": "qwen2.5:3b"},
    "llama3.2:3b": {"provider": "ollama", "model": "llama3.2:3b"},
    "gemma3:4b": {"provider": "ollama", "model": "gemma3:4b"},
}

# ============================================================================
# Code Reviewer SubAgent - Reviews code for generalization opportunities
# ============================================================================
CODE_REVIEWER_PROMPT = """
You are a code reviewer for generalization opportunities.

**Task:** If a value is HARDCODED, suggest making it a PARAMETER.

**Input example:** count_doors function with hardcoded 'IfcDoor'
**Output example:** count_entities function with entity_type parameter

If no changes needed: "NO_CHANGES_NEEDED: [reason]"
"""

# ============================================================================
# Code Fixer SubAgent - Fixes scripts that fail AST validation
# ============================================================================
CODE_FIXER_PROMPT = """
You are a Python code fixer. You receive a script that failed validation.

Your task: Return ONLY the corrected Python code. No explanations.

Common errors and fixes:
1. Function called but not defined → Define the function in the script
2. Function called but not imported → Add the import OR define locally

Rules:
- Preserve the original docstring and purpose
- Keep the same filename convention
- Return ONLY valid Python code, no markdown, no explanations
- The fixed code must be complete and runnable
"""

INSTRUCTIONS = """
You are a BIM expert specialized in IFC information retrieval.

## EXECUTION ENVIRONMENT
- Current directory: {base_dir}
- You are ALREADY in the ifc-coding-agent directory
- For read_file: Use RELATIVE paths (e.g., skills/..., sandbox/...)
- For write_file: Use ABSOLUTE paths starting with {base_dir} (e.g., {base_dir}/sandbox/...)
- Scripts: ./sandbox/

## MANDATORY PLANNING PHASE
Before executing ANY code, you MUST:
1. Use `create_execution_plan` tool with: query_id, IFC model, entity types, step descriptions
2. Use `mark_step_complete` after each step
3. Use `complete_plan` when finished

## CRITICAL RULES (NON-NEGOTIABLE)

### 1. Function Structure
EVERY script MUST contain reusable function(s) with complete docstring.

Example - count_entities function:
- Purpose: Count entities of specified type in IFC model
- Args: ifc_path (str), entity_type (str like "IfcWall")
- Returns: int (total count)
- Implementation: Open IFC file, query by type, return count

### 2. Import-Call Consistency (CRITICAL)
**Rule:** Every function you CALL must be IMPORTED or DEFINED in the same file.

Import ONLY ONE function from ONE path. Call that SAME function.

CORRECT example:
  from skills.learned.quantities.scripts.count_entities import count_entities
  result = count_entities('./model.ifc', 'IfcWall')

WRONG example:
  from skills.learned.quantities.scripts.count_entities import count_entities
  result = count_walls('./model.ifc')  # count_walls never imported/defined!

### 3. Skill Reading Strategy

BEFORE writing ANY code, check available skills:

**STEP 1: Read the skill index (SKILL.md is small, ~80 lines)**
```
read_file("skills/ifcopenshell-filtering/SKILL.md")
```
This shows the Function Index table with links to example scripts.

**STEP 2: Read the specific script you need**
Based on the Function Index, read only the relevant script:
```
read_file("skills/ifcopenshell-filtering/scripts/filter_by_class.py")
```

**Available IfcOpenShell skills:**
- `skills/ifcopenshell-filtering/` → Filter elements (class, material, type, location, properties)
- `skills/ifcopenshell-extracting/` → Extract values (coordinates, attributes, properties)
- `skills/ifcopenshell-formatting/` → Format values (text, numbers, measures)
- `skills/ifcopenshell-schema/` → Schema introspection and pset templates
- `skills/ifcopenshell-geometry/` → Vertices, faces, meshes, glTF export
- `skills/ifcopenshell-discovery/` → **LAST RESORT**: Discover actual IFC naming conventions (materials, types, Psets) when zero-result queries suggest terminology mismatches. Use only after standard filtering fails.

Each skill has:
- `SKILL.md` → Function index + reference tables (read first)
- `scripts/` → Individual example files (read only what you need)

**STEP 3: Check learned skills for reusable functions**
```
read_file("skills/learned/SKILL.md")
```

### 4. Generic-First Creation

When you need a function that doesn't exist in learned skills:

**RULE: Always create GENERIC functions first, then use them**

**STEP 1: Create the generic skill in `skills/learned/`**
```python
# File: skills/learned/quantities/scripts/count_entities.py
def count_entities(params) -> int:
    # Count entities of specified type in IFC model.
    # ... implementation here ...
    return ...
```

**STEP 2: Create your query script in `sandbox/` importing the generic**
```python
# File: sandbox/count_walls_arq_e01.py
from skills.learned.quantities.scripts.count_entities import count_entities

def count_walls(params) -> int:
    # Count walls in IFC model using generic count_entities.
    return count_entities(params)

if __name__ == "__main__":
    print(count_walls("./projects/fnde/ARQ.ifc"))
```

**Categories for learned skills:**
- `quantities/` → count, sum, aggregate functions
- `properties/` → extract property sets, attributes
- `relationships/` → spatial containment, connections
- `spatial/` → storey, building, site queries
- `geometry/` → volumes, areas, coordinates
- `validation/` → check, verify, validate
- `transformation/` → convert, modify, filter

### 5. Response Format
Your response MUST include:
- Script output (the printed result)
- Final answer based on output

DO NOT include full source code in your response. Show output only.


## Execution
1. Create generic skill in ./skills/learned/{{category}}/scripts/ if needed
2. Create query script in ./sandbox/ that imports the generic
3. Execute with: `python3 sandbox/script_name.py`
4. Use type hints for all parameters and return values
5. Respond in English
"""


def get_ollama_model(model_name: str) -> ChatOllama:
    """
    Returns a ChatOllama instance for local models.
    
    Args:
        model_name: Ollama model name (e.g., 'deepseek-r1:8b', 'qwen3:4b-instruct')
    
    Returns:
        Configured ChatOllama instance
    
    Raises:
        ConnectionError: If Ollama server is not running
    """
    ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    
    print(f"🦙 Using Ollama model: {model_name}")
    print(f"   Server: {ollama_base_url}")
    
    try:
        return ChatOllama(
            model=model_name,
            base_url=ollama_base_url,
            temperature=0,  # Deterministic for reproducibility
        )
    except Exception as e:
        raise ConnectionError(
            f"Failed to connect to Ollama server at {ollama_base_url}. "
            f"Make sure Ollama is running with: ollama serve"
        ) from e


def get_model(model_key: str = "claude-haiku-4.5"):
    """
    Returns a configured LLM instance (OpenAI, OpenRouter, or Ollama).
    
    Args:
        model_key: Key from MODELS dict (e.g., 'gpt-4o-openai', 'claude-haiku-4.5', 'deepseek-r1:8b')
    
    Returns:
        ChatOpenAI or ChatOllama instance
    
    Raises:
        ValueError: If model_key is unknown or required credentials missing
    """
    if model_key not in MODELS:
        available = ", ".join(MODELS.keys())
        raise ValueError(f"Unknown model '{model_key}'. Available: {available}")
    
    config = MODELS[model_key]
    provider = config["provider"]
    model_name = config["model"]
    
    if provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment")
        
        print(f"🤖 Using OpenAI Direct: {model_key} ({model_name})")
        
        return ChatOpenAI(
            model=model_name,
            openai_api_key=api_key,
            temperature=0,
        )
    
    elif provider == "openrouter":
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY not found in environment")
        
        print(f"☁️  Using OpenRouter: {model_key} ({model_name})")
        
        return ChatOpenAI(
            model=model_name,
            openai_api_key=api_key,
            openai_api_base="https://openrouter.ai/api/v1",
            temperature=0,
        )
    
    elif provider == "ollama":
        return get_ollama_model(model_name)
    
    else:
        raise ValueError(f"Unknown provider: {provider}")


def create_my_deep_agent(model_key: str = "claude-haiku-4.5"):
    """
    Creates and configures the deep agent with specified LLM backbone.
    
    Args:
        model_key: Key from MODELS dict
    
    Returns:
        Tuple of (agent, backend) where backend allows skill tracking
    """
    print(f"Initializing Deep Agent with {model_key}...")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(base_dir)
    
    model = get_model(model_key)
    reviewer_model = get_model(model_key)  # Use same model for code review
    fixer_model = get_model(model_key)  # Use same model for code fixing
    shell_tool = ValidatedShellTool()  # Use validating shell
    planning_middleware = PlanningEnforcerMiddleware(plans_dir=os.path.join(base_dir, "sandbox/plans"))
    
    # Create simple fixer agent (just model + system prompt)
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import StrOutputParser
    
    fixer_prompt = ChatPromptTemplate.from_messages([
        ("system", CODE_FIXER_PROMPT),
        ("user", "{input}")
    ])
    fixer_chain = fixer_prompt | fixer_model | StrOutputParser()
    
    # Wrap in a simple invocable object
    class FixerAgent:
        def __init__(self, chain):
            self.chain = chain
        def invoke(self, data):
            user_msg = data.get("messages", [{}])[0].get("content", "")
            result = self.chain.invoke({"input": user_msg})
            return {"content": result}
    
    fixer_agent = FixerAgent(fixer_chain)
    set_fixer_agent(fixer_agent)
    print("🔧 Code-fixer agent configured for auto-correction")
    
    # Use SkillTrackingBackend to automatically track skill access
    backend = SkillTrackingBackend(
        root_dir=base_dir,
        log_file=os.path.join(base_dir, "sandbox/skills_accessed.jsonl")
    )
    
    # Create code reviewer subagent with LangChain model instance
    code_reviewer_subagent = {
        "name": "code-reviewer",
        "description": "Reviews Python code for generalization opportunities. Call after creating any new function to check if hardcoded values should become parameters.",
        "system_prompt": CODE_REVIEWER_PROMPT,
        "tools": [],
        "model": reviewer_model,
    }
    
    agent = create_deep_agent(
        model=model,
        skills=["/skills"],
        tools=[shell_tool] + planning_middleware.tools,
        backend=backend,
        memory=[os.path.join(base_dir, "AGENTS.md")],
        system_prompt=INSTRUCTIONS.format(base_dir=base_dir),
        subagents=[code_reviewer_subagent],  # Code review for generalization
    )

    print(f"Agent ready! Working directory: {base_dir}")
    return agent, backend


def run_query(agent, query: str, langfuse_handler: Optional[CallbackHandler] = None) -> dict:
    """
    Runs a single query through the agent.
    
    Args:
        agent: The deep agent instance
        query: Natural language query
        langfuse_handler: Optional Langfuse callback for tracing
    
    Returns:
        Response dict from the agent
    """
    config = {}
    if langfuse_handler:
        config["callbacks"] = [langfuse_handler]
    
    response = agent.invoke(
        {"messages": [{"role": "user", "content": query}]},
        config=config
    )
    return response


def main():
    """Main entry point for testing the agent."""
    parser = argparse.ArgumentParser(description="Deep Agent for BIM Information Retrieval")
    parser.add_argument("--model", type=str, default="claude-haiku-4.5", 
                        help=f"Model to use: {', '.join(MODELS.keys())}")
    parser.add_argument("--query", type=str, default=None,
                        help="Query to run (interactive mode if not provided)")
    args = parser.parse_args()
    
    try:
        agent, backend = create_my_deep_agent(args.model)
        langfuse_handler = CallbackHandler()
        
        if args.query:
            # Single query mode
            response = run_query(agent, args.query, langfuse_handler)
            print("\n=== Response ===")
            print(response)
        else:
            # Interactive mode
            print("\nInteractive mode. Type 'exit' to quit.")
            while True:
                query = input("\nQuery: ").strip()
                if query.lower() == 'exit':
                    break
                if query:
                    response = run_query(agent, query, langfuse_handler)
                    print("\n=== Response ===")
                    print(response)
                    
    except Exception as e:
        print(f"Error: {e}")
        raise


if __name__ == "__main__":
    main()
