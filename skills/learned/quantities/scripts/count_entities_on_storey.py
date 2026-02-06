"""
Count entities of a specified IFC class in an IFC file, optionally filtered by storey (location).

Purpose:
    Provide a reusable function to count IFC entities (e.g., IfcWindow) in a model, with optional
    filtering by exact storey/location name.

Args:
    ifc_path (str): Path to the IFC file.
    entity_type (str): IFC entity class name to count (e.g., "IfcWindow").
    storey_name (str | None): Optional exact storey/location name to filter by. If None, counts across the whole model.

Returns:
    int: Number of matching entities found in the model.

Example:
    >>> from skills.learned.quantities.scripts.count_entities_on_storey import count_entities_on_storey
    >>> count = count_entities_on_storey('./projects/fnde/ARQ.ifc', 'IfcWindow', storey_name='T\u00c9RREO')
    >>> print(count)
"""
from typing import Optional
import ifcopenshell
import ifcopenshell.util.selector


def count_entities_on_storey(ifc_path: str, entity_type: str, storey_name: Optional[str] = None) -> int:
    """Count IFC entities of a given class, optionally restricted to a storey.

    Args:
        ifc_path: Path to the IFC file.
        entity_type: IFC class name (e.g., 'IfcWindow').
        storey_name: Optional exact storey/location name to filter by.

    Returns:
        Integer count of entities matching the query.

    Example:
        >>> count_entities_on_storey('./projects/fnde/ARQ.ifc', 'IfcWindow', storey_name='T\u00c9RREO')
    """
    model = ifcopenshell.open(ifc_path)

    if storey_name:
        selector = f'{entity_type}, location="{storey_name}"'
    else:
        selector = entity_type

    elements = ifcopenshell.util.selector.filter_elements(model, selector)
    return len(elements)
