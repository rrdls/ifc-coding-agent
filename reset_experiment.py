#!/usr/bin/env python3
"""
Reset Experiment Environment

Automated script to reset the deep-agent benchmark environment for clean experiment runs.
Removes generated artifacts while preserving core infrastructure.

Usage:
    python reset_experiment.py              # Interactive mode (asks for confirmation)
    python reset_experiment.py --yes        # Silent mode (no confirmation)
    python reset_experiment.py --dry-run    # Show what would be removed
    python reset_experiment.py --backup     # Create backup before removal
"""

import argparse
import shutil
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict


# ANSI color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def print_header(msg: str):
    """Print a styled header message."""
    print(f"\n{Colors.BOLD}{Colors.HEADER}{'='*60}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.HEADER}{msg.center(60)}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.HEADER}{'='*60}{Colors.ENDC}\n")


def print_warning(msg: str):
    """Print a warning message."""
    print(f"{Colors.WARNING}⚠️  {msg}{Colors.ENDC}")


def print_success(msg: str):
    """Print a success message."""
    print(f"{Colors.OKGREEN}✓ {msg}{Colors.ENDC}")


def print_info(msg: str):
    """Print an info message."""
    print(f"{Colors.OKCYAN}ℹ {msg}{Colors.ENDC}")


def print_error(msg: str):
    """Print an error message."""
    print(f"{Colors.FAIL}✗ {msg}{Colors.ENDC}")


# Base directory
BASE_DIR = Path(__file__).parent


# SKILL.md templates
CATEGORY_SKILL_TEMPLATES = {
    "quantities": {
        "description": "Functions for counting, summing, and aggregating IFC entities.",
        "operations": [
            "- Count entities by type",
            "- Sum quantities across elements",
            "- Aggregate statistics",
            "- Calculate totals"
        ]
    },
    "properties": {
        "description": "Functions for extracting properties, elevations, and attributes.",
        "operations": [
            "- Extract element properties",
            "- Get property sets (Psets)",
            "- Access attributes",
            "- Query elevations and dimensions"
        ]
    },
    "relationships": {
        "description": "Functions for navigating entity relationships and material associations.",
        "operations": [
            "- Get material associations",
            "- Navigate containment",
            "- Find related elements",
            "- Query connections"
        ]
    },
    "spatial": {
        "description": "Functions for spatial queries (storeys, containment, zones).",
        "operations": [
            "- Query building storeys",
            "- Navigate spatial hierarchy",
            "- Find contained elements",
            "- Get zones and spaces"
        ]
    },
    "geometry": {
        "description": "Functions for geometric calculations (areas, volumes, bounding boxes).",
        "operations": [
            "- Calculate areas",
            "- Compute volumes",
            "- Get bounding boxes",
            "- Extract coordinates"
        ]
    },
    "validation": {
        "description": "Functions for model verification and compliance checking.",
        "operations": [
            "- Validate schema compliance",
            "- Check data integrity",
            "- Verify relationships",
            "- Audit model quality"
        ]
    },
    "transformation": {
        "description": "Functions for data conversion, unit handling, and aggregation.",
        "operations": [
            "- Convert units",
            "- Transform coordinates",
            "- Aggregate data",
            "- Group elements"
        ]
    },
    "schema": {
        "description": "Functions for querying IFC schema information and metadata.",
        "operations": [
            "- Get IFC schema version",
            "- Query entity definitions",
            "- Extract schema metadata",
            "- Validate schema compliance"
        ]
    },
    "uncategorized": {
        "description": "Functions that don't fit existing categories (emerging patterns).",
        "operations": [
            "- Experimental functions",
            "- Novel patterns",
            "- Unclassified operations"
        ]
    }
}


def create_category_skill_md(category: str) -> str:
    """Generate SKILL.md content for a category."""
    template = CATEGORY_SKILL_TEMPLATES.get(category, {})
    category_title = category.capitalize()
    description = template.get("description", "")
    operations = "\n".join(template.get("operations", []))
    
    return f"""# {category_title} Skills

{description}

## Available Functions

| Function | Script | Description | Tags | Source |
|----------|--------|-------------|------|--------|
| *(auto-populated by SkillBuilder)* |

## Typical Operations

{operations}
"""


