"""
Count walls in the ARQ.ifc model using the generic count_entities function.

This script defines a function `count_walls` that imports and calls the
`count_entities` function from the learned skills and prints the result when run
as a script.
"""
from typing import Any
from skills.learned.quantities.scripts.count_entities import count_entities


def count_walls(ifc_path: str) -> int:
    """Count IfcWall entities in the given IFC model.

    Args:
        ifc_path (str): Path to the IFC file.

    Returns:
        int: Number of IfcWall instances in the model.

    Example:
        >>> count_walls('./projects/fnde/ARQ.ifc')
        42
    """
    return count_entities(ifc_path, 'IfcWall')


if __name__ == '__main__':
    import sys
    path = './projects/fnde/ARQ.ifc'
    result = count_walls(path)
    print(result)
