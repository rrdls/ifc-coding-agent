---
name: IfcOpenShell Filtering
description: "Filter IFC elements by class, attributes, properties, material, location using Selector Syntax."
---

# IfcOpenShell Filtering

Filter IFC elements efficiently using **Selector Syntax**.

## Function Index

| Function | File | Description |
|----------|------|-------------|
| `filter_by_class()` | [filter_by_class.py](scripts/filter_by_class.py) | Filter elements by IFC class (IfcWall, IfcSlab, etc.) |
| `filter_by_globalid()` | [filter_by_globalid.py](scripts/filter_by_globalid.py) | Filter elements by unique GlobalId identifier |
| `filter_by_attribute()` | [filter_by_attribute.py](scripts/filter_by_attribute.py) | Filter elements by attribute values (exact or regex) |
| `filter_by_property()` | [filter_by_property.py](scripts/filter_by_property.py) | Filter elements by property set values |
| `filter_by_type()` | [filter_by_type.py](scripts/filter_by_type.py) | Filter elements by element type |
| `filter_by_material()` | [filter_by_material.py](scripts/filter_by_material.py) | Filter elements by material name |
| `filter_by_classification()` | [filter_by_classification.py](scripts/filter_by_classification.py) | Filter elements by classification reference |
| `filter_by_location()` | [filter_by_location.py](scripts/filter_by_location.py) | Filter elements by spatial location |
| `combine_filters_and()` | [combine_filters_and.py](scripts/combine_filters_and.py) | Combine multiple filters with AND logic (comma separator) |
| `combine_filters_or()` | [combine_filters_or.py](scripts/combine_filters_or.py) | Combine multiple filter groups with OR logic (+ separator) |

---

## Filter Syntax Reference

### Available Filters

| Filter | Syntax | Example |
|--------|---------|---------|
| **Class** | `[!] IfcClass` | `IfcWall`, `! IfcWindow` |
| **GlobalId** | `[!] guid` | `325Q7...`, `! 325Q7...` |
| **Attribute** | `Attr=value` | `Name=D01`, `Name=/D[0-9]+/` |
| **Property** | `Pset.Prop=value` | `Pset_WallCommon.FireRating=2HR` |
| **Type** | `type=value` | `type=WT01` |
| **Material** | `material=value` | `material=concrete` |
| **Classification** | `classification=value` | `classification=/Pr_.*` |
| **Location** | `location=value` | `location="Level 3"` |
| **Parent** | `parent=value` | `parent="Building A"` |
| **Query** | `query:keys=value` | `query:types.count=0` |

### Comparison Operators

| Operator | Description |
|----------|-------------|
| `=` | Equal to |
| `!=` | Not equal to |
| `>` | Greater than |
| `>=` | Greater or equal |
| `<` | Less than |
| `<=` | Less or equal |
| `*=` | Contains |
| `!*=` | Does not contain |

### Value Types

| Type | Example | Use |
|------|---------|-----|
| String with quotes | `"foo \"bar\" baz"` | Values with spaces or special characters |
| String without quotes | `foobarbaz` | Simple values |
| Regex | `/foo.*baz/` | Pattern matching |

---

## Combining Filters

### AND Logic
Use **comma (`,`)** to combine filters - all conditions must be met.

Example: `IfcWall, material=concrete, Pset_WallCommon.FireRating=2HR`

See [combine_filters_and.py](scripts/combine_filters_and.py) for examples.

### OR Logic
Use **plus (`+`)** to combine filter groups - any group can match.

Example: `IfcSlab, material=concrete + IfcDoor`

See [combine_filters_or.py](scripts/combine_filters_or.py) for examples.

---

## Quick Reference

**Basic usage:**
```python
import ifcopenshell.util.selector
elements = ifcopenshell.util.selector.filter_elements(model, "query")
```

**Common patterns:**
- Single class: `"IfcWall"`
- Multiple classes: `"IfcWall, IfcSlab"`
- Exclude class: `"IfcElement, ! IfcWall"`
- By property: `"IfcWall, Pset_WallCommon.FireRating=2HR"`
- By material: `"IfcWall, material=concrete"`
- By location: `"IfcPump, location=\"Level 3\""`
- Regex: `"IfcDoor, Name=/D[0-9]{2}/"`

For complete examples of each filter type, see the [scripts/](scripts/) directory.
