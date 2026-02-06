"""
Script to count walls in ARQ.ifc that use a specific material.

This script imports the generic learned function `count_entities_by_material`
and runs it for the query material.
"""
from skills.learned.quantities.scripts.count_entities_by_material import count_entities_by_material


def count_walls_with_material(ifc_path: str, material_name: str) -> int:
    """Count IfcWall and IfcWallStandardCase entities that use a given material.

    Args:
        ifc_path: Path to the IFC file.
        material_name: Exact name of the material to match.

    Returns:
        Integer count of matching wall entities.

    Example:
        >>> count_walls_with_material('./projects/fnde/ARQ.ifc', 'TIJOLO - MACIÇO 5x10x20')
        12
    """
    # Try both IfcWall and IfcWallStandardCase by running two queries and summing.
    count_wall = count_entities_by_material(ifc_path, 'IfcWall', material_name)
    count_wall_std = count_entities_by_material(ifc_path, 'IfcWallStandardCase', material_name)
    return count_wall + count_wall_std


if __name__ == '__main__':
    model_path = './projects/fnde/ARQ.ifc'
    mat = 'TIJOLO - MACIÇO 5x10x20'
    total = count_walls_with_material(model_path, mat)
    print(total)
