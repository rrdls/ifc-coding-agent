from typing import Tuple
from skills.learned.quantities.scripts.count_entities import count_entities


def count_stairs_and_ramps(ifc_path: str) -> Tuple[int, int, int]:
    """Count stairs and ramps in the given IFC model and return totals.

    Purpose:
        Use the generic count_entities function to count IfcStair and IfcRamp
        entities in an IFC file, and compute the combined total.

    Args:
        ifc_path (str): Path to the IFC file.

    Returns:
        Tuple[int, int, int]: A tuple with (stair_count, ramp_count, total)

    Example:
        >>> count_stairs_and_ramps('./projects/fnde/ARQ.ifc')
        (5, 2, 7)
    """
    stair_count = count_entities(ifc_path, 'IfcStair')
    ramp_count = count_entities(ifc_path, 'IfcRamp')
    total = stair_count + ramp_count
    return stair_count, ramp_count, total


if __name__ == '__main__':
    import sys
    ifc_file = './projects/fnde/ARQ.ifc'
    stairs, ramps, total = count_stairs_and_ramps(ifc_file)
    print(f"Stairs: {stairs}")
    print(f"Ramps: {ramps}")
    print(f"Total (stairs + ramps): {total}")
