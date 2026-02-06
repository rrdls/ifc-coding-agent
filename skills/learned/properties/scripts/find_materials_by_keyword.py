"""
Find materials in an IFC model by keyword.

This generic function searches common IFC material-related entities and returns
a deduplicated list of material names that contain the provided keyword
(case-insensitive).

Args:
    ifc_path (str): Path to the IFC file.
    keyword (str): Substring to search for in material names (case-insensitive).

Returns:
    list[str]: Sorted list of unique material names that contain the keyword.

Example:
    >>> find_materials_by_keyword('./projects/fnde/ARQ.ifc', 'Pintura')
    ['Pintura Branco', 'Pintura Texturada']
"""
from typing import List
import ifcopenshell


def find_materials_by_keyword(ifc_path: str, keyword: str) -> List[str]:
    """Search IFC model for material names containing keyword.

    The function inspects IfcMaterial and several material container types
    to capture names that may appear in layers, lists or constituents.

    Args:
        ifc_path (str): Path to the IFC file.
        keyword (str): Substring to search for in material names.

    Returns:
        List[str]: Sorted unique material names matching the keyword.
    """
    model = ifcopenshell.open(ifc_path)
    matches = set()
    key = keyword.lower()

    # Helper to add name if it exists and matches
    def check_name(name):
        if not name:
            return
        if key in name.lower():
            matches.add(name)

    # 1. Direct IfcMaterial entities
    for m in model.by_type('IfcMaterial'):
        name = getattr(m, 'Name', None)
        check_name(name)

    # 2. IfcMaterialLayer -> attribute 'Material'
    for layer in model.by_type('IfcMaterialLayer'):
        mat = getattr(layer, 'Material', None)
        if mat is not None:
            name = getattr(mat, 'Name', None)
            check_name(name)

    # 3. IfcMaterialLayerSet -> has MaterialLayers list
    for mls in model.by_type('IfcMaterialLayerSet'):
        layers = getattr(mls, 'MaterialLayers', []) or []
        for layer in layers:
            mat = getattr(layer, 'Material', None)
            if mat is not None:
                name = getattr(mat, 'Name', None)
                check_name(name)

    # 4. IfcMaterialList -> has 'Materials'
    for mlist in model.by_type('IfcMaterialList'):
        mats = getattr(mlist, 'Materials', []) or []
        for mat in mats:
            name = getattr(mat, 'Name', None)
            check_name(name)

    # 5. IfcMaterialConstituent -> attribute 'Material'
    for mc in model.by_type('IfcMaterialConstituent'):
        mat = getattr(mc, 'Material', None)
        if mat is not None:
            name = getattr(mat, 'Name', None)
            check_name(name)

    # 6. IfcMaterialProfile -> attribute 'Material'
    for mp in model.by_type('IfcMaterialProfile'):
        mat = getattr(mp, 'Material', None)
        if mat is not None:
            name = getattr(mat, 'Name', None)
            check_name(name)

    # 7. As a fallback, inspect IfcRelAssociatesMaterial relationships
    for rel in model.by_type('IfcRelAssociatesMaterial'):
        mat = getattr(rel, 'RelatingMaterial', None)
        if mat is None:
            continue
        # RelatingMaterial can be IfcMaterial, IfcMaterialList, IfcMaterialLayerSet
        if hasattr(mat, 'Name'):
            check_name(getattr(mat, 'Name', None))
        # If it's a list
        mats = getattr(mat, 'Materials', None) or getattr(mat, 'MaterialLayers', None) or []
        if mats:
            for item in mats:
                # item may be IfcMaterialLayer with .Material
                if hasattr(item, 'Name'):
                    check_name(getattr(item, 'Name', None))
                else:
                    mat2 = getattr(item, 'Material', None)
                    if mat2 is not None:
                        check_name(getattr(mat2, 'Name', None))

    return sorted(matches)
