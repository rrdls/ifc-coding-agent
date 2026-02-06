---
name: IfcOpenShell Schema Querying
description: "Query IFC schema definitions and buildingSMART property set templates."
---

# IfcOpenShell Schema Querying

Query IFC schema structure and property set templates.

## Function Index

| Function | File | Description |
|----------|------|-------------|
| `query_schema()` | [query_schema.py](scripts/query_schema.py) | Load schema, list declarations, get by name |
| `class_hierarchy()` | [class_hierarchy.py](scripts/class_hierarchy.py) | Navigate supertype/subtypes inheritance |
| `entity_attributes()` | [entity_attributes.py](scripts/entity_attributes.py) | Get direct, all, and inverse attributes |
| `pset_templates()` | [pset_templates.py](scripts/pset_templates.py) | Query buildingSMART pset templates |

---

## Quick Reference

| Operation | Code |
|-----------|------|
| Load schema | `ifcopenshell.schema_by_name("IFC4")` |
| List declarations | `schema.declarations()` |
| Get declaration | `schema.declaration_by_name("IfcWall")` |
| Check abstract | `declaration.is_abstract()` |
| Get supertype | `declaration.supertype()` |
| Get subtypes | `declaration.subtypes()` |
| Direct attributes | `declaration.attributes()` |
| All attributes | `declaration.all_attributes()` |
| Inverse attributes | `declaration.all_inverse_attributes()` |
| Load pset templates | `ifcopenshell.util.pset.PsetQto("IFC4")` |
| Applicable psets | `templates.get_applicable_names("IfcWall")` |
| Get pset by name | `templates.get_by_name("Pset_WallCommon")` |

---

## Available Schemas

| Schema | Description |
|--------|-------------|
| `IFC2X3` | IFC 2x3 TC1 |
| `IFC4` | IFC 4 ADD2 TC1 |
| `IFC4X3` | IFC 4.3 |

For complete examples, see the [scripts/](scripts/) directory.
