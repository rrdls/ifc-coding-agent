"""
Count internal walls in ARQ.ifc

This script defines a function `count_internal_walls` that counts walls marked as internal
using the IfcOpenShell selector. It imports the reusable `count_entities` function from
skills.learned.quantities.scripts.count_entities.

Usage:
    python3 sandbox/count_internal_walls_arq_filter.py
"""
from typing import Any
from skills.learned.quantities.scripts.count_entities import count_entities


def count_internal_walls(ifc_path: str) -> int:
    """Count internal walls in an IFC model.

    Args:
        ifc_path (str): Path to the IFC file (e.g., './projects/fnde/ARQ.ifc').

    Returns:
        int: Number of internal walls found in the model. If no explicit property distinguishes
             internal from external walls, the function will attempt common pset selectors
             such as `Pset_WallCommon.IsExternal=False`.

    Example:
        >>> count_internal_walls('./projects/fnde/ARQ.ifc')
        12
    """
    # Common property used to mark external walls is Pset_WallCommon.IsExternal
    selector = 'IfcWall, Pset_WallCommon.IsExternal=False'
    return count_entities(ifc_path, selector)


if __name__ == "__main__":
    import sys
    path = './projects/fnde/ARQ.ifc'
    result = count_internal_walls(path)
    print(result)
