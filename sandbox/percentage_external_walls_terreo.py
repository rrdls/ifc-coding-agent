"""
Compute percentage of external walls on a given storey (TÉRREO) in ARQ.ifc.

This script defines a function `percentage_external_walls_on_storey` that counts walls
on a named storey and those flagged as external, then computes the percentage.

Usage:
    python3 sandbox/percentage_external_walls_terreo.py
"""
from typing import Tuple
from skills.learned.quantities.scripts.count_entities import count_entities
import ifcopenshell
import ifcopenshell.util.selector


def percentage_external_walls_on_storey(ifc_path: str, storey_name: str) -> Tuple[int, int, float]:
    """Calculate number and percentage of external walls on a specific storey.

    Args:
        ifc_path (str): Path to the IFC file.
        storey_name (str): Name of the storey as stored in IFC (e.g., 'TÉRREO').

    Returns:
        A tuple with (total_walls, external_walls, percentage_external) where percentage is
        a float between 0 and 100. If total_walls is 0, percentage_external will be 0.0.

    Example:
        >>> percentage_external_walls_on_storey('./projects/fnde/ARQ.ifc', 'TÉRREO')
        (100, 40, 40.0)
    """
    model = ifcopenshell.open(ifc_path)

    # Count total walls on the specified storey using selector location
    total_walls = count_entities(ifc_path, 'IfcWall')

    # Use selector to find walls located on the given storey
    selector_storey = f"IfcWall, location=\"{storey_name}\""
    walls_on_storey = ifcopenshell.util.selector.filter_elements(model, selector_storey)
    total_on_storey = len(walls_on_storey)

    # Find walls on the storey that are external. Common property: Pset_WallCommon.IsExternal
    selector_external = f"IfcWall, location=\"{storey_name}\", Pset_WallCommon.IsExternal=true"
    external_walls = ifcopenshell.util.selector.filter_elements(model, selector_external)
    external_on_storey = len(external_walls)

    # If the Pset property search returned zero but walls exist, attempt common alternative values (True/1/'Yes')
    if external_on_storey == 0 and total_on_storey > 0:
        # Try capitalized True
        selector_external_alt = f"IfcWall, location=\"{storey_name}\", Pset_WallCommon.IsExternal=True"
        external_walls_alt = ifcopenshell.util.selector.filter_elements(model, selector_external_alt)
        external_on_storey = len(external_walls_alt)

    percentage = (external_on_storey / total_on_storey * 100.0) if total_on_storey > 0 else 0.0
    return (total_on_storey, external_on_storey, percentage)


if __name__ == '__main__':
    ifc_path = './projects/fnde/ARQ.ifc'
    storey = 'T\u00c9RREO'  # TÉRREO unicode
    total, external, pct = percentage_external_walls_on_storey(ifc_path, storey)
    print(f"Total walls on {storey}: {total}")
    print(f"External walls on {storey}: {external}")
    print(f"Percentage external: {pct:.2f}%")
