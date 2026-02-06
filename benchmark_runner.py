#!/usr/bin/env python3
"""
Benchmark Runner for FNDE-BIM-Bench

Automates execution of 100 benchmark queries across multiple LLM backbones.
Results are saved to structured output for manual evaluation.

Usage:
    # Run all queries with a single model
    python benchmark_runner.py --model claude-3.5-sonnet
    
    # Run a single query (for testing)
    python benchmark_runner.py --model claude-haiku-4.5 --query ARQ_E01
    
    # Run questions 0-9 (first 10 questions, 0-indexed)
    python benchmark_runner.py --model claude-haiku-4.5 --start 0 --end 9
    
    # Run questions 10-19 (next batch)
    python benchmark_runner.py --model claude-haiku-4.5 --start 10 --end 19
    
    # Run all models (700 total executions)
    python benchmark_runner.py --all-models
    
    # Resume interrupted run
    python benchmark_runner.py --model claude-3.5-sonnet --resume
"""

import os
import json
import argparse
import time
from datetime import datetime
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

from main import create_my_deep_agent, run_query, MODELS
from langfuse.langchain import CallbackHandler
from skill_builder import SkillBuilder

load_dotenv()


def extract_tokens_from_response(response: dict) -> dict:
    """
    Extract token usage directly from AIMessage.usage_metadata in the response.
    
    This is the MOST RELIABLE method because tokens are captured synchronously
    from the LLM response, without depending on Langfuse eventual consistency.
    
    Args:
        response: Agent response dict containing 'messages' list
        
    Returns:
        Dict with 'totals', 'calls', and 'call_count'.
        Returns None if no usage metadata found (fallback to Langfuse needed).
    """
    if not isinstance(response, dict) or "messages" not in response:
        return None
    
    messages = response.get("messages", [])
    
    totals = {
        "input_tokens": 0,
        "output_tokens": 0,
        "reasoning_tokens": 0,
        "total_tokens": 0
    }
    calls = []
    
    for msg in messages:
        # Check for usage_metadata on AIMessage objects
        if hasattr(msg, 'usage_metadata') and msg.usage_metadata:
            usage = msg.usage_metadata
            
            # Get model info from response_metadata if available
            model_name = "unknown"
            if hasattr(msg, 'response_metadata') and msg.response_metadata:
                model_name = msg.response_metadata.get('model', 'unknown')
            
            call_data = {
                "name": "AIMessage",
                "model": model_name,
                "input_tokens": usage.get('input_tokens', 0) or 0,
                "output_tokens": usage.get('output_tokens', 0) or 0,
                "total_tokens": usage.get('total_tokens', 0) or 0,
                "reasoning_tokens": 0
            }
            
            # Extract reasoning tokens if available
            output_details = usage.get('output_token_details', {})
            if output_details:
                call_data["reasoning_tokens"] = output_details.get('reasoning', 0) or 0
            
            # Accumulate
            totals["input_tokens"] += call_data["input_tokens"]
            totals["output_tokens"] += call_data["output_tokens"]
            totals["total_tokens"] += call_data["total_tokens"]
            totals["reasoning_tokens"] += call_data["reasoning_tokens"]
            
            calls.append(call_data)
    
    if not calls:
        return {
            "totals": None,
            "calls": [],
            "call_count": 0
        }
    
    return {
        "totals": totals,
        "calls": calls,
        "call_count": len(calls)
    }


def get_token_usage(response: dict) -> dict:
    """
    Extract token usage from agent response.
    
    Extracts usage_metadata directly from AIMessage objects in the response.
    This is synchronous and 100% reliable (no eventual consistency issues).
    
    Args:
        response: Agent response dict containing 'messages' list
        
    Returns:
        Dict with 'totals', 'calls', and 'call_count'
    """
    return extract_tokens_from_response(response)

# Paths
BASE_DIR = Path(__file__).parent
BENCHMARK_FILE = BASE_DIR / "dataset" / "benchmark_dataset.json"
RESULTS_DIR = BASE_DIR / "results"
SANDBOX_DIR = BASE_DIR / "sandbox"


