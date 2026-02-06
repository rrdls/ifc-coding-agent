"""
Script to count IfcWall elements that use materials containing the string 'TIJOLO'.

This script imports the generic count_entities function from skills.learned.quantities.scripts.count_entities
and uses IfcOpenShell selector syntax with the '*=' operator (contains).

Usage:
    python3 sandbox/count_walls_with_tijolo.py
"""
from typing import Any
from skills.learned.quantities.scripts.count_entities import count_entities


def count_walls_with_material_tijolo(ifc_path: str) -> int:
    """Count IfcWall elements whose associated material name contains 'TIJOLO'.

    Args:
        ifc_path (str): Path to the IFC file.

    Returns:
        int: Number of IfcWall elements with material names containing 'TIJOLO'.

    Example:
        >>> count_walls_with_material_tijolo('./projects/fnde/ARQ.ifc')
        10
    """
    # Use selector: class IfcWall and material contains TIJOLO (case-sensitive as selector is literal)
    selector = 'IfcWall, material*=TIJOLO'
    return count_entities(ifc_path, selector)


if __name__ == '__main__':
    ifc_file = './projects/fnde/ARQ.ifc'
    result = count_walls_with_material_tijolo(ifc_file)
    print(result)
