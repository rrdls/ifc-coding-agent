"""
Generic utility to count IfcSpace instances matching a property selector.

This file implements a reusable function required by sandbox query scripts.
"""
import ifcopenshell
import ifcopenshell.util.selector
from typing import Optional


def count_spaces_with_property(ifc_path: str, pset_prop: str, expected_value: Optional[str] = None) -> int:
    """
    Count IfcSpace instances in an IFC model matching a property filter.

    Purpose:
        Open an IFC model and count IfcSpace entities that match a property-based
        selector expression. The function is generic and accepts either a
        complete selector fragment (e.g. "Pset_SpaceCommon.Waterproofing=TRUE")
        or a property name together with an expected_value which will be
        combined into a selector.

    Args:
        ifc_path (str): Path to the IFC file.
        pset_prop (str): Property selector fragment or property name. Examples:
            - "Pset_SpaceCommon.Waterproofing=TRUE"
            - "Pset_SpaceCommon.WallWaterproofing"
            - "/Pset_.*/.Waterproofing=TRUE"
        expected_value (Optional[str]): If pset_prop does not contain a
            comparison operator and expected_value is provided, the function
            will build a selector like "{pset_prop}={expected_value}".
            For boolean values pass 'TRUE' or 'FALSE' (strings).

    Returns:
        int: Number of IfcSpace entities matching the filter.

    Example:
        >>> count_spaces_with_property('./projects/fnde/ARQ.ifc',
        ...     'Pset_SpaceCommon.Waterproofing', 'TRUE')
        3
    """
    # Open model
    model = ifcopenshell.open(ifc_path)

    # Determine if pset_prop already contains a comparison operator
    comparators = ['=', '!=', '>', '<', '>=', '<=', '*=', '!*=']
    contains_comparator = any(op in pset_prop for op in comparators)

    if contains_comparator:
        selector_fragment = pset_prop
    else:
        if expected_value is None:
            # If no expected value, assume we want property defined (not NULL)
            selector_fragment = f"{pset_prop} != NULL"
        else:
            selector_fragment = f"{pset_prop}={expected_value}"

    selector_string = f"IfcSpace, {selector_fragment}"

    elements = ifcopenshell.util.selector.filter_elements(model, selector_string)
    return len(elements)
