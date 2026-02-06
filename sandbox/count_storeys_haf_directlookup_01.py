"""
Script to count building storeys (IfcBuildingStorey) in the HAF.ifc model.

This script uses the generic learned skill `count_entities` located in
`skills/learned/quantities/scripts/count_entities.py`.

It defines a function `count_building_storeys` with a full docstring and
executes it when run as a script, printing the result.
"""
from typing import Any
from skills.learned.quantities.scripts.count_entities import count_entities


def count_building_storeys(ifc_path: str) -> int:
    """Count the number of building storeys in the provided IFC model.

    Args:
        ifc_path (str): Path to the IFC file (e.g., './projects/fnde/HAF.ifc').

    Returns:
        int: Number of IfcBuildingStorey instances in the model.

    Example:
        >>> count_building_storeys('./projects/fnde/HAF.ifc')
        3
    """
    return count_entities(ifc_path, 'IfcBuildingStorey')


if __name__ == '__main__':
    model_path = './projects/fnde/HAF.ifc'
    total_storeys = count_building_storeys(model_path)
    print(total_storeys)
