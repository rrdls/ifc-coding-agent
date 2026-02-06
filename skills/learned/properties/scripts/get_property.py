"""
Reusable function to get a property value from the first element of a given type in an IFC model.

Purpose:
    Open an IFC model and retrieve a property value using selector keys.

Functions:
    get_property_value(ifc_path: str, element_type: str, property_key: str) -> object

Args:
    ifc_path (str): Path to the IFC file.
    element_type (str): IFC entity type to search (e.g., "IfcWall").
    property_key (str): Selector key for the property (e.g., "Pset_WallCommon.FireRating" or "/Pset_.*Common/.FireRating").

Returns:
    object: The property value if found, otherwise None.

Example:
    >>> from skills.learned.properties.scripts.get_property import get_property_value
    >>> get_property_value('./projects/fnde/ARQ.ifc', 'IfcWall', '/Pset_.*Common/.FireRating')
"""
from typing import Any
import ifcopenshell
import ifcopenshell.util.selector


def get_property_value(ifc_path: str, element_type: str, property_key: str) -> Any:
    """Open an IFC model and retrieve a property value from the first element of the given type.

    Args:
        ifc_path (str): Path to the IFC file.
        element_type (str): IFC entity type to search (e.g., "IfcWall").
        property_key (str): Selector key for the property (e.g., "Pset_WallCommon.FireRating" or "/Pset_.*Common/.FireRating").

    Returns:
        Any: The property value if found, otherwise None.

    Example:
        >>> get_property_value('./projects/fnde/ARQ.ifc', 'IfcWall', '/Pset_.*Common/.FireRating')
    """
    model = ifcopenshell.open(ifc_path)
    elements = model.by_type(element_type)
    if not elements:
        return None
    element = elements[0]
    value = ifcopenshell.util.selector.get_element_value(element, property_key)
    return value
