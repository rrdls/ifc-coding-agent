import ast
import builtins
import sys
from pathlib import Path

def get_defined_names(tree):
    """Get all functions/classes defined in the script."""
    defined = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            defined.add(node.name)
        # Also handle assignments at module level (e.g. imports or variable assignments)
        # To be safe, we track imported names separately
    return defined

def get_imported_names(tree):
    """Get all names imported into the script."""
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                name = alias.asname if alias.asname else alias.name
                imported.add(name.split('.')[0]) # simplistic handling
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                name = alias.asname if alias.asname else alias.name
                imported.add(name)
    return imported

def get_called_functions(tree):
    """Get all function names called in the script."""
    calls = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                calls.append((node.func.id, node.lineno))
    return calls

def validate_script(file_path):
    try:
        with open(file_path, 'r') as f:
            source = f.read()
        tree = ast.parse(source)
    except SyntaxError as e:
        return False, f"SyntaxError: {e}"
    except Exception as e:
        return False, f"Could not parse script: {e}"

    defined = get_defined_names(tree)
    imported = get_imported_names(tree)
    # Add script builtins (common ones)
    builtin_names = set(dir(builtins))
    
    # Allow some common library aliases if consistent
    # But strictly, if it calls 'ifcopenshell.open', 'ifcopenshell' must be imported
    
    available = defined | imported | builtin_names
    
    calls = get_called_functions(tree)
    errors = []
    
    for func_name, lineno in calls:
        if func_name not in available:
            # Maybe it's a global variable that is callable?
            # AST analysis for variable assignment is harder, but let's assume functions must be def or import
            # This is strict validation for the agent
            errors.append(f"Line {lineno}: Function '{func_name}' is called but not defined or imported.")

    if errors:
        return False, "\n".join(errors)
    
    return True, "Valid"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python code_validator.py <script_path>")
        sys.exit(1)
        
    path = sys.argv[1]
    is_valid, msg = validate_script(path)
    if is_valid:
        print(f"✅ Script {path} is valid.")
    else:
        print(f"❌ Script {path} contains errors:\n{msg}")
        sys.exit(1)
