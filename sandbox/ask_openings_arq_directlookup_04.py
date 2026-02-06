"""
Script to check for IfcOpeningElement entities in the ARQ.ifc model (Query ID: ARQ_DIRECTLOOKUP_04).

This script uses the learned generic function 'count_entities' to count IfcOpeningElement instances.
"""
from typing import Any
from skills.learned.quantities.scripts.count_entities import count_entities


def count_openings(ifc_path: str) -> int:
    """Count IfcOpeningElement entities in an IFC model.

    Args:
        ifc_path (str): Path to the IFC file.

    Returns:
        int: Number of IfcOpeningElement entities found.

    Example:
        >>> count_openings('./projects/fnde/ARQ.ifc')
        3
    """
    return count_entities(ifc_path, 'IfcOpeningElement')


if __name__ == '__main__':
    path = './projects/fnde/ARQ.ifc'
    total = count_openings(path)
    print(total)
