---
name: IfcOpenShell Geometry Processing
description: "Process IFC geometry - extract vertices, faces, transformations, batch iteration, and serialize to glTF/OBJ."
---

# IfcOpenShell Geometry Processing

Process and serialize IFC geometry.

## Function Index

| Function | File | Description |
|----------|------|-------------|
| `create_shape()` | [create_shape.py](scripts/create_shape.py) | Process single element geometry |
| `get_matrix()` | [get_matrix.py](scripts/get_matrix.py) | Get transformation matrix (position/rotation) |
| `get_mesh_data()` | [get_mesh_data.py](scripts/get_mesh_data.py) | Get vertices, edges, faces |
| `get_materials()` | [get_materials.py](scripts/get_materials.py) | Get materials and styles |
| `geometry_iterator()` | [geometry_iterator.py](scripts/geometry_iterator.py) | Batch process all elements |
| `export_gltf()` | [export_gltf.py](scripts/export_gltf.py) | Export to glTF/GLB format |
| `export_obj()` | [export_obj.py](scripts/export_obj.py) | Export to OBJ format |

---

## Quick Reference

| Operation | Code |
|-----------|------|
| Process element | `ifcopenshell.geom.create_shape(settings, element)` |
| Settings | `settings = ifcopenshell.geom.settings()` |
| Get matrix | `shape.transformation.matrix` |
| Get numpy matrix | `ifcopenshell.util.shape.get_shape_matrix(shape)` |
| Vertices | `shape.geometry.verts` |
| Faces | `shape.geometry.faces` |
| Edges | `shape.geometry.edges` |
| Grouped vertices | `ifcopenshell.util.shape.get_vertices(geometry)` |
| Grouped faces | `ifcopenshell.util.shape.get_faces(geometry)` |
| Materials | `shape.geometry.materials` |
| Create iterator | `ifcopenshell.geom.iterator(settings, ifc, cores)` |
| Serialize glTF | `ifcopenshell.geom.serializers.gltf(file, settings, ser_settings)` |
| Serialize OBJ | `ifcopenshell.geom.serializers.obj(obj, mtl, settings, ser_settings)` |

---

## Geometry Settings

| Setting | Description |
|---------|-------------|
| `use-python-opencascade` | Return OpenCASCADE BRep instead of mesh |
| `use-world-coords` | Vertices in global coordinates |
| `apply-default-materials` | Apply default materials |
| `dimensionality` | Control geometry types (curves, surfaces, solids) |

---

## Related Modules

| Module | Description |
|--------|-------------|
| `ifcopenshell.geom` | Geometry processing |
| `ifcopenshell.geom.settings` | Geometry settings |
| `ifcopenshell.geom.iterator` | Batch processing iterator |
| `ifcopenshell.geom.serializers` | 3D format serializers |
| `ifcopenshell.util.shape` | Geometry data utilities |
| `ifcopenshell.util.representation` | Representation utilities |

For complete examples, see the [scripts/](scripts/) directory.
