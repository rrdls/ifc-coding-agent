"""
Compute the ratio of railings to stairs in the specified IFC model.

This script defines a function `railings_to_stairs_ratio` which uses the
reusable `count_entities` function from skills.learned.quantities to count
IfcRailing and IfcStair elements and returns the ratio as a float.

Usage:
    python3 sandbox/compute_railings_to_stairs_ratio_arq_multistep_01.py
"""
from typing import Tuple
from skills.learned.quantities.scripts.count_entities import count_entities


def railings_to_stairs_ratio(ifc_path: str) -> Tuple[int, int, float]:
    """Count railings and stairs in an IFC model and compute the ratio (railings/stairs).

    Args:
        ifc_path (str): Path to the IFC file.

    Returns:
        Tuple[int, int, float]: A tuple with (railings_count, stairs_count, ratio).
            - railings_count (int): Number of IfcRailing entities found.
            - stairs_count (int): Number of IfcStair entities found.
            - ratio (float): railings_count / stairs_count if stairs_count > 0, else float('inf').

    Example:
        >>> railings_to_stairs_ratio('./projects/fnde/ARQ.ifc')
        (10, 5, 2.0)
    """
    railings = count_entities(ifc_path, 'IfcRailing')
    stairs = count_entities(ifc_path, 'IfcStair')
    if stairs == 0:
        ratio = float('inf')
    else:
        ratio = railings / stairs
    return railings, stairs, ratio


if __name__ == '__main__':
    ifc = './projects/fnde/ARQ.ifc'
    r, s, ratio = railings_to_stairs_ratio(ifc)
    print(f"Railings: {r}")
    print(f"Stairs: {s}")
    if s == 0:
        print("Ratio (railings/stairs): Infinity (no stairs found)")
    else:
        print(f"Ratio (railings/stairs): {ratio}")
