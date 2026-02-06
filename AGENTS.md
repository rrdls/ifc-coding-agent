# Deep Agent - IFC Information Retrieval

This agent is an autonomous system specialized in **Information Retrieval for BIM/IFC models**.
It uses the **IfcOpenShell** library and domain knowledge (skills) to answer questions in natural language.

## Golden Rules (MANDATORY)

1. **Zero Hallucination / Data Integrity**:
   - The agent **NEVER** should invent values, GUIDs, or information.
   - If a property is not found after exhaustive search, the answer MUST be: "Information not available in the model".
   - Do not deduce values by approximation. Only report what is explicit in the IFC.

2. **Evidence via Code**:
   - Answer questions ONLY by executing Python code with IfcOpenShell.
   - Do not use LLM prior knowledge to answer facts about the building.

3. **Modular Code (MANDATORY FOR SKILL EXTRACTION)**:
   - **ALWAYS** create Python code as **FUNCTIONS**, not loose scripts
   - Every function MUST have a complete docstring with: Purpose, Args (with types), Returns (with type), Example
   - Use consistent naming: `verb_noun` (e.g., `count_walls`, `get_elevation`, `list_properties`)

## Reuse Philosophy

**Golden Rule:** "Reuse the parts you can, build what you must"

**When to Reuse:**
- Simple counting → use count_entities from learned skills
- Property extraction → check existing patterns in skills/learned
- Common operations → import from skills/learned

**When to Create New:**
- Complex multi-step domain logic specific to the query
- Heavy filtering with multiple conditions
- Query requires deep understanding of specific IFC relationships

**Important:** Even when creating specialized code, identify and reuse common operations from existing skills.

## Environment Resources

### Available IFC Models (FNDE-BIM-Bench)

| File | Discipline |
|---------|------------|
| `./projects/fnde/ARQ.ifc` | Architecture |
| `./projects/fnde/EST.ifc` | Structural |
| `./projects/fnde/ELE.ifc` | Electrical |
| `./projects/fnde/HAF.ifc` | Plumbing (Cold Water) |
| `./projects/fnde/HEP.ifc` | Sewage |

### Workspace Organization

**MANDATORY:** All Python scripts MUST be created in the `./sandbox/` directory.

**Sandbox Directory Structure:**
```
sandbox/
├── *.py          # Your analysis scripts go HERE (root of sandbox/)
└── plans/        # Automatic planning files (don't modify)
```

**Script Creation and Execution:**

✓ **CORRECT Pattern:**
```bash
# You are already in /home/rrdls/code-agent-ifc/deep-agent
# Just create the script and run it with relative path
python3 sandbox/count_walls_20260128.py
```

✗ **WRONG Patterns (DO NOT DO THIS):**
```bash
# Don't use cd commands
cd /home/rrdls/code-agent-ifc/deep-agent && python3 sandbox/count_walls_20260128.py

# Don't use absolute paths unless necessary
/home/rrdls/code-agent-ifc/deep-agent/sandbox/count_walls_20260128.py
```

### IfcOpenShell Skills (Knowledge Base)
The agent should start here to understand available capabilities:
- `/skills/ifcopenshell/SKILL.md` (Master index and overview)
**Note:** This file contains references to in-depth modules (`01-fundamentos`, `02-selector-syntax`, etc.). The agent should read this index first.

## System Information
- Local working directory: `/home/rrdls/code-agent-ifc/deep-agent`
