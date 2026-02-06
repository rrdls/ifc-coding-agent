"""
Count entities of a specified IFC class that reference materials whose names contain a keyword.

Purpose:
    Search an IFC model for all instances of a given IFC class (e.g., IfcCovering) and
    count how many of them have at least one associated material whose name contains the
    provided keyword (case-insensitive). The implementation inspects common material
    assignment patterns (IfcRelAssociatesMaterial with IfcMaterial, IfcMaterialLayerSet,
    IfcMaterialLayerSetUsage, IfcMaterialConstituentSet and IfcMaterialList).

Args:
    ifc_path (str): Path to the IFC file.
    entity_type (str): IFC entity type to search for (e.g., "IfcCovering").
    material_keyword (str): Substring to match against material names (case-insensitive).

Returns:
    int: Number of entities of the given type that reference materials whose names contain
         the provided keyword.

Example:
    >>> count_entities_by_material_keyword('./projects/fnde/ARQ.ifc', 'IfcCovering', 'epoxy')
    3
"""
from typing import List
import ifcopenshell


def _collect_material_names_from_relating(rm) -> List[str]:
    """Extract material names from a RelatingMaterial entity.

    Args:
        rm: An Ifc material-related entity (various types).
    Returns:
        List[str]: material names found (may be empty).
    """
    names: List[str] = []
    if rm is None:
        return names
    # IfcMaterial
    try:
        if rm.is_a('IfcMaterial'):
            if getattr(rm, 'Name', None):
                names.append(rm.Name)
            return names
    except Exception:
        pass

    # IfcMaterialLayerSetUsage -> ForLayerSet -> MaterialLayers
    try:
        if rm.is_a('IfcMaterialLayerSetUsage'):
            layer_set = getattr(rm, 'ForLayerSet', None)
            if layer_set is not None and hasattr(layer_set, 'MaterialLayers'):
                for layer in layer_set.MaterialLayers or []:
                    mat = getattr(layer, 'Material', None)
                    if mat is not None and getattr(mat, 'Name', None):
                        names.append(mat.Name)
            return names
    except Exception:
        pass

    # IfcMaterialLayerSet
    try:
        if rm.is_a('IfcMaterialLayerSet'):
            for layer in getattr(rm, 'MaterialLayers', []) or []:
                mat = getattr(layer, 'Material', None)
                if mat is not None and getattr(mat, 'Name', None):
                    names.append(mat.Name)
            return names
    except Exception:
        pass

    # IfcMaterialConstituentSet
    try:
        if rm.is_a('IfcMaterialConstituentSet'):
            for cons in getattr(rm, 'MaterialConstituents', []) or []:
                mat = getattr(cons, 'Material', None)
                if mat is not None and getattr(mat, 'Name', None):
                    names.append(mat.Name)
            return names
    except Exception:
        pass

    # IfcMaterialList
    try:
        if rm.is_a('IfcMaterialList'):
            for mat in getattr(rm, 'Materials', []) or []:
                if getattr(mat, 'Name', None):
                    names.append(mat.Name)
            return names
    except Exception:
        pass

    return names


def count_entities_by_material_keyword(ifc_path: str, entity_type: str, material_keyword: str) -> int:
    """Count entities of a given IFC class that reference materials matching a keyword.

    Args:
        ifc_path: Path to IFC file.
        entity_type: IFC class name to search (e.g., 'IfcCovering').
        material_keyword: Case-insensitive substring to match within material names.

    Returns:
        int: Number of matching entities.

    Example:
        >>> count_entities_by_material_keyword('./projects/fnde/ARQ.ifc', 'IfcCovering', 'epoxy')
        4
    """
    model = ifcopenshell.open(ifc_path)
    elements = model.by_type(entity_type)
    keyword = material_keyword.lower()
    count = 0

    # Collect all IfcRelAssociatesMaterial
    rels = model.by_type('IfcRelAssociatesMaterial')

    for el in elements:
        matched = False
        for rel in rels:
            try:
                related = getattr(rel, 'RelatedObjects', None)
                if not related:
                    continue
                # RelatedObjects may be list
                related_list = related if isinstance(related, (list, tuple)) else [related]
                if el not in related_list:
                    continue
                rm = getattr(rel, 'RelatingMaterial', None)
                names = _collect_material_names_from_relating(rm)
                for n in names:
                    if n and keyword in n.lower():
                        matched = True
                        break
            except Exception:
                continue
            if matched:
                break
        if matched:
            count += 1

    return count
