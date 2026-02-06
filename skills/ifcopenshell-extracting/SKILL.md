---
name: IfcOpenShell Extracting
description: "Extract values from IFC elements (attributes, properties, coordinates, materials) using Selector Syntax."
---

# IfcOpenShell Extracting

Extract values from IFC elements using **Selector Syntax**.

## Function Index

| Function | File | Description |
|----------|------|-------------|
| `extract_attributes()` | [extract_attributes.py](scripts/extract_attributes.py) | Extract class, id, Name, predefined_type |
| `extract_properties()` | [extract_properties.py](scripts/extract_properties.py) | Extract property set values (Pset_*) |
| `extract_type()` | [extract_type.py](scripts/extract_type.py) | Extract type name and occurrence count |
| `extract_spatial()` | [extract_spatial.py](scripts/extract_spatial.py) | Extract spatial location (storey, building, site) |
| `extract_materials()` | [extract_materials.py](scripts/extract_materials.py) | Extract material name and layer info |
| `extract_coordinates()` | [extract_coordinates.py](scripts/extract_coordinates.py) | Extract x, y, z and geospatial coordinates |
| `extract_classification()` | [extract_classification.py](scripts/extract_classification.py) | Extract classification, group, system, zone |

---

## Query Keys Reference

### Basic Attributes

| Key | Description |
|-----|-------------|
| `class` | IFC class name |
| `id` | STEP ID |
| `Name` | Name attribute |
| `predefined_type` | PredefinedType (with inheritance) |

### Properties

| Key | Description |
|-----|-------------|
| `Pset_WallCommon.Status` | Specific property value |
| `/Pset_.*Common/.Status` | Property with regex for pset name |

### Type

| Key | Description |
|-----|-------------|
| `type.Name` | Type name |
| `types.count` | Number of occurrences |

### Spatial Location

| Key | Description |
|-----|-------------|
| `container` | Immediate container |
| `space.Name` | Space name |
| `storey.Name` | Storey name |
| `building.Name` | Building name |
| `site.Name` | Site name |
| `parent.Name` | Parent in hierarchy |

### Materials

| Key | Description |
|-----|-------------|
| `materials.count` | Material count |
| `material.Name` | Material/set name |
| `material.item.0.Name` | First layer name |

### Coordinates

| Key | Description |
|-----|-------------|
| `x`, `y`, `z` | Local coordinates |
| `easting`, `northing`, `elevation` | Geospatial coordinates |

### Classifications & Groups

| Key | Description |
|-----|-------------|
| `classification` | Classification references |
| `group` | Groups |
| `system` | Systems (MEP) |
| `zone` | Zones |

---

## Quick Reference

**Basic usage:**
```python
import ifcopenshell.util.selector
value = ifcopenshell.util.selector.get_element_value(element, "key")
```

For complete examples of each extraction type, see the [scripts/](scripts/) directory.