def load_benchmark() -> list[dict]:
    """Load benchmark dataset from JSON file."""
    with open(BENCHMARK_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def get_result_path(model_key: str, query_id: str, experiment_id: str = None) -> Path:
    """Get the path for storing a single query result."""
    # If experiment_id is provided, append it to model folder name
    folder_name = f"{model_key}-{experiment_id}" if experiment_id else model_key
    model_dir = RESULTS_DIR / folder_name
    model_dir.mkdir(parents=True, exist_ok=True)
    return model_dir / f"{query_id}.json"


def is_query_completed(model_key: str, query_id: str, experiment_id: str = None) -> bool:
    """Check if a query has already been processed."""
    return get_result_path(model_key, query_id, experiment_id).exists()


def save_result(model_key: str, query_id: str, result: dict, experiment_id: str = None) -> None:
    """Save query result to JSON file."""
    path = get_result_path(model_key, query_id, experiment_id)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"  Saved: {path}")


def get_sandbox_scripts(query_id: str) -> list[str]:
    """Get all Python scripts in sandbox that might be related to this query."""
    if not SANDBOX_DIR.exists():
        return []
    
    scripts = []
    for script in SANDBOX_DIR.glob("*.py"):
        # Get recent scripts (modified in last 5 minutes)
        if script.stat().st_mtime > time.time() - 300:
            scripts.append(str(script))
    return scripts


def detect_dataset_access(response_content: str, full_response: dict) -> bool:
    """
    Detect if the agent attempted to access the benchmark dataset file.
    
    Args:
        response_content: Extracted text response from agent
        full_response: Full response dict from agent
    
    Returns:
        True if suspicious dataset access patterns detected, False otherwise
    """
    suspicious_patterns = [
        "benchmark_dataset.json",
        "dataset/benchmark",
        "gold_standard",
        "is_impossible",
        # Commands that might read the dataset
        "cat dataset/",
        "grep dataset/",
        "open('dataset/benchmark",
        'open("dataset/benchmark',
        "json.load",  # Combined with dataset mentions
    ]
    
    # Convert entire response to string for comprehensive check
    full_text = str(full_response).lower()
    response_lower = response_content.lower()
    
    # Check for suspicious patterns
    for pattern in suspicious_patterns:
        if pattern.lower() in response_lower or pattern.lower() in full_text:
            return True
    
    return False


def extract_response_content(response: dict, query_id: str = "") -> str:
    """Extract the final answer from agent response."""
    try:
        # DEBUG: Print response structure
        print(f"\n[DEBUG] Response type: {type(response)}")
        print(f"[DEBUG] Response keys: {response.keys() if isinstance(response, dict) else 'N/A'}")
        if isinstance(response, dict) and "messages" in response:
            print(f"[DEBUG] Number of messages: {len(response['messages'])}")
            for i, msg in enumerate(response["messages"][-3:]):  # Last 3 messages
                print(f"[DEBUG] msg[{i}] type: {type(msg).__name__}, hasattr content: {hasattr(msg, 'content')}")
                if hasattr(msg, 'content'):
                    print(f"[DEBUG] msg[{i}].content (first 200 chars): {str(msg.content)[:200]}")
                if hasattr(msg, 'type'):
                    print(f"[DEBUG] msg[{i}].type: {msg.type}")
        
        # Response structure varies by agent, try common patterns
        if isinstance(response, dict):
            if "messages" in response:
                # Get last AI message - iterate in reverse
                for msg in reversed(response["messages"]):
                    # LangChain message objects (AIMessage, HumanMessage, etc.)
                    if hasattr(msg, "content"):
                        msg_type = type(msg).__name__
                        # Accept AIMessage or any message type ending with 'Message'
                        if msg_type == "AIMessage" or (hasattr(msg, "type") and msg.type == "ai"):
                            # Try content first, then text attribute as fallback
                            content = msg.content if msg.content else (msg.text if hasattr(msg, "text") else "")
                            return content
                    # Dict-style messages
                    elif isinstance(msg, dict):
                        if msg.get("role") == "assistant" or msg.get("type") == "ai":
                            return msg.get("content", "")
            if "output" in response:
                return response["output"]
            if "content" in response:
                return response["content"]
        return str(response)
    except Exception as e:
        return f"ERROR extracting response: {e}"


