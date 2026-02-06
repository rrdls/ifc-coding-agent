"""
Compute the ratio of doors to windows in a given IFC model.

This script defines a function `doors_to_windows_ratio` which uses the
reusable `count_entities` function from the learned skills to count
IfcDoor and IfcWindow instances and returns the ratio as a float
(doors / windows). It prints counts and the ratio when executed.

Usage:
    python3 sandbox/compute_doors_windows_ratio_arq_multistep_03.py
"""
from typing import Tuple
from skills.learned.quantities.scripts.count_entities import count_entities


def doors_to_windows_ratio(ifc_path: str) -> Tuple[int, int, float]:
    """Compute counts and ratio of doors to windows in an IFC model.

    Args:
        ifc_path (str): Path to the IFC file.

    Returns:
        Tuple[int, int, float]: (num_doors, num_windows, ratio)
            - num_doors: Number of IfcDoor instances
            - num_windows: Number of IfcWindow instances
            - ratio: doors/windows as float. If num_windows == 0, ratio is
                     returned as float('inf') to indicate undefined/infinite.

    Example:
        >>> doors_to_windows_ratio('./projects/fnde/ARQ.ifc')
        (10, 5, 2.0)
    """
    num_doors = count_entities(ifc_path, 'IfcDoor')
    num_windows = count_entities(ifc_path, 'IfcWindow')
    if num_windows == 0:
        ratio = float('inf')
    else:
        ratio = num_doors / num_windows
    return num_doors, num_windows, ratio


if __name__ == '__main__':
    ifc_file = './projects/fnde/ARQ.ifc'
    doors, windows, ratio = doors_to_windows_ratio(ifc_file)
    print(f"Doors: {doors}")
    print(f"Windows: {windows}")
    if windows == 0:
        print("Ratio (doors/windows): undefined (no windows present)")
    else:
        print(f"Ratio (doors/windows): {ratio}")
