"""
Compute percentage of walls that are internal in the given IFC model.

This script defines a function `percentage_internal_walls` which counts total
walls and internal walls using IfcOpenShell selector filters and returns the
percentage of walls that are internal.

Usage:
    python3 sandbox/percentage_internal_walls_arq_multistep_06.py
"""
from typing import Tuple
from skills.learned.quantities.scripts.count_entities import count_entities
import ifcopenshell
import ifcopenshell.util.selector


def percentage_internal_walls(ifc_path: str) -> Tuple[int, int, float]:
    """Calculate total walls, internal walls, and percentage internal.

    Args:
        ifc_path (str): Path to the IFC file.

    Returns:
        Tuple[int, int, float]: (total_walls, internal_walls, percent_internal)
            - total_walls: total number of IfcWall entities found
            - internal_walls: number of walls classified as internal
            - percent_internal: percentage (0-100) of walls that are internal

    Example:
        >>> percentage_internal_walls('./projects/fnde/ARQ.ifc')
        (100, 40, 40.0)
    """
    # Use the generic count function for total walls (covers IfcWall types)
    total_walls = count_entities(ifc_path, 'IfcWall')

    # Open model and use selector to find walls with IsExternal = FALSE or Name/Function indicating internal
    model = ifcopenshell.open(ifc_path)

    # Try common patterns:
    # 1) IfcWall with attribute 'IsExternal' defined in IfcWall (not common)
    # 2) Property set: Pset_WallCommon.IsExternal = FALSE
    # 3) Some models use External/Internal in 'Pset_SomeCommon.External' or other psets
    # We'll search for walls with Pset_WallCommon.IsExternal = FALSE first.

    selector_query = 'IfcWall, Pset_WallCommon.IsExternal=FALSE'
    internal_walls = ifcopenshell.util.selector.filter_elements(model, selector_query)
    count_internal = len(internal_walls)

    # If no results, try alternative: IsExternal != TRUE (covers missing explicit FALSE)
    if count_internal == 0:
        selector_query2 = 'IfcWall, /Pset_.*Wall.*/.IsExternal != TRUE'
        try:
            internal_walls2 = ifcopenshell.util.selector.filter_elements(model, selector_query2)
            count_internal = len(internal_walls2)
        except Exception:
            # Fallback: try property name containing 'External' = FALSE
            selector_query3 = 'IfcWall, /Pset_.*/.*/External=FALSE'
            try:
                internal_walls3 = ifcopenshell.util.selector.filter_elements(model, selector_query3)
                count_internal = len(internal_walls3)
            except Exception:
                count_internal = 0

    percent_internal = (count_internal / total_walls * 100) if total_walls > 0 else 0.0
    return total_walls, count_internal, percent_internal


if __name__ == '__main__':
    ifc_path = './projects/fnde/ARQ.ifc'
    total, internal, percent = percentage_internal_walls(ifc_path)
    print(f"Total walls: {total}")
    print(f"Internal walls (by Pset_WallCommon.IsExternal=FALSE or alternatives): {internal}")
    print(f"Percentage internal: {percent:.2f}%")