def run_benchmark_query(
    agent, 
    backend,
    query_data: dict, 
    model_key: str,
    langfuse_handler: Optional[CallbackHandler] = None
) -> dict:
    """
    Run a single benchmark query and return structured result.
    
    Args:
        agent: The deep agent instance
        backend: SkillTrackingBackend instance for tracking skill access
        query_data: Query dict from benchmark dataset
        model_key: Model identifier
        langfuse_handler: Optional Langfuse callback
    
    Returns:
        Result dict with query, response, and metadata
    """
    query_id = query_data["id"]
    question = query_data["question"]
    model_file = query_data["model"]
    
    # Set query context for skill tracking
    backend.set_query_context(query_id)
    
    # Build the full query with context
    full_query = f"""
Query ID: {query_id}
IFC Model: ./projects/fnde/{model_file}

Question: {question}

INSTRUCTIONS:
1. Create a Python script in ./sandbox/ with a FUNCTION to answer this query
2. The function MUST have a complete docstring with Args, Returns, and Example
3. Execute the script with: python3 sandbox/your_script.py
4. Report the answer based on the script output
5. Do NOT answer without executing code first
"""
    
    print(f"  Processing: {query_id} - {question[:50]}...")
    
    start_time = time.time()
    try:
        response = run_query(agent, full_query, langfuse_handler)
        response_content = extract_response_content(response, query_id)
        status = "success"
        error = None
        
        # Security check: detect dataset access attempts
        dataset_accessed = detect_dataset_access(response_content, response)
        if dataset_accessed:
            print(f"  ⚠️  WARNING: Potential dataset access detected in response!")
            
    except Exception as e:
        response_content = ""
        status = "error"
        error = str(e)
        dataset_accessed = False
        print(f"  ERROR: {e}")
    
    elapsed_time = time.time() - start_time
    
    # Extract skills accessed during this query
    skills_accessed = backend.get_skills_for_query(query_id)
    
    # Reset tracking for next query
    backend.reset_tracking()
    
    # Extract token usage directly from response (synchronous, reliable)
    token_usage = None
    if status == "success":
        print(f"    📊 Extracting token usage...")
        token_usage = get_token_usage(response)
        if token_usage and token_usage.get("totals"):
            totals = token_usage["totals"]
            print(f"    📊 Tokens: {totals['input_tokens']} in, {totals['output_tokens']} out, {totals['total_tokens']} total ({token_usage['call_count']} calls)")
    
    # Get trace_id for debugging (still useful for Langfuse UI)
    trace_id = langfuse_handler.last_trace_id if langfuse_handler else None
    
    # Extract full message content for offline analysis
    messages_log = []
    if status == "success" and isinstance(response, dict) and "messages" in response:
        for i, msg in enumerate(response["messages"]):
            msg_data = {
                "index": i,
                "type": type(msg).__name__,
                "role": getattr(msg, "type", "unknown"),
            }
            
            # Extract content
            if hasattr(msg, "content"):
                msg_data["content"] = msg.content
            elif isinstance(msg, dict):
                msg_data["content"] = msg.get("content", "")
            
            # Extract tool calls if present
            if hasattr(msg, "tool_calls") and msg.tool_calls:
                msg_data["tool_calls"] = [
                    {
                        "name": tc.get("name") if isinstance(tc, dict) else getattr(tc, "name", ""),
                        "args": tc.get("args") if isinstance(tc, dict) else getattr(tc, "args", {}),
                    }
                    for tc in msg.tool_calls
                ]
            
            messages_log.append(msg_data)
    
    return {
        "query_id": query_id,
        "question": question,
        "model_file": model_file,
        "type": query_data.get("type", ""),
        "category": query_data.get("category", ""),
        "difficulty": query_data.get("difficulty", 0),
        "gold_standard": query_data.get("gold_standard", ""),
        "is_impossible": query_data.get("is_impossible", False),
        "model_key": model_key,
        "agent_response": response_content,
        "status": status,
        "error": error,
        "dataset_access_detected": dataset_accessed,  # Security flag
        "skills_accessed": skills_accessed,  # Track which skills were consulted
        "langfuse_trace_id": trace_id,  # Langfuse trace for debugging
        "token_usage": token_usage,  # Per-call and total token breakdown
        "messages": messages_log,  # Full message content for offline analysis
        "elapsed_seconds": round(elapsed_time, 2),
        "timestamp": datetime.now().isoformat(),
    }


