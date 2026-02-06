"""
Skill Builder - Extracts reusable functions from successful queries.

This module analyzes Python scripts from successful benchmark queries,
extracts modular functions with docstrings, and saves them as learned skills.
"""

import os
import ast
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Optional

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

# Prompt for LLM code reviewer
CODE_REVIEWER_PROMPT = """You are a code reviewer specialized in code generalization.

Analyze this Python function and generalize it by converting hardcoded values to parameters.

RULES:
1. If an IFC entity type is hardcoded (like 'IfcWall', 'IfcDoor'), make it a parameter with a default value
2. Rename the function to reflect the generic behavior (e.g., count_walls -> count_entities)
3. Update the docstring to reflect the new parameter
4. Return ONLY the refactored function code, nothing else - no explanations, no markdown
5. If no generalization is possible, return the original code unchanged

FUNCTION TO REVIEW:
{code}
"""

# Prompt for LLM reuse detector
REUSE_DETECTOR_PROMPT = """You detect if a function duplicates existing skill functionality.

EXISTING SKILLS in same category:
{skills_summary}

GENERATED FUNCTION:
{generated_function}

RULES:
1. If the function does the same thing as an existing skill, it's a duplicate
2. A generic skill (count_entities) can replace a specific function (count_doors)
3. Return ONLY a JSON object, no explanations

RESPONSE:
If duplicate: {{"match": true, "skill_name": "X", "skill_path": "skills/learned/category/scripts/X.py"}}
If not duplicate: {{"match": false}}
"""


