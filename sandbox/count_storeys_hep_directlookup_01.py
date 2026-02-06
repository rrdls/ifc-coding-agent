"""
Sandbox script to count building storeys in the HEP.ifc model.

This script defines a reusable function `count_building_storeys` which wraps
`count_entities` from the learned quantities skill.

Usage:
    python3 sandbox/count_storeys_hep_directlookup_01.py
"""
from typing import Any
from skills.learned.quantities.scripts.count_entities import count_entities


def count_building_storeys(ifc_path: str) -> int:
    """Count IfcBuildingStorey instances in an IFC model.

    Args:
        ifc_path (str): Path to the IFC file to open.

    Returns:
        int: Number of IfcBuildingStorey entities in the model.

    Example:
        >>> count_building_storeys('./projects/fnde/HEP.ifc')
        5
    """
    return count_entities(ifc_path, 'IfcBuildingStorey')


if __name__ == '__main__':
    path = './projects/fnde/HEP.ifc'
    total = count_building_storeys(path)
    print(total)