def run_model_benchmark(
    model_key: str, 
    queries: list[dict],
    resume: bool = True,
    single_query_id: Optional[str] = None,

    start_idx: Optional[int] = None,
    end_idx: Optional[int] = None,
    experiment_id: Optional[str] = None
) -> None:
    """
    Run benchmark for a single model across all (or selected) queries.
    
    Args:
        model_key: Model identifier from MODELS dict
        queries: List of query dicts from benchmark
        resume: Skip already completed queries
        single_query_id: If provided, run only this query

        start_idx: Start index (0-indexed, inclusive) for question range
        end_idx: End index (0-indexed, inclusive) for question range
        experiment_id: Unique ID for this experiment execution (e.g. timestamp)
    """
    print(f"\n{'='*60}")
    print(f"Running benchmark with model: {model_key}")
    if experiment_id:
        print(f"Experiment ID: {experiment_id}")
        print(f"Results path: results/{model_key}-{experiment_id}/")
    else:
        print(f"Results path: results/{model_key}/")
    print(f"{'='*60}")
    
    # Filter to single query if specified
    if single_query_id:
        queries = [q for q in queries if q["id"] == single_query_id]
        if not queries:
            print(f"Query ID '{single_query_id}' not found in benchmark!")
            return
    
    # Filter by index range if specified
    if start_idx is not None or end_idx is not None:
        original_count = len(queries)
        start = start_idx if start_idx is not None else 0
        end = (end_idx + 1) if end_idx is not None else len(queries)  # +1 because slice is exclusive
        
        if start < 0 or end > original_count or start >= end:
            print(f"Invalid range: --start {start_idx} --end {end_idx}")
            print(f"Valid range: 0 to {original_count - 1} (total: {original_count} questions)")
            return
        
        queries = queries[start:end]
        print(f"Filtered to questions {start} to {end - 1} (inclusive): {len(queries)} questions")
    
    # Initialize agent and Langfuse
    try:
        agent, backend = create_my_deep_agent(model_key)
        langfuse_handler = CallbackHandler()
    except Exception as e:
        print(f"Failed to initialize agent: {e}")
        return
    
    # Track progress
    total = len(queries)
    completed = 0
    skipped = 0
    errors = 0
    skills_extracted = 0
    
    # Initialize skill builder if needed
    skill_builder = SkillBuilder(model_key=model_key)
    
    for i, query_data in enumerate(queries, 1):
        query_id = query_data["id"]
        
        # Check for resume
        if resume and is_query_completed(model_key, query_id, experiment_id):
            print(f"[{i}/{total}] Skipping {query_id} (already completed)")
            skipped += 1
            continue
        
        print(f"\n[{i}/{total}] {query_id}")
        
        result = run_benchmark_query(agent, backend, query_data, model_key, langfuse_handler)
        save_result(model_key, query_id, result, experiment_id)
        
        if result["status"] == "success":
            completed += 1
            
            # Extract skills from sandbox scripts
            if skill_builder:
                sandbox_scripts = get_sandbox_scripts(query_id)
                if sandbox_scripts:
                    try:
                        # First: enforce reuse of existing skills
                        for script in sandbox_scripts:
                            skill_builder.enforce_reuse(Path(script))
                        
                        # Then: extract new skills from processed scripts
                        extraction = skill_builder.process_successful_query(
                            query_id=result["query_id"],
                            category=result["category"],
                            scripts_used=sandbox_scripts,
                            gold_standard=result["gold_standard"],
                            agent_answer=result["agent_response"]
                        )
                        if extraction.get("skills_created"):
                            skills_extracted += len(extraction["skills_created"])
                            print(f"    📚 Found {len(extraction['skills_created'])} skills in category")
                    except Exception as e:
                        print(f"    ⚠️  Skill extraction error: {e}")
        else:
            errors += 1
        
        # Brief pause between queries to avoid rate limiting
        if i < total:
            seconds = 30
            print(f"    ⏳ Cooling down for {seconds}s to manage TPM limit...")
            time.sleep(seconds)
    
    # Summary
    print(f"\n{'='*60}")
    print(f"Model {model_key} - Summary:")
    print(f"  Total queries: {total}")
    print(f"  Completed: {completed}")
    print(f"  Skipped (already done): {skipped}")
    print(f"  Errors: {errors}")
    print(f"  Skills extracted: {skills_extracted}")
    print(f"{'='*60}")


