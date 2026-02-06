"""
Count entities of a specified IFC class in an IFC model filtered by a spatial location name (storey).

Purpose:
    Reusable function to count IFC entities of a given class located on a specific storey using
    ifcopenshell.util.selector filter syntax.

Args:
    ifc_path (str): Path to the IFC file (relative or absolute).
    entity_type (str): IFC class name to count (e.g., "IfcColumn").
    storey_name (str): Exact name of the storey/spatial element to filter by (e.g., "Térreo").

Returns:
    int: Number of matching entities found on the specified storey.

Example:
    >>> from skills.learned.quantities.scripts.count_entities_storey import count_entities_on_storey
    >>> count = count_entities_on_storey('./projects/fnde/EST.ifc', 'IfcColumn', 'Térreo')
    >>> print(count)
"""
from typing import Any
import ifcopenshell
import ifcopenshell.util.selector


def count_entities_on_storey(ifc_path: str, entity_type: str, storey_name: str) -> int:
    """Count entities of a specified IFC class on a given storey.

    Args:
        ifc_path: Path to the IFC file.
        entity_type: IFC class name to count (e.g., 'IfcColumn').
        storey_name: Name of the storey to filter by (exact match).

    Returns:
        Integer count of matching entities located on the specified storey.

    Example:
        >>> count_entities_on_storey('./projects/fnde/EST.ifc', 'IfcColumn', 'Térreo')
    """
    model = ifcopenshell.open(ifc_path)
    selector = f'{entity_type}, location="{storey_name}"'
    elements = ifcopenshell.util.selector.filter_elements(model, selector)
    return len(elements)
