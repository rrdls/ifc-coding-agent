"""
Script to count How many IfcWall entities have material containing 'VEDAÇÃO'.

This script imports the generic learned function and provides a small CLI.
"""
from skills.learned.quantities.scripts.count_entities_by_material_contains import count_entities_by_material_contains


def count_walls_with_vedacao(ifc_path: str) -> int:
    """Count walls whose material contains 'VEDAÇÃO'.

    Args:
        ifc_path (str): Path to the IFC model file.

    Returns:
        int: Number of IfcWall entities with material containing 'VEDAÇÃO'.

    Example:
        >>> count_walls_with_vedacao('./projects/fnde/ARQ.ifc')
        5
    """
    return count_entities_by_material_contains(ifc_path, 'IfcWall', 'VEDAÇÃO')


if __name__ == '__main__':
    result = count_walls_with_vedacao('./projects/fnde/ARQ.ifc')
    print(result)
