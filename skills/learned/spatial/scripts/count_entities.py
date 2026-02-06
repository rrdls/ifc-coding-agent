import ifcopenshell
from typing import Any


def count_entities(ifc_path: str, entity_type: str) -> int:
    """Count entities of a specified IFC type in an IFC model.

    Purpose:
        Open an IFC file and count how many entities of the given IFC class exist
        (for example, "IfcWall", "IfcBuildingStorey").

    Args:
        ifc_path (str): Path to the IFC file.
        entity_type (str): IFC entity type to count (e.g., "IfcWall").

    Returns:
        int: Number of entities of the specified type found in the model.

    Example:
        >>> count_entities('./projects/fnde/EST.ifc', 'IfcBuildingStorey')
        5
    """
    model = ifcopenshell.open(ifc_path)
    entities = model.by_type(entity_type)
    return len(entities)
