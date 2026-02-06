"""
Compute percentage of external walls on a given storey (TÉRREO) in ARQ.ifc.

This improved script uses discovered Pset names and searches for property values
that indicate external walls (e.g., 'GENÉRICO - VEDAÇÃO EXTERNA').

Usage:
    python3 sandbox/percentage_external_walls_terreo_v2.py
"""
from typing import Tuple
from skills.learned.quantities.scripts.count_entities import count_entities
import ifcopenshell
import ifcopenshell.util.selector


def percentage_external_walls_on_storey(ifc_path: str, storey_name: str) -> Tuple[int, int, float]:
    """Calculate number and percentage of external walls on a specific storey, using Pset discovery.

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

    # Find all walls on the storey
    selector_storey = f"IfcWall, location=\"{storey_name}\""
    walls_on_storey = ifcopenshell.util.selector.filter_elements(model, selector_storey)
    total_on_storey = len(walls_on_storey)

    # If no walls found on storey, return zeros
    if total_on_storey == 0:
        return (0, 0, 0.0)

    # Strategy: iterate walls_on_storey and inspect their psets for values indicating external
    import ifcopenshell.util.element as util_element

    external_keywords = [
        'EXTERNA', 'VEDAÇÃO EXTERNA', 'externa', 'GENÉRICO - VEDAÇÃO EXTERNA', 'GENÉRICO - VEDACAO EXTERNA'
    ]

    external_count = 0
    for w in walls_on_storey:
        try:
            psets = util_element.get_psets(w)
        except Exception:
            psets = {}
        found = False
        for pset_name, props in psets.items():
            for prop_name, value in props.items():
                if value is None:
                    continue
                sval = str(value)
                for kw in external_keywords:
                    if kw.lower() in sval.lower():
                        found = True
                        break
                if found:
                    break
            if found:
                break
        if found:
            external_count += 1

    percentage = (external_count / total_on_storey * 100.0)
    return (total_on_storey, external_count, percentage)


if __name__ == '__main__':
    ifc_path = './projects/fnde/ARQ.ifc'
    storey = 'T\u00c9RREO'  # TÉRREO unicode
    total, external, pct = percentage_external_walls_on_storey(ifc_path, storey)
    print(f"Total walls on {storey}: {total}")
    print(f"External walls on {storey}: {external}")
    print(f"Percentage external: {pct:.2f}%")
