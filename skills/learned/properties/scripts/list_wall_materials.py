"""
List unique materials used by walls in an IFC model.

This is a generic reusable function intended to be imported by sandbox query
scripts. It inspects material associations on wall elements and their types
and collects material names from common IFC material constructs.
"""
from typing import List, Set
import ifcopenshell
import ifcopenshell.util.selector


def list_wall_materials(ifc_path: str) -> List[str]:
    """List unique material names used by wall elements in an IFC file.

    Args:
        ifc_path (str): Path to the IFC file to open.

    Returns:
        List[str]: Sorted list of unique material names. If no materials are
                   found, returns an empty list.

    Example:
        >>> list_wall_materials('./projects/fnde/ARQ.ifc')
        ['Concrete - Generic', 'Gypsum Board']
    """
    model = ifcopenshell.open(ifc_path)

    # Select walls (including standard case variants)
    walls = ifcopenshell.util.selector.filter_elements(model, "IfcWall, IfcWallStandardCase")

    material_names: Set[str] = set()

    def extract_from_relating_material(relating_material):
        """Helper to extract material names from various relating material types."""
        if relating_material is None:
            return
        t = relating_material
        ttype = t.is_a()
        # If it's a direct material
        if ttype == 'IfcMaterial':
            name = getattr(t, 'Name', None)
            if name:
                material_names.add(name)
        # If it's a material list
        elif ttype == 'IfcMaterialList':
            for m in getattr(t, 'Materials', []) or []:
                name = getattr(m, 'Name', None)
                if name:
                    material_names.add(name)
        # If it's a material layer set
        elif ttype == 'IfcMaterialLayerSet':
            for layer in getattr(t, 'MaterialLayers', []) or []:
                mat = getattr(layer, 'Material', None)
                if mat is not None:
                    name = getattr(mat, 'Name', None)
                    if name:
                        material_names.add(name)
        # If it's a usage wrapper (relating to a layer set)
        elif ttype == 'IfcMaterialLayerSetUsage':
            mls = getattr(t, 'ForLayerSet', None) or getattr(t, 'RelatingMaterial', None)
            if mls is not None and mls.is_a() == 'IfcMaterialLayerSet':
                for layer in getattr(mls, 'MaterialLayers', []) or []:
                    mat = getattr(layer, 'Material', None)
                    if mat is not None:
                        name = getattr(mat, 'Name', None)
                        if name:
                            material_names.add(name)

    # Inspect associations on each wall
    for wall in walls:
        # Direct associations (IfcRelAssociatesMaterial)
        for rel in getattr(wall, 'HasAssociations', []) or []:
            try:
                if rel.is_a('IfcRelAssociatesMaterial'):
                    extract_from_relating_material(getattr(rel, 'RelatingMaterial', None))
            except Exception:
                # defensive: some unexpected relation objects may raise
                continue

        # Materials can also be defined on the element type referenced by
        # IfcRelDefinesByType relationships
        for rel in getattr(wall, 'IsDefinedBy', []) or []:
            try:
                if rel.is_a('IfcRelDefinesByType'):
                    relating_type = getattr(rel, 'RelatingType', None)
                    if relating_type is None:
                        continue
                    for rel2 in getattr(relating_type, 'HasAssociations', []) or []:
                        if rel2.is_a('IfcRelAssociatesMaterial'):
                            extract_from_relating_material(getattr(rel2, 'RelatingMaterial', None))
            except Exception:
                continue

    # Return sorted list
    return sorted([n for n in material_names if n])
