"""
Count unique material names in an IFC model that contain a search term.

Purpose:
    Scan material-related entities in an IFC file (IfcMaterial, IfcMaterialList,
    IfcMaterialLayerSet, IfcMaterialLayer, and IfcRelAssociatesMaterial) and
    return the number of unique material names containing the provided term.

Args:
    ifc_path (str): Path to the IFC file.
    term (str): Substring to match inside material names (case-insensitive).

Returns:
    int: Number of unique material names that contain the term.

Example:
    >>> count_unique_materials('./projects/fnde/ARQ.ifc', 'Cerâmica')
    3
"""
from typing import Set
import ifcopenshell


def _extract_names_from_material_entity(mat) -> Set[str]:
    """Helper: extract possible material names from a material-related entity.

    Args:
        mat: An IfcOpenShell entity that may represent a material (IfcMaterial,
             IfcMaterialList, IfcMaterialLayerSet, IfcMaterialLayer, etc.).

    Returns:
        Set[str]: A set of material names found on the entity (may be empty).
    """
    names = set()
    if mat is None:
        return names

    # Direct name attribute
    name = getattr(mat, 'Name', None)
    if name:
        names.add(str(name))

    # If it's a material list, it usually has attribute 'Materials'
    materials = getattr(mat, 'Materials', None)
    if materials:
        for m in materials:
            if m is None:
                continue
            n = getattr(m, 'Name', None)
            if n:
                names.add(str(n))

    # If it's a material layer set, it may have 'MaterialLayers' or 'MaterialLayers' list
    layers = getattr(mat, 'MaterialLayers', None) or getattr(mat, 'Layers', None)
    if layers:
        for layer in layers:
            if layer is None:
                continue
            # layers may be IfcMaterialLayer with attribute 'Material'
            matref = getattr(layer, 'Material', None)
            if matref is None:
                # sometimes layer itself has Name
                ln = getattr(layer, 'Name', None)
                if ln:
                    names.add(str(ln))
            else:
                ln = getattr(matref, 'Name', None)
                if ln:
                    names.add(str(ln))

    # If it's an IfcMaterialLayer (single layer), attempt to get referenced material
    matref = getattr(mat, 'Material', None)
    if matref is not None:
        ln = getattr(matref, 'Name', None)
        if ln:
            names.add(str(ln))

    return names


def count_unique_materials(ifc_path: str, term: str) -> int:
    """Count unique material names containing `term` in the IFC model.

    This function opens the IFC model and searches common material-bearing
    entities (IfcMaterial, IfcMaterialList, IfcMaterialLayerSet, IfcMaterialLayer,
    and IfcRelAssociatesMaterial). It collects all material names and returns
    how many unique names contain the provided search term (case-insensitive).

    Args:
        ifc_path (str): Path to the IFC file.
        term (str): Substring to search for inside material names.

    Returns:
        int: Count of unique material names containing the term.

    Example:
        >>> count_unique_materials('./projects/fnde/ARQ.ifc', 'Cerâmica')
        2
    """
    model = ifcopenshell.open(ifc_path)
    found_names = set()
    search = term.lower()

    # Inspect direct IfcMaterial entities
    for mat in model.by_type('IfcMaterial'):
        name = getattr(mat, 'Name', None)
        if name and search in str(name).lower():
            found_names.add(str(name))

    # Inspect IfcMaterialList, IfcMaterialLayerSet, IfcMaterialLayer and other material holders
    for ent_type in ('IfcMaterialList', 'IfcMaterialLayerSet', 'IfcMaterialLayer'):
        for ent in model.by_type(ent_type):
            names = _extract_names_from_material_entity(ent)
            for n in names:
                if search in n.lower():
                    found_names.add(n)

    # Inspect relations that associate materials to products
    for rel in model.by_type('IfcRelAssociatesMaterial'):
        relating = getattr(rel, 'RelatingMaterial', None)
        if relating is None:
            continue
        names = _extract_names_from_material_entity(relating)
        for n in names:
            if search in n.lower():
                found_names.add(n)

    return len(found_names)
