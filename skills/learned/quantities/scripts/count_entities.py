"""
Count entities of a specified IFC class in an IFC model.

Purpose:
    Provide a reusable function to count entities (e.g., IfcWall) in an IFC file using IfcOpenShell.

Args:
    ifc_path (str): Path to the IFC file.
    entity_type (str): IFC entity type name to count (e.g., "IfcWall").

Returns:
    int: Number of entities matching the specified type.

Example:
    >>> count_entities('./projects/fnde/ARQ.ifc', 'IfcWall')
    42
"""
from typing import Any
import ifcopenshell
import ifcopenshell.util.selector


def count_entities(ifc_path: str, entity_type: str) -> int:
    """Count entities of a specified IFC class in an IFC model.

    Args:
        ifc_path (str): Path to the IFC file.
        entity_type (str): IFC entity type name to count (e.g., "IfcWall").

    Returns:
        int: Number of entities matching the specified type.

    Example:
        >>> count_entities('./projects/fnde/ARQ.ifc', 'IfcWall')
        42
    """
    model = ifcopenshell.open(ifc_path)
    elements = ifcopenshell.util.selector.filter_elements(model, entity_type)
    return len(elements)
