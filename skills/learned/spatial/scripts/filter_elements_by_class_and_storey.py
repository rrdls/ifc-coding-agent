"""
Filter elements by IFC class and building storey using IfcOpenShell selector.

Purpose:
    Query an IFC model for elements of one or more IFC classes filtered by
    the spatial location (building storey) name.

Functions:
    filter_elements_by_class_and_storey(ifc_path: str, class_filter: str, storey_name: str) -> list

Args:
    ifc_path (str): Path to the IFC file.
    class_filter (str): IFC class or selector string (e.g. "IfcJunctionBox" or
        "IfcJunctionBox, IfcDistributionElement"). This string is passed
        directly to ifcopenshell.util.selector.filter_elements, so it can
        include multiple classes separated by comma and other selector filters.
    storey_name (str): The name of the building storey to filter by (location).

Returns:
    List[dict]: A list of dictionaries for each matched element with keys:
        - "globalid" (str): element GlobalId
        - "ifctype" (str): element IFC type (e.g., "IfcJunctionBox")
        - "name" (str): element Name attribute (may be None)

Example:
    >>> filter_elements_by_class_and_storey('./projects/fnde/ELE.ifc', 'IfcJunctionBox', 'COBERTURA')
    [
        {"globalid": "1a2b3c...", "ifctype": "IfcJunctionBox", "name": "JB-01"}
    ]
"""
from typing import List, Dict
import ifcopenshell
import ifcopenshell.util.selector


def filter_elements_by_class_and_storey(ifc_path: str, class_filter: str, storey_name: str) -> List[Dict[str, str]]:
    """Query IFC model and return elements of given class located on a storey.

    Args:
        ifc_path (str): Path to the IFC file.
        class_filter (str): Selector string for class(es) (e.g. "IfcJunctionBox").
        storey_name (str): Storey name to filter by (location attribute).

    Returns:
        List[Dict[str, str]]: List of matched elements represented as dictionaries.

    Example:
        >>> filter_elements_by_class_and_storey('./projects/fnde/ELE.ifc', 'IfcJunctionBox', 'COBERTURA')
    """
    model = ifcopenshell.open(ifc_path)
    selector_string = f"{class_filter}, location=\"{storey_name}\""
    elements = ifcopenshell.util.selector.filter_elements(model, selector_string)

    results: List[Dict[str, str]] = []
    for e in elements:
        results.append({
            "globalid": getattr(e, 'GlobalId', None),
            "ifctype": e.is_a(),
            "name": getattr(e, 'Name', None)
        })
    return results
