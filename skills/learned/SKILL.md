---
name: learned-ifc-functions
description: Reusable Python functions extracted from successful IFC queries. Use these functions BEFORE writing new code. Import with: from skills.learned.<category>.scripts.<module> import <function>
---

# Learned IFC Functions

This skill contains **validated, reusable functions** extracted from successful benchmark queries.

## How to Use

1. **Check this index FIRST** before writing new code
2. **Import the function** instead of rewriting logic
3. **Extend** existing functions if needed

## Function Index

| Function | Category | File | Description | Tags | Source Queries |
|----------|----------|------|-------------|------|----------------|
| *(functions will be added as queries succeed)* |
## Categories

### [Quantities](quantities/SKILL.md)
Functions for counting, summing, and aggregating IFC entities.

### [Properties](properties/SKILL.md)
Functions for extracting properties, elevations, and attributes.

### [Relationships](relationships/SKILL.md)
Functions for navigating entity relationships and material associations.

### [Spatial](spatial/SKILL.md)
Functions for spatial queries (storeys, containment, zones).

### [Geometry](geometry/SKILL.md)
Functions for geometric calculations (areas, volumes, bounding boxes).

### [Validation](validation/SKILL.md)
Functions for model verification and compliance checking.

### [Transformation](transformation/SKILL.md)
Functions for data conversion, unit handling, and aggregation.

### [Uncategorized](uncategorized/SKILL.md)
Functions that don't fit existing categories (emerging patterns).

---

## Adding New Functions

New functions are automatically extracted from successful queries by the SkillBuilder.

Requirements for a function to be saved:
1. Query must **execute successfully** (no runtime errors)
2. Code must be **modular** (reusable function, not just script)
3. Function must have **docstring** with args, returns, and example

## Multi-Tag System

Each function is automatically tagged based on keywords in its name and docstring:
- `element_filtering`: filter, select, find, get, search
- `aggregation`: sum, count, group, collect, aggregate
- `hierarchy_traversal`: parent, child, contained, decomposed
- `property_extraction`: property, pset, attribute, value
- `unit_handling`: unit, convert, scale
- `error_handling`: validate, check, verify

Functions can have multiple tags for flexible discovery.

## Pattern Discovery

Functions that don't match existing categories are logged to `uncategorized_log.jsonl` for analysis. Run `python deep-agent/uncategorized_analyzer.py` to identify emerging patterns.
