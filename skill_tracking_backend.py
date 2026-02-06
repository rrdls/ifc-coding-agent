"""
Skill Tracking Backend for Deep Agent
Wraps FilesystemBackend to automatically track when skills are accessed by the agent.
"""

from deepagents.backends import FilesystemBackend
from datetime import datetime
from pathlib import Path
import json
from typing import List, Optional


class SkillTrackingBackend(FilesystemBackend):
    """
    FilesystemBackend wrapper that automatically tracks
    when skills (.md files in /skills/) are accessed by the agent.
    
    Records each access in memory and in a JSONL file for later analysis.
    """
    
    def __init__(self, root_dir: str, log_file: str = "./sandbox/skills_accessed.jsonl"):
        """
        Initialize the backend with skill tracking.
        
        Args:
            root_dir: Root directory for the filesystem backend
            log_file: Path to the JSONL log file
        """
        super().__init__(root_dir=root_dir)
        self._root_dir = root_dir  # Store for path normalization
        self.log_file = Path(log_file)
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        self._skills_accessed = []
        self._current_query_id = None
    
    def set_query_context(self, query_id: str):
        """
        Set the current query context for tracking.
        
        Args:
            query_id: Unique query identifier (e.g., ARQ_M04)
        """
        self._current_query_id = query_id
    
    def _normalize_path(self, file_path: str) -> str:
        """
        Normalize file paths to ensure FilesystemBackend compatibility.
        
        Converts relative paths to absolute, resolving them relative to root_dir.
        Also handles paths that appear absolute (start with /) but are actually
        relative to root_dir (e.g., /skills/... -> root_dir/skills/...).
        
        Args:
            file_path: Original path (can be relative or absolute)
            
        Returns:
            Normalized path (absolute)
        """
        path = Path(file_path)
        root = Path(self._root_dir)
        
        # If absolute AND (exists OR starts with root_dir), return as is
        if path.is_absolute():
            if path.exists() or str(path).startswith(str(root)):
                return file_path
        
        # If starts with / but is not a real path, treat as relative (remove leading /)
        if file_path.startswith('/'):
            file_path = file_path.lstrip('/')
        
        # Resolve based on root_dir
        normalized = root / file_path
        return str(normalized)
    
    def read(self, file_path: str, offset: int = 0, limit: int = 2000) -> str:
        """
        Intercept file reads and track skill accesses.
        
        Args:
            file_path: Path to the file to read (relative or absolute)
            offset: Starting line (0-indexed)
            limit: Maximum number of lines to read
        
        Returns:
            File content
        """
        # Normalize path to ensure compatibility
        normalized_path = self._normalize_path(file_path)
        
        if self._is_skill_file(normalized_path):
            self._log_skill_access(normalized_path, offset, limit)
        
        # Call the original FilesystemBackend method with normalized path
        result = super().read(normalized_path, offset, limit)
        
        return result
    
    def write(self, file_path: str, content: str) -> str:
        """
        Intercept file writes and normalize paths.
        
        Args:
            file_path: File path (relative or absolute)
            content: Content to write
        
        Returns:
            Result of the write operation
        """
        # Normalize path to ensure compatibility
        normalized_path = self._normalize_path(file_path)
        
        # Call the original FilesystemBackend method with normalized path
        return super().write(normalized_path, content)
    
    async def aread(self, file_path: str, offset: int = 0, limit: int = 2000) -> str:
        """
        Async version of read with tracking.
        
        Args:
            file_path: Path to the file to read (relative or absolute)
            offset: Starting line (0-indexed)
            limit: Maximum number of lines to read
        
        Returns:
            File content
        """
        # Normalize path to ensure compatibility
        normalized_path = self._normalize_path(file_path)
        
        # Force smaller limit for skills (progressive disclosure)
        if self._is_skill_file(normalized_path):
            limit = min(limit, 50)  # Maximum 50 lines at a time for skills
            self._log_skill_access(normalized_path, offset, limit)
        
        # Call the original FilesystemBackend method with normalized path
        result = await super().aread(normalized_path, offset, limit)
        
        return result
    
    def _is_skill_file(self, file_path: str) -> bool:
        """Check if the file is a skill documentation file."""
        return (
            'SKILL.md' in file_path or 
            ('/skills/' in file_path and file_path.endswith('.md')) or
            ('/.agent/skills/' in file_path and file_path.endswith('.md'))
        )
    
    def _log_skill_access(self, path: str, offset: int, limit: int):
        """
        Log a skill access.
        
        Args:
            path: Path of the accessed skill
            offset: Read offset
            limit: Line limit read
        """
        access_log = {
            "timestamp": datetime.now().isoformat(),
            "query_id": self._current_query_id,
            "skill_path": path,
            "offset": offset,
            "limit": limit,
            "access_type": "read"
        }
        
        # Save in memory
        self._skills_accessed.append(access_log)
        
        # Save to JSONL file (append)
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(access_log, ensure_ascii=False) + "\n")
        except Exception as e:
            # Silent failure to avoid breaking the agent
            print(f"Warning: Failed to log skill access: {e}")
    
    def get_skills_for_query(self, query_id: str) -> List[dict]:
        """
        Return all skills accessed for a specific query.
        
        Args:
            query_id: Query ID
        
        Returns:
            List of access logs for that query
        """
        return [
            log for log in self._skills_accessed 
            if log.get("query_id") == query_id
        ]
    
    def reset_tracking(self):
        """Reset tracking (useful between queries)."""
        self._skills_accessed = []
        self._current_query_id = None
