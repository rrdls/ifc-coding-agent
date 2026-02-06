"""
Count building storeys in the ARQ.ifc model.

This script uses the reusable function `count_entities` from
skills.learned.quantities.scripts.count_entities to count
instances of IfcBuildingStorey.
"""
from typing import Any
from skills.learned.quantities.scripts.count_entities import count_entities


def count_building_storeys(ifc_path: str) -> int:
    """Count the number of IfcBuildingStorey entities in an IFC model.

    Args:
        ifc_path (str): Relative path to the IFC file (e.g., './projects/fnde/ARQ.ifc').

    Returns:
        int: Number of IfcBuildingStorey entities found in the model.

    Example:
        >>> count_building_storeys('./projects/fnde/ARQ.ifc')
        5
    """
    return count_entities(ifc_path, 'IfcBuildingStorey')


if __name__ == "__main__":
    ifc_file = './projects/fnde/ARQ.ifc'
    total = count_building_storeys(ifc_file)
    print(total)
