"""
Script to determine if an IFC model contains load-bearing walls.

This script defines a function `has_load_bearing_walls` which uses the
learned skill `find_elements_with_property` to search for walls with a
property indicating load-bearing. It prints the result to stdout.

Usage:
    python3 sandbox/check_load_bearing_walls_arq_filter.py
"""
from typing import List
from skills.learned.properties.scripts.find_elements_with_property import find_elements_with_property


def has_load_bearing_walls(ifc_path: str) -> bool:
    """
    Check if the provided IFC model contains any load-bearing walls.

    Args:
        ifc_path (str): Path to the IFC file.

    Returns:
        bool: True if at least one wall is marked as load-bearing, False otherwise.

    Example:
        >>> has_load_bearing_walls('./projects/fnde/ARQ.ifc')
        True
    """
    # Common property set and property names where load-bearing info may be stored
    candidates = [
        ('Pset_WallCommon', 'LoadBearing'),
        ('', 'LoadBearing'),  # any pset
        ('Pset_WallCommon', 'Loadbearing'),
        ('Pset_WallLoad', 'IsLoadBearing'),
    ]

    for pset, prop in candidates:
        matches = find_elements_with_property(ifc_path, 'IfcWall', pset, prop, [True, 'true', 'yes', '1'])
        if matches:
            return True
    # Also check IfcWallStandardCase
    for pset, prop in candidates:
        matches = find_elements_with_property(ifc_path, 'IfcWallStandardCase', pset, prop, [True, 'true', 'yes', '1'])
        if matches:
            return True

    return False


if __name__ == '__main__':
    ifc = './projects/fnde/ARQ.ifc'
    result = has_load_bearing_walls(ifc)
    print(result)
