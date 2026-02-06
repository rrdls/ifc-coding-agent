"""
Find elements on a specific storey (building storey) with optional class and name filtering.

Purpose:
    Provide a reusable function to query IFC models for elements that are located on a
    given storey. Supports filtering by IFC class and by Name regex using the selector
    utility from IfcOpenShell.

Functions:
    find_elements_on_storey(ifc_path: str, storey_name: str, ifc_class: str | None = None, name_regex: str | None = None) -> list

Example:
    >>> find_elements_on_storey('./projects/fnde/HEP.ifc', 'COBERTURA', ifc_class='IfcFlowTreatmentDevice')

"""
from typing import List, Optional
import ifcopenshell
import ifcopenshell.util.selector


def find_elements_on_storey(ifc_path: str, storey_name: str, ifc_class: Optional[str] = None, name_regex: Optional[str] = None) -> List[object]:
    """
    Find elements located on a specified building storey.

    Args:
        ifc_path (str): Path to the IFC file (e.g., './projects/fnde/HEP.ifc').
        storey_name (str): The exact name of the IfcBuildingStorey to filter by (e.g., 'COBERTURA').
        ifc_class (Optional[str]): Optional IFC class to restrict results (e.g., 'IfcWall'). If None, defaults to 'IfcElement'.
        name_regex (Optional[str]): Optional regular expression to match the Name attribute (e.g., '/(?i)interceptor/').

    Returns:
        List[object]: A list of Ifc entity instances that match the filters. May be empty if no matches found.

    Example:
        >>> elems = find_elements_on_storey('./projects/fnde/HEP.ifc', 'COBERTURA', ifc_class='IfcFlowTreatmentDevice')
        >>> len(elems)
        0
    """
    model = ifcopenshell.open(ifc_path)

    base_class = ifc_class if ifc_class else 'IfcElement'

    # Build selector query parts
    parts = [base_class, f'location="{storey_name}"']
    if name_regex:
        # ensure regex is provided between slashes as required by selector syntax
        parts.append(f'Name={name_regex}')

    query = ', '.join(parts)

    elements = ifcopenshell.util.selector.filter_elements(model, query)
    return elements