def reset_main_skill_md(skill_path: Path, dry_run: bool = False) -> bool:
    """Reset the main SKILL.md by clearing the function table."""
    if not skill_path.exists():
        print_warning(f"Main SKILL.md not found at {skill_path}")
        return False
    
    if dry_run:
        print_info(f"Would reset function table in: {skill_path}")
        return True
    
    with open(skill_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Find the function table and reset it
    new_lines = []
    in_table = False
    table_header_found = False
    
    for i, line in enumerate(lines):
        # Detect table header
        if '| Function | Category | File | Description | Tags | Source Queries |' in line:
            in_table = True
            table_header_found = True
            new_lines.append(line)
            # Add separator
            if i + 1 < len(lines) and lines[i + 1].startswith('|---'):
                new_lines.append(lines[i + 1])
            # Add placeholder row
            new_lines.append('| *(functions will be added as queries succeed)* |\n')
            continue
        
        # Skip rows until we hit the next section
        if in_table:
            if line.startswith('##') or (line.strip() and not line.startswith('|')):
                in_table = False
                new_lines.append(line)
            # Skip table content rows
            continue
        
        new_lines.append(line)
    
    # Write back
    with open(skill_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print_success(f"Reset main SKILL.md: {skill_path}")
    return True


def get_removal_targets() -> Dict[str, List[Path]]:
    """Identify all files and directories to be removed."""
    targets = {
        "results": [],
        "sandbox": [],
        "learned_skills": [],
        "cache": []
    }
    
    # 1. Results directory
    results_dir = BASE_DIR / "results"
    if results_dir.exists():
        for model_dir in results_dir.iterdir():
            if model_dir.is_dir():
                targets["results"].append(model_dir)
    
    # 2. Sandbox scripts and plans
    sandbox_dir = BASE_DIR / "sandbox"
    if sandbox_dir.exists():
        for item in sandbox_dir.iterdir():
            if item.name == ".gitkeep":
                continue
            targets["sandbox"].append(item)
    
    # 3. Learned skills (scripts only, preserve structure)
    learned_dir = BASE_DIR / "skills" / "learned"
    if learned_dir.exists():
        # Uncategorized log
        log_file = learned_dir / "uncategorized_log.jsonl"
        if log_file.exists():
            targets["learned_skills"].append(log_file)
        
        # Dynamically discover ALL category directories (not just hardcoded ones)
        for category_dir in learned_dir.iterdir():
            if not category_dir.is_dir():
                continue
            if category_dir.name.startswith('.'):  # Skip hidden dirs
                continue
            
            # Check for scripts directory in this category
            category_scripts = category_dir / "scripts"
            if category_scripts.exists():
                for script in category_scripts.glob("*.py"):
                    if script.name != "__init__.py":
                        targets["learned_skills"].append(script)
    
    # 4. Cache directories
    for cache_dir in BASE_DIR.rglob("__pycache__"):
        targets["cache"].append(cache_dir)
    
    pytest_cache = BASE_DIR / ".pytest_cache"
    if pytest_cache.exists():
        targets["cache"].append(pytest_cache)
    
    return targets


def create_backup(targets: Dict[str, List[Path]]) -> Path:
    """Create a backup of all files to be removed."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = BASE_DIR.parent / "backups" / f"experiment_backup_{timestamp}"
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    print_info(f"Creating backup at: {backup_dir}")
    
    for category, paths in targets.items():
        for path in paths:
            relative = path.relative_to(BASE_DIR)
            backup_path = backup_dir / relative
            backup_path.parent.mkdir(parents=True, exist_ok=True)
            
            if path.is_dir():
                shutil.copytree(path, backup_path, dirs_exist_ok=True)
            else:
                shutil.copy2(path, backup_path)
    
    print_success(f"Backup created: {backup_dir}")
    return backup_dir


def remove_targets(targets: Dict[str, List[Path]], dry_run: bool = False):
    """Remove all target files and directories."""
    stats = {"files": 0, "dirs": 0, "size": 0}
    
    for category, paths in targets.items():
        if not paths:
            continue
        
        print(f"\n{Colors.BOLD}Cleaning {category}...{Colors.ENDC}")
        
        for path in paths:
            if not path.exists():
                continue
            
            # Calculate size
            if path.is_file():
                stats["size"] += path.stat().st_size
            elif path.is_dir():
                stats["size"] += sum(f.stat().st_size for f in path.rglob("*") if f.is_file())
            
            # Remove
            if dry_run:
                if path.is_dir():
                    print_info(f"  Would remove directory: {path}")
                    stats["dirs"] += 1
                else:
                    print_info(f"  Would remove file: {path}")
                    stats["files"] += 1
            else:
                try:
                    if path.is_dir():
                        shutil.rmtree(path)
                        print_success(f"  Removed directory: {path}")
                        stats["dirs"] += 1
                    else:
                        path.unlink()
                        print_success(f"  Removed file: {path}")
                        stats["files"] += 1
                except Exception as e:
                    print_error(f"  Failed to remove {path}: {e}")
    
    return stats


def recreate_skill_templates(dry_run: bool = False):
    """Recreate SKILL.md templates for all categories."""
    print(f"\n{Colors.BOLD}Recreating SKILL.md templates...{Colors.ENDC}")
    
    learned_dir = BASE_DIR / "skills" / "learned"
    
    # Reset main SKILL.md
    main_skill = learned_dir / "SKILL.md"
    reset_main_skill_md(main_skill, dry_run)
    
    # Discover all category directories dynamically
    discovered_categories = set()
    if learned_dir.exists():
        for category_dir in learned_dir.iterdir():
            if category_dir.is_dir() and not category_dir.name.startswith('.'):
                discovered_categories.add(category_dir.name)
    
    # Combine known and discovered categories
    all_categories = set(CATEGORY_SKILL_TEMPLATES.keys()) | discovered_categories
    
    # Recreate category SKILL.md files
    for category in sorted(all_categories):
        category_dir = learned_dir / category
        category_skill = category_dir / "SKILL.md"
        
        if dry_run:
            print_info(f"  Would recreate: {category_skill}")
        else:
            category_dir.mkdir(parents=True, exist_ok=True)
            scripts_dir = category_dir / "scripts"
            scripts_dir.mkdir(exist_ok=True)
            
            # Create __init__.py if it doesn't exist
            init_file = scripts_dir / "__init__.py"
            if not init_file.exists():
                init_file.touch()
            
            # Write SKILL.md (use template if known, otherwise generic)
            if category in CATEGORY_SKILL_TEMPLATES:
                content = create_category_skill_md(category)
            else:
                # Fallback for dynamically created categories
                content = f"""# {category.capitalize()} Skills

Dynamically created category.

## Available Functions

| Function | Script | Description | Tags | Source |
|----------|--------|-------------|------|--------|
| *(auto-populated by SkillBuilder)* |

## Notes

This category was created dynamically. Consider adding it to CATEGORY_SKILL_TEMPLATES in reset_experiment.py and skill_builder.py.
"""
            
            with open(category_skill, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print_success(f"  Recreated: {category_skill}")


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description="Reset the deep-agent experiment environment",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python reset_experiment.py              # Interactive mode
  python reset_experiment.py --yes        # Automatic yes
  python reset_experiment.py --dry-run    # Show what would happen
  python reset_experiment.py --backup     # Backup before reset
        """
    )
    parser.add_argument('--yes', '-y', action='store_true',
                       help='Skip confirmation prompt')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be removed without actually doing it')
    parser.add_argument('--backup', action='store_true',
                       help='Create backup before removing files')
    
    args = parser.parse_args()
    
    print_header("Deep-Agent Experiment Reset")
    
    # Identify targets
    print("Analyzing current state...")
    targets = get_removal_targets()
    
    total_items = sum(len(paths) for paths in targets.values())
    
    if total_items == 0:
        print_success("Nothing to remove! Environment is already clean.")
        return
    
    # Show what will be removed
    print(f"\n{Colors.BOLD}Items to be removed:{Colors.ENDC}")
    for category, paths in targets.items():
        if paths:
            print(f"  {Colors.OKCYAN}{category.upper()}{Colors.ENDC}: {len(paths)} items")
    
    print(f"\n{Colors.BOLD}Total: {total_items} items{Colors.ENDC}")
    
    if args.dry_run:
        print_warning("\n🔍 DRY RUN MODE - No changes will be made\n")
    
    # Confirmation
    if not args.yes and not args.dry_run:
        print_warning("\n⚠️  This will PERMANENTLY DELETE generated artifacts!")
        print_info("Preserved: dataset, ifcopenshell skills, source code, configs")
        response = input(f"\n{Colors.BOLD}Continue? [y/N]: {Colors.ENDC}").strip().lower()
        if response != 'y':
            print_info("Reset cancelled.")
            return
    
    # Backup
    backup_path = None
    if args.backup and not args.dry_run:
        backup_path = create_backup(targets)
    
    # Remove targets
    stats = remove_targets(targets, dry_run=args.dry_run)
    
    # Recreate SKILL.md templates
    recreate_skill_templates(dry_run=args.dry_run)
    
    # Summary
    print_header("Reset Complete")
    
    if args.dry_run:
        print_info(f"Would remove: {stats['dirs']} directories, {stats['files']} files")
        print_info(f"Would free: {stats['size'] / 1024 / 1024:.2f} MB")
    else:
        print_success(f"Removed: {stats['dirs']} directories, {stats['files']} files")
        print_success(f"Freed: {stats['size'] / 1024 / 1024:.2f} MB")
        
        if backup_path:
            print_success(f"Backup saved to: {backup_path}")
        
        print_success("\n✨ Environment reset complete! Ready for new experiments.")


if __name__ == "__main__":
    main()