def main():
    parser = argparse.ArgumentParser(
        description="FNDE-BIM-Bench Benchmark Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument(
        "--model", type=str, default=None,
        help=f"Model to use: {', '.join(MODELS.keys())}"
    )
    parser.add_argument(
        "--query", type=str, default=None,
        help="Run only this query ID (e.g., ARQ_E01)"
    )
    parser.add_argument(
        "--all-models", action="store_true",
        help="Run all models (700 total queries)"
    )
    parser.add_argument(
        "--resume", action="store_true", default=True,
        help="Skip already completed queries (default: True)"
    )
    parser.add_argument(
        "--no-resume", action="store_true",
        help="Re-run all queries even if completed"
    )
    parser.add_argument(
        "--list-models", action="store_true",
        help="List available models and exit"
    )

    parser.add_argument(
        "--start", type=int, default=None,
        help="Start index for question range (0-indexed, inclusive)"
    )
    parser.add_argument(
        "--end", type=int, default=None,
        help="End index for question range (0-indexed, inclusive)"
    )
    parser.add_argument(
        "--experiment-id", type=str, default=None,
        help="Experiment ID to append to results folder (default: autogenerated timestamp if creating new)"
    )
    
    args = parser.parse_args()
    
    if args.list_models:
        print("Available models:")
        for key, value in MODELS.items():
            print(f"  {key}: {value}")
        return
    
    # Load benchmark
    print(f"Loading benchmark from: {BENCHMARK_FILE}")
    queries = load_benchmark()
    print(f"Loaded {len(queries)} queries")
    
    resume = not args.no_resume

    
    # Determine experiment ID
    experiment_id = args.experiment_id
    if not experiment_id and not resume:
        # If not resuming and no ID provided, generate new one
        # BUT: args.resume is True by default.
        # If user wants a NEW experiment, they should use --no-resume OR provide a new ID?
        # A safer default: 
        # If ID IS provided -> Use it (could be new or existing)
        # If ID NOT provided -> Generate NEW timestamp ID to avoid overwriting default folder?
        # Wait, if we generate new ID every time, --resume won't work without explicit ID.
        # That is Acceptable behavior for reproducible experiments.
        
        # Let's generate a timestamp if no ID is passed, UNLESS user explicitly wants unrelated behavior?
        # User requested: "esse id vc vai criar por experimento" -> so YES, create it.
        experiment_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        print(f"Generated new Experiment ID: {experiment_id}")
    elif not experiment_id and resume:
         # If resuming but no ID provided, try to find the most recent experiment for this model
         model_key = args.model
         if model_key:
             existing_folders = sorted(RESULTS_DIR.glob(f"{model_key}-*"), reverse=True)
             if existing_folders:
                 # Use the most recent experiment folder
                 latest_folder = existing_folders[0]
                 experiment_id = latest_folder.name.replace(f"{model_key}-", "")
                 print(f"Resuming experiment: {experiment_id} (found {len(existing_folders)} previous runs)")
             else:
                 # No existing experiment found, start a new one
                 experiment_id = datetime.now().strftime("%Y%m%d_%H%M%S")
                 print(f"No previous experiment found. Starting NEW experiment with ID: {experiment_id}")
         else:
             experiment_id = datetime.now().strftime("%Y%m%d_%H%M%S")
             print(f"No Experiment ID provided. Starting NEW experiment with ID: {experiment_id}")
    
    if args.all_models:
        # Run all models
        for model_key in MODELS.keys():
            run_model_benchmark(
                model_key, queries, resume, 

                start_idx=args.start,
                end_idx=args.end,
                experiment_id=experiment_id
            )
    elif args.model:
        run_model_benchmark(
            args.model, queries, resume, args.query, 

            start_idx=args.start,
            end_idx=args.end,
            experiment_id=experiment_id
        )
    else:
        print("Please specify --model or --all-models")
        print(f"Available models: {', '.join(MODELS.keys())}")


if __name__ == "__main__":
    main()
 
