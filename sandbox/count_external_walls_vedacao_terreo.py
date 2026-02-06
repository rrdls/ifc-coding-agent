from typing import Optional
from skills.learned.quantities.scripts.count_entities_filtered import count_entities_filtered


def count_external_walls_vedacao(ifc_path: str) -> int:
    """Count external walls using material 'VEDAÇÃO EXTERNA' on storey 'TÉRREO'.

    Args:
        ifc_path (str): Path to the IFC file.

    Returns:
        int: Number of external walls that match the material and storey.

    Example:
        >>> count_external_walls_vedacao('./projects/fnde/ARQ.ifc')
        12
    """
    # Count both IfcWall and IfcWallStandardCase
    count_walls = count_entities_filtered(ifc_path, 'IfcWall, IfcWallStandardCase', material_name='VEDAÇÃO EXTERNA', storey_name='TÉRREO')
    return count_walls


if __name__ == '__main__':
    result = count_external_walls_vedacao('./projects/fnde/ARQ.ifc')
    print(result)
