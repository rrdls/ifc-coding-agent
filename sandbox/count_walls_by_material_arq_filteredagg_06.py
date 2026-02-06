from skills.learned.quantities.scripts.count_entities import count_entities
import ifcopenshell
import ifcopenshell.util.selector
from typing import List


def count_walls_with_material(ifc_path: str, material_name: str) -> int:
    """
    Purpose: Count IfcWall entities in an IFC model that use a material with the given name.

    Args:
        ifc_path (str): Path to the IFC file.
        material_name (str): Exact material name to filter by (case-sensitive as in IFC).

    Returns:
        int: Number of IfcWall elements that reference the given material name.

    Example:
        >>> count_walls_with_material('./projects/fnde/ARQ.ifc', 'GENÉRICO - VEDAÇÃO INTERNA')
        5
    """
    model = ifcopenshell.open(ifc_path)
    # Use selector filter: class IfcWall and material equals the provided name
    query = f"IfcWall, material=\"{material_name}\""
    walls = ifcopenshell.util.selector.filter_elements(model, query)
    return len(walls)


if __name__ == '__main__':
    ifc_file = './projects/fnde/ARQ.ifc'
    material = 'GENÉRICO - VEDAÇÃO INTERNA'
    count = count_walls_with_material(ifc_file, material)
    print(count)
