"""
Planning Enforcer Middleware for Deep Agent
Ensures all queries have an execution plan before code execution.
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Optional
from langchain_core.tools import tool
from langchain.agents.middleware import AgentMiddleware


class PlanningEnforcerMiddleware(AgentMiddleware):
    """
    Middleware that enforces planning before code execution.
    Provides tools for creating and tracking execution plans.
    """
    
    def __init__(self, plans_dir: str = "./sandbox/plans"):
        self.plans_dir = Path(plans_dir)
        self.plans_dir.mkdir(parents=True, exist_ok=True)
        self._current_plan = None
        self._current_query_id = None
    
    def create_execution_plan(
        self, 
        query_id: str,
        query_text: str,
        steps: list,
        ifc_model: str,
        entity_types: list
    ) -> str:
        """
        MANDATORY: Create an execution plan before running any code.
        This MUST be called before executing any shell commands.
        
        Args:
            query_id: Unique identifier for the query (e.g., ARQ_E01, ARQ_H02)
            query_text: The natural language query being answered
            steps: List of planned steps to execute (strings)
            ifc_model: Target IFC model file (e.g., ARQ.ifc)
            entity_types: IFC entity types to query (e.g., ["IfcWall"])
        
        Returns:
            Confirmation message with plan path
        """
        plan = {
            "query_id": query_id,
            "query_text": query_text,
            "steps": [{"step": s, "status": "pending"} for s in steps],
            "ifc_model": ifc_model,
            "entity_types": entity_types,
            "scripts": [],
            "created_at": datetime.now().isoformat(),
            "completed_at": None
        }
        
        plan_path = self.plans_dir / f"{query_id}.json"
        with open(plan_path, "w", encoding="utf-8") as f:
            json.dump(plan, f, indent=2, ensure_ascii=False)
        
        self._current_plan = plan
        self._current_query_id = query_id
        
        return f"✅ Execution plan created: {plan_path}\nPlan has {len(steps)} steps. You may now proceed with code execution."
    
    def mark_step_complete(
        self, 
        step_index: int, 
        script_path: Optional[str] = None
    ) -> str:
        """
        Mark a plan step as complete and optionally track the script used.
        
        Args:
            step_index: Zero-based index of the step to mark complete
            script_path: Optional path to the Python script used for this step
        
        Returns:
            Confirmation message
        """
        if not self._current_plan:
            return "❌ No active plan. Create one using create_execution_plan first."
        
        if step_index < 0 or step_index >= len(self._current_plan["steps"]):
            return f"❌ Invalid step index. Valid range: 0-{len(self._current_plan['steps'])-1}"
        
        self._current_plan["steps"][step_index]["status"] = "complete"
        self._current_plan["steps"][step_index]["completed_at"] = datetime.now().isoformat()
        
        if script_path:
            if script_path not in self._current_plan["scripts"]:
                self._current_plan["scripts"].append(script_path)
        
        self._save_current_plan()
        
        remaining = sum(1 for s in self._current_plan["steps"] if s["status"] == "pending")
        return f"✅ Step {step_index} marked complete. {remaining} steps remaining."
    
    def complete_plan(self) -> str:
        """
        Mark the entire plan as complete.
        Call this after all steps are done and the answer is ready.
        
        Returns:
            Confirmation with summary
        """
        if not self._current_plan:
            return "❌ No active plan to complete."
        
        self._current_plan["completed_at"] = datetime.now().isoformat()
        
        # Mark any remaining steps as complete
        for step in self._current_plan["steps"]:
            if step["status"] == "pending":
                step["status"] = "complete"
        
        self._save_current_plan()
        
        scripts_count = len(self._current_plan["scripts"])
        steps_count = len(self._current_plan["steps"])
        
        result = f"✅ Plan {self._current_query_id} completed!\n"
        result += f"   Steps: {steps_count}\n"
        result += f"   Scripts tracked: {scripts_count}"
        
        return result
    
    def _save_current_plan(self):
        """Save the current plan to disk."""
        if self._current_plan and self._current_query_id:
            plan_path = self.plans_dir / f"{self._current_query_id}.json"
            with open(plan_path, "w", encoding="utf-8") as f:
                json.dump(self._current_plan, f, indent=2, ensure_ascii=False)
    
    @property
    def tools(self):
        """Return the middleware tools."""
        # Convert methods to langchain tools
        from langchain_core.tools import StructuredTool
        
        return [
            StructuredTool.from_function(
                func=self.create_execution_plan,
                name="create_execution_plan",
                description=self.create_execution_plan.__doc__
            ),
            StructuredTool.from_function(
                func=self.mark_step_complete,
                name="mark_step_complete", 
                description=self.mark_step_complete.__doc__
            ),
            StructuredTool.from_function(
                func=self.complete_plan,
                name="complete_plan",
                description=self.complete_plan.__doc__
            )
        ]


# Standalone tool functions for direct use
def create_planning_tools(plans_dir: str = "./sandbox/plans"):
    """Create planning tools with a specific plans directory."""
    middleware = PlanningEnforcerMiddleware(plans_dir)
    return middleware.tools
