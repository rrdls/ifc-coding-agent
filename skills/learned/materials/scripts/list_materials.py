"""
List materials in an IFC model that contain a given keyword.

Purpose:
    Search common IFC material entities (IfcMaterial, IfcMaterialLayer, IfcMaterialList,
    IfcMaterialLayerSet) and return unique material names that contain the
    provided keyword (case-insensitive).

Args:
    ifc_path (str): Path to the IFC file to open.
    keyword (str): Substring to search for in material names (default: "Granito").

Returns:
    list[str]: Sorted list of unique material names containing the keyword.

Example:
    >>> from skills.learned.materials.scripts.list_materials import list_materials
    >>> list_materials('./projects/fnde/ARQ.ifc', keyword='Granito')
    ['Granito Natural', 'Granito Polido']
"""
from typing import List
import ifcopenshell


def list_materials(ifc_path: str, keyword: str = "Granito") -> List[str]:
    """Return material names from the IFC that contain keyword (case-insensitive).

    The function searches several IFC material-related entity types to collect
    candidate names:
      - IfcMaterial
      - IfcMaterialLayer (checks layer.Name and referenced Material.Name)
      - IfcMaterialList (checks referenced Materials' names)
      - IfcMaterialLayerSet (checks Name)

    Args:
        ifc_path: Path to the IFC file.
        keyword: Substring to match inside material names. Case-insensitive.

    Returns:
        A sorted list of unique material names (strings) that contain the keyword.

    Example:
        >>> list_materials('./projects/fnde/ARQ.ifc', 'Granito')
        ['Granito A', 'Granito B']
    """
    model = ifcopenshell.open(ifc_path)
    keyword_lower = keyword.lower()
    found = set()

    # Helper to check and add name
    def check_name(name):
        if not name:
            return
        try:
            if keyword_lower in name.lower():
                found.add(name)
        except Exception:
            # name might not be a str
            pass

    # IfcMaterial
    for m in model.by_type('IfcMaterial'):
        check_name(getattr(m, 'Name', None))

    # IfcMaterialLayer (has .Name and .Material -> IfcMaterial)
    for ml in model.by_type('IfcMaterialLayer'):
        check_name(getattr(ml, 'Name', None))
        mat = getattr(ml, 'Material', None)
        if mat is not None:
            # mat can be IfcMaterial or other
            check_name(getattr(mat, 'Name', None))

    # IfcMaterialList (Materials: list of IfcMaterial)
    for mlist in model.by_type('IfcMaterialList'):
        materials = getattr(mlist, 'Materials', None)
        if materials:
            for mat in materials:
                check_name(getattr(mat, 'Name', None))

    # IfcMaterialLayerSet (Name)
    for mls in model.by_type('IfcMaterialLayerSet'):
        check_name(getattr(mls, 'Name', None))

    return sorted(found)
