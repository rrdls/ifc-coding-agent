"""Query script: Are there any walls with material 'GENÉRICO - VEDAÇÃO EXTERNA'?

This script defines a function `walls_with_material` that searches the given IFC model
for IfcWall elements associated with a material name exactly matching the query.

Usage:
    python3 sandbox/arq_filtered_aggregation_02.py
"""
from typing import List
from skills.learned.quantities.scripts.count_entities import count_entities
import ifcopenshell
import ifcopenshell.util.selector


def walls_with_material(ifc_path: str, material_name: str) -> List[str]:
    """Find IfcWall elements that have the specified material name.

    Purpose:
        Use IfcOpenShell selector filters to locate IfcWall elements associated with a
        material having the provided name.

    Args:
        ifc_path (str): Path to the IFC file.
        material_name (str): Exact material name to search for (case-sensitive).

    Returns:
        List[str]: List of GlobalIds of the matching IfcWall elements. Empty list if none found.

    Example:
        >>> walls_with_material('./projects/fnde/ARQ.ifc', 'GENÉRICO - VEDAÇÃO EXTERNA')
        ['0$abc123', '1$def456']
    """
    model = ifcopenshell.open(ifc_path)
    # Use selector filter combining class and material name. Quote the material since it has spaces and hyphen.
    query = f"IfcWall, material=\"{material_name}\""
    elements = ifcopenshell.util.selector.filter_elements(model, query)
    # Return GlobalIds for evidence
    return [e.GlobalId for e in elements]


if __name__ == '__main__':
    ifc_file = './projects/fnde/ARQ.ifc'
    material = 'GENÉRICO - VEDAÇÃO EXTERNA'

    # quick count of total walls (using learned skill)
    total_walls = count_entities(ifc_file, 'IfcWall')
    matching = walls_with_material(ifc_file, material)

    print(f"Total IfcWall elements: {total_walls}")
    print(f"Walls with material '{material}': {len(matching)}")
    if matching:
        print('\nList of matching GlobalIds:')
        for gid in matching:
            print(gid)
    else:
        print('No walls found with that material.')
