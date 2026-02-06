"""
Sandbox query script for ARQ_DIRECTLOOKUP_10: list unique wall materials

This script imports the generic learned function and prints the materials.
"""
from typing import List
from skills.learned.properties.scripts.list_wall_materials import list_wall_materials


def query_list_wall_materials(ifc_path: str) -> List[str]:
    """Query wrapper that returns unique wall materials from the IFC.

    Args:
        ifc_path (str): Path to IFC model

    Returns:
        List[str]: Sorted unique material names

    Example:
        python3 sandbox/list_wall_materials_arq_directlookup_10.py
    """
    return list_wall_materials(ifc_path)


if __name__ == '__main__':
    materials = query_list_wall_materials('./projects/fnde/ARQ.ifc')
    if materials:
        for m in materials:
            print(m)
    else:
        print('No materials found')
