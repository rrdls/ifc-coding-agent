"""
Count ramps in the ARQ.ifc model.

This script defines count_ramps which uses the learned count_entities function.
"""
from typing import Any
from skills.learned.quantities.scripts.count_entities import count_entities


def count_ramps(ifc_path: str) -> int:
    """
    Count ramp elements (IfcRamp) in the given IFC model.

    Args:
        ifc_path (str): Path to the IFC file to open.

    Returns:
        int: Number of IfcRamp entities in the model.

    Example:
        >>> count_ramps('./projects/fnde/ARQ.ifc')
        3
    """
    return count_entities(ifc_path, 'IfcRamp')


if __name__ == '__main__':
    import sys
    path = './projects/fnde/ARQ.ifc'
    count = count_ramps(path)
    print(count)
