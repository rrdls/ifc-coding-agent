"""
Count IFC entities of a given class whose material name contains a substring.

Purpose:
    Generic reusable function to count entities (e.g., IfcWall) whose associated
    material name contains a given substring. Uses IfcOpenShell selector syntax
    with the '*=' (contains) operator.

Args:
    ifc_path (str): Path to the IFC file.
    entity_type (str): IFC entity class to filter (e.g., "IfcWall").
    material_substring (str): Substring to search for in material names.

Returns:
    int: Number of matching entities found in the model.

Example:
    >>> count_entities_by_material_contains('./projects/fnde/ARQ.ifc', 'IfcWall', 'VEDAÇÃO')
    12
"""
from typing import Any
import ifcopenshell
import ifcopenshell.util.selector


def count_entities_by_material_contains(ifc_path: str, entity_type: str, material_substring: str) -> int:
    """Count entities of a given IFC class whose material name contains a substring.

    This function constructs a selector query using the material*=(contains) operator.

    Args:
        ifc_path: Path to the IFC model file.
        entity_type: IFC class name to filter (e.g., "IfcWall").
        material_substring: Substring to search for within material names.

    Returns:
        The integer count of matching entities.

    Example:
        >>> count_entities_by_material_contains('./projects/fnde/ARQ.ifc', 'IfcWall', 'VEDAÇÃO')
        12
    """
    model = ifcopenshell.open(ifc_path)
    # Use contains operator *= and quote the value to preserve accents/spaces
    selector_str = f'{entity_type}, material*="{material_substring}"'
    elements = ifcopenshell.util.selector.filter_elements(model, selector_str)
    return len(elements)