class SkillBuilder:
    """Extracts and saves reusable functions from successful queries."""
    
    def __init__(self, skills_dir: str = "./skills/learned", model_key: str = None):
        self.skills_dir = Path(skills_dir)
        self.skills_dir.mkdir(parents=True, exist_ok=True)
        self.model_key = model_key
        
        # Initialize LLM reviewer using get_model() from main.py
        # This ensures consistent model configuration across the application
        if model_key:
            try:
                # Import get_model dynamically to avoid circular imports
                from main import get_model
                self.reviewer = get_model(model_key)
                print(f"    🔧 SkillBuilder initialized with {model_key}")
            except Exception as e:
                print(f"    ⚠️  Could not initialize model {model_key}: {e}")
                # Fallback to default Haiku via OpenRouter
                self.reviewer = ChatOpenAI(
                    model="anthropic/claude-haiku-4.5",
                    openai_api_base="https://openrouter.ai/api/v1",
                    openai_api_key=os.environ.get("OPENROUTER_API_KEY", ""),
                    temperature=0,
                )
        else:
            # Fallback to Haiku if no model specified
            self.reviewer = ChatOpenAI(
                model="anthropic/claude-haiku-4.5",
                openai_api_base="https://openrouter.ai/api/v1",
                openai_api_key=os.environ.get("OPENROUTER_API_KEY", ""),
                temperature=0,
            )
        
        # Base categories for primary organization
        self.base_categories = {
            "quantities": ["count", "sum", "total", "how many", "number"],
            "properties": ["elevation", "name", "value", "attribute", "pset", "property"],
            "relationships": ["material", "relation", "association", "contained", "connected"],
            "spatial": ["storey", "floor", "building", "site", "space", "zone", "location"],
            "geometry": ["area", "volume", "bbox", "coordinate", "dimension", "shape"],
            "validation": ["check", "verify", "validate", "compliance", "conform"],
            "transformation": ["convert", "transform", "aggregate", "group", "filter"],
            "schema": ["schema", "version", "metadata", "ifc2x3", "ifc4"],
            "uncategorized": []  # Catch-all for unmatched functions
        }
        
        # Tag keywords for cross-cutting concerns (can overlap with categories)
        self.tag_keywords = {
            "element_filtering": ["filter", "select", "find", "get", "search"],
            "aggregation": ["sum", "count", "group", "collect", "aggregate"],
            "hierarchy_traversal": ["parent", "child", "contained", "decomposed"],
            "property_extraction": ["property", "pset", "attribute", "value"],
            "unit_handling": ["unit", "convert", "scale"],
            "error_handling": ["validate", "check", "verify"],
        }
    
    def process_successful_query(
        self,
        query_id: str,
        category: str,
        scripts_used: list,
        gold_standard: str,
        agent_answer: str
    ) -> dict:
        """
        Audit a successful query - verify agent created generic skills correctly.
        
        With Generic-First workflow, agent creates generics upfront.
        This method now:
        1. Checks if skills/learned/ was updated
        2. Updates SKILL.md indexes if needed
        3. Reports what was created
        
        Args:
            query_id: Query identifier (e.g., ARQ_E01)
            category: Query category (quantities, properties, etc.)
            scripts_used: List of script paths used in the query
            gold_standard: Expected answer
            agent_answer: Agent's answer
            
        Returns:
            Dict with audit results
        """
        results = {
            "query_id": query_id,
            "category": category,
            "skills_created": [],
            "scripts_analyzed": [],
            "timestamp": datetime.now().isoformat()
        }
        
        # Check if any new skills were created in learned/
        category_dir = self.skills_dir / category / "scripts"
        if category_dir.exists():
            for skill_file in category_dir.glob("*.py"):
                skill_name = skill_file.stem
                results["skills_created"].append(skill_name)
        
        # Analyze sandbox scripts for import patterns
        for script_path in scripts_used:
            script_file = Path(script_path)
            if not script_file.exists():
                continue
                
            try:
                with open(script_file, "r", encoding="utf-8") as f:
                    source = f.read()
                
                # Check if script imports from skills.learned
                if "from skills.learned" in source:
                    results.setdefault("imports_generic", []).append(str(script_path))
                else:
                    # Agent didn't follow Generic-First pattern
                    results.setdefault("missing_import", []).append(str(script_path))
                
                results["scripts_analyzed"].append(str(script_path))
                
            except Exception as e:
                results["error"] = str(e)
        
        return results
    
    
    def _extract_functions(self, source: str) -> list:
        """Extract function definitions from Python source code."""
        functions = []
        
        try:
            tree = ast.parse(source)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    func = {
                        "name": node.name,
                        "args": [arg.arg for arg in node.args.args],
                        "docstring": ast.get_docstring(node),
                        "source": ast.get_source_segment(source, node),
                        "lineno": node.lineno
                    }
                    functions.append(func)
        except SyntaxError:
            pass
        
        return functions
    
    def _is_reusable(self, func: dict) -> bool:
        """Check if a function is suitable for reuse."""
        # Must have docstring
        if not func["docstring"]:
            return False
        
        # Must have meaningful name (not main, test_, etc.)
        skip_prefixes = ["main", "test_", "_", "__"]
        if any(func["name"].startswith(p) for p in skip_prefixes):
            return False
        
        # Must have arguments (not just constants)
        if len(func["args"]) == 0:
            return False
        
        # Must have ifcopenshell usage
        if func["source"] and "ifcopenshell" not in func["source"]:
            return False
        
        return True
    
    def _generalize_function(self, func: dict) -> dict:
        """
        Use LLM to generalize a function by converting hardcoded values to parameters.
        
        Args:
            func: Function dict with name, source, docstring, args
            
        Returns:
            Updated function dict with generalized code
        """
        try:
            prompt = CODE_REVIEWER_PROMPT.format(code=func["source"])
            
            response = self.reviewer.invoke([
                SystemMessage(content="You are a code reviewer. Return only Python code, no explanations."),
                HumanMessage(content=prompt)
            ])
            
            generalized_code = response.content.strip()
            
            # Remove markdown code blocks if present
            if generalized_code.startswith("```"):
                lines = generalized_code.split("\n")
                generalized_code = "\n".join(lines[1:-1] if lines[-1] == "```" else lines[1:])
            
            # Extract new function name from generalized code
            try:
                tree = ast.parse(generalized_code)
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        func["name"] = node.name
                        func["source"] = generalized_code
                        func["docstring"] = ast.get_docstring(node) or func["docstring"]
                        func["args"] = [arg.arg for arg in node.args.args]
                        print(f"    🔄 Generalized: {func['name']}")
                        break
            except SyntaxError:
                # If parsing fails, keep original
                print(f"    ⚠️ Could not parse generalized code, keeping original")
                
        except Exception as e:
            print(f"    ⚠️ Generalization failed: {e}")
        
        return func

    
    def _save_function(self, func: dict, category: str, source_query: str) -> bool:
        """Save a function to the appropriate skill category with tags."""
        # Normalize category
        category = category.lower()
        if category not in self.base_categories:
            category = self._infer_category(func["name"])
        
        # Infer tags
        tags = self._infer_tags(func)
        
        # Log if function is uncategorized
        if category == "uncategorized":
            self._log_uncategorized_function(func, source_query, tags)
        
        category_dir = self.skills_dir / category / "scripts"
        category_dir.mkdir(parents=True, exist_ok=True)
        
        # Create script file
        script_name = f"{func['name']}.py"
        script_path = category_dir / script_name
        
        # Don't overwrite existing functions
        if script_path.exists():
            return False
        
        # Create module with proper imports and header
        module_content = self._create_module(func, source_query)
        
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(module_content)
        
        # Update category index with tags
        self._update_category_index(category, func, source_query, tags)
        
        # Update main index with tags
        self._update_main_index(category, func, source_query, tags)
        
        return True
    
    def _create_module(self, func: dict, source_query: str) -> str:
        """Create a standalone Python module from a function."""
        header = f'''"""
{func['name']} - Extracted from {source_query}

{func['docstring'] or 'No description available.'}

Source Query: {source_query}
Extracted: {datetime.now().strftime('%Y-%m-%d')}
"""

import ifcopenshell
import ifcopenshell.util.element
from pathlib import Path


'''
        return header + func["source"]
    
    def _infer_category(self, func_name: str) -> str:
        """Infer category from function name."""
        name_lower = func_name.lower()
        
        for category, keywords in self.base_categories.items():
            if category == "uncategorized":
                continue
            if any(kw in name_lower for kw in keywords):
                return category
        
        return "uncategorized"  # Default for unmatched functions
    
    def _infer_tags(self, func: dict) -> list[str]:
        """
        Infer multiple tags for a function based on name, docstring, and code.
        
        Returns:
            List of tag strings (can be empty)
        """
        tags = set()
        
        # Combine name and docstring for analysis
        text = f"{func['name']} {func.get('docstring', '')}".lower()
        
        # Check against tag keywords
        for tag, keywords in self.tag_keywords.items():
            if any(kw in text for kw in keywords):
                tags.add(tag)
        
        # Add category as a tag as well (categories are also tags)
        primary_category = self._infer_category(func['name'])
        if primary_category != "uncategorized":
            tags.add(primary_category)
        
        return sorted(list(tags))
    
    def _log_uncategorized_function(self, func: dict, source_query: str, tags: list[str]):
        """Log functions that don't fit existing categories for analysis."""
        log_path = self.skills_dir / "uncategorized_log.jsonl"
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "function_name": func["name"],
            "source_query": source_query,
            "inferred_tags": tags,
            "docstring": func.get("docstring", ""),
            "args": func.get("args", [])
        }
        
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry) + "\n")
    
    def _update_category_index(self, category: str, func: dict, source_query: str, tags: list[str]):
        """Update the category's SKILL.md index with tags."""
        skill_path = self.skills_dir / category / "SKILL.md"
        
        if not skill_path.exists():
            return
        
        with open(skill_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Format tags for display
        tags_str = ", ".join(f"`{t}`" for t in tags) if tags else "—"
        
        # Find the table and add new row with tags
        table_marker = "| *(auto-populated by SkillBuilder)* |"
        new_row = f"| `{func['name']}()` | {func['name']}.py | {func['docstring'][:50] if func['docstring'] else 'N/A'}... | {tags_str} | {source_query} |"
        
        if table_marker in content:
            content = content.replace(table_marker, f"{new_row}\n{table_marker}")
        
        with open(skill_path, "w", encoding="utf-8") as f:
            f.write(content)
    
    def _update_main_index(self, category: str, func: dict, source_query: str, tags: list[str]):
        """Update the main learned/SKILL.md index with tags."""
        main_skill = self.skills_dir / "SKILL.md"
        
        if not main_skill.exists():
            return
        
        with open(main_skill, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Format tags for display
        tags_str = ", ".join(f"`{t}`" for t in tags) if tags else "—"
        
        # Find the table and add new row with tags
        table_marker = "| *(functions will be added as queries succeed)* |"
        new_row = f"| `{func['name']}()` | {category} | {func['name']}.py | {func['docstring'][:40] if func['docstring'] else 'N/A'}... | {tags_str} | {source_query} |"
        
        if table_marker in content:
            content = content.replace(table_marker, f"{new_row}\n{table_marker}")
        
        with open(main_skill, "w", encoding="utf-8") as f:
            f.write(content)

    # =========================================================================
    # REUSE ENFORCEMENT METHODS
    # =========================================================================
    
    def enforce_reuse(self, script_path: Path) -> bool:
        """
        Refactor generated script to import existing skills instead of duplicating.
        
        Args:
            script_path: Path to the generated script
            
        Returns:
            True if refactoring was applied
        """
        if not script_path.exists():
            return False
            
        with open(script_path, "r", encoding="utf-8") as f:
            source = f.read()
        
        funcs = self._extract_functions(source)
        if not funcs:
            return False
            
        refactored = False
        
        for func in funcs:
            # 1. Infer category from function name
            category = self._infer_category(func['name'])
            if category == "uncategorized":
                continue
            
            # 2. Load only skills from that category (progressive disclosure)
            skills_summary = self._load_category_skills_summary(category)
            if not skills_summary:
                continue
            
            # 3. LLM detects if this is a duplicate
            match = self._find_matching_skill_llm(func, skills_summary)
            
            # 4. Refactor if match found
            if match:
                source = self._replace_with_import(source, func, match)
                refactored = True
                print(f"    ♻️ Reuse: {func['name']} → import {match['skill_name']}")
        
        if refactored:
            with open(script_path, "w", encoding="utf-8") as f:
                f.write(source)
        
        return refactored
    
    def _load_category_skills_summary(self, category: str) -> str:
        """Load compact summary of skills in a category."""
        category_dir = self.skills_dir / category / "scripts"
        if not category_dir.exists():
            return ""
        
        summaries = []
        for py_file in category_dir.glob("*.py"):
            if py_file.name.startswith("__"):
                continue
            try:
                with open(py_file, "r", encoding="utf-8") as f:
                    file_source = f.read()
                funcs = self._extract_functions(file_source)
                for func in funcs:
                    args_str = ", ".join(func.get('args', []))
                    sig = f"{func['name']}({args_str})"
                    doc = (func.get('docstring') or 'No description')[:60]
                    path = f"skills/learned/{category}/scripts/{py_file.name}"
                    summaries.append(f"- {sig}: {doc}... [{path}]")
            except Exception:
                continue
        
        return "\n".join(summaries)
    
    def _find_matching_skill_llm(self, func: dict, skills_summary: str) -> Optional[dict]:
        """Use LLM to find matching skill for a function."""
        try:
            prompt = REUSE_DETECTOR_PROMPT.format(
                skills_summary=skills_summary,
                generated_function=func['source']
            )
            
            response = self.reviewer.invoke([
                SystemMessage(content="You are a code analyzer. Return only JSON."),
                HumanMessage(content=prompt)
            ])
            
            result_text = response.content.strip()
            
            # Remove markdown code blocks if present
            if result_text.startswith("```"):
                lines = result_text.split("\n")
                result_text = "\n".join(lines[1:-1] if lines[-1].startswith("```") else lines[1:])
            
            result = json.loads(result_text)
            if result.get('match'):
                return result
        except Exception as e:
            print(f"    ⚠️ Reuse detection failed: {e}")
        
        return None
    
    def _replace_with_import(self, source: str, func: dict, match: dict) -> str:
        """Replace function definition with import statement."""
        skill_name = match['skill_name']
        skill_path = match['skill_path']
        
        # Build import statement
        # skill_path: "skills/learned/quantities/scripts/count_entities.py"
        module_path = skill_path.replace("/", ".").replace(".py", "")
        import_stmt = f"from {module_path} import {skill_name}"
        
        # Remove the function definition from source
        try:
            tree = ast.parse(source)
            lines = source.split("\n")
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name == func['name']:
                    # Find start and end lines
                    start_line = node.lineno - 1  # 0-indexed
                    end_line = node.end_lineno
                    
                    # Remove function lines
                    del lines[start_line:end_line]
                    break
            
            # Rebuild source
            new_source = "\n".join(lines)
            
            # Add sys.path and import at the top (after existing imports)
            if "sys.path.append" not in new_source:
                import_block = "import sys\nsys.path.append('.')\n"
            else:
                import_block = ""
            
            if import_stmt not in new_source:
                import_block += f"{import_stmt}\n"
            
            # Insert after other imports
            if import_block:
                # Find last import line
                import_lines = [i for i, line in enumerate(new_source.split("\n")) 
                               if line.startswith("import ") or line.startswith("from ")]
                if import_lines:
                    insert_pos = max(import_lines) + 1
                else:
                    insert_pos = 0
                
                lines = new_source.split("\n")
                lines.insert(insert_pos, import_block.strip())
                new_source = "\n".join(lines)
            
            return new_source
            
        except Exception as e:
            print(f"    ⚠️ Could not refactor: {e}")
            return source


def extract_functions_from_sandbox(
    sandbox_dir: str = "./sandbox",
    results_dir: str = "./results",
    model_key: str = "claude-haiku-4.5"
) -> list:
    """
    Extract functions from all successful queries in the sandbox.
    
    Args:
        sandbox_dir: Path to sandbox directory
        results_dir: Path to results directory
        model_key: Model to analyze
        
    Returns:
        List of extraction results
    """
    builder = SkillBuilder()
    results = []
    
    results_path = Path(results_dir) / model_key
    plans_path = Path(sandbox_dir) / "plans"
    
    if not results_path.exists() or not plans_path.exists():
        return results
    
    # Load all result files
    for result_file in results_path.glob("*.json"):
        try:
            with open(result_file, "r", encoding="utf-8") as f:
                result = json.load(f)
            
            query_id = result.get("query_id")
            category = result.get("category", "quantities")
            status = result.get("status")
            
            if status != "success":
                continue
            
            # Get scripts from plan
            plan_file = plans_path / f"{query_id}.json"
            scripts = []
            
            if plan_file.exists():
                with open(plan_file, "r", encoding="utf-8") as f:
                    plan = json.load(f)
                scripts = plan.get("scripts", [])
            
            if not scripts:
                # Try to find scripts by query_id pattern
                for script in Path(sandbox_dir).glob("*.py"):
                    if query_id.lower() in script.name.lower():
                        scripts.append(str(script))
            
            if scripts:
                extraction = builder.process_successful_query(
                    query_id=query_id,
                    category=category,
                    scripts_used=scripts,
                    gold_standard=result.get("gold_standard", ""),
                    agent_answer=result.get("agent_response", "")
                )
                results.append(extraction)
                
        except Exception as e:
            print(f"Error processing {result_file}: {e}")
    
    return results


if __name__ == "__main__":
    print("Extracting functions from successful queries...")
    results = extract_functions_from_sandbox()
    
    total_functions = sum(len(r.get("functions_extracted", [])) for r in results)
    total_scripts = sum(len(r.get("scripts_analyzed", [])) for r in results)
    
    print(f"\nExtraction complete:")
    print(f"  Queries analyzed: {len(results)}")
    print(f"  Scripts analyzed: {total_scripts}")
    print(f"  Functions extracted: {total_functions}")
    
    for r in results:
        if r.get("functions_extracted"):
            print(f"\n  {r['query_id']}: {r['functions_extracted']}")
