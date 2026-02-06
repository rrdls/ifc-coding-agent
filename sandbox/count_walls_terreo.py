"""
Count walls on the storey named 'TÉRREO' in the ARQ.ifc model.

This script defines a function `count_walls_on_storey` which uses the
reusable `count_entities` function from skills.learned.quantities to perform
a selector-based count restricted to a storey location.

Usage:
    python3 sandbox/count_walls_terreo.py
"""
from typing import Any
from skills.learned.quantities.scripts.count_entities import count_entities


def count_walls_on_storey(ifc_path: str, storey_name: str) -> int:
    """Count IfcWall entities located on a given storey.

    Args:
        ifc_path (str): Path to the IFC file.
        storey_name (str): Name of the storey to filter by (exact match). Example: 'T\u00c9RREO'

    Returns:
        int: Number of IfcWall entities located on the specified storey.

    Example:
        >>> count_walls_on_storey('./projects/fnde/ARQ.ifc', 'T\u00c9RREO')
        15
    """
    # Use selector syntax: class + location
    selector = f"IfcWall, location=\"{storey_name}\""
    return count_entities(ifc_path, selector)


if __name__ == '__main__':
    ifc_file = './projects/fnde/ARQ.ifc'
    storey = 'T\u00c9RREO'
    total = count_walls_on_storey(ifc_file, storey)
    print(total)
