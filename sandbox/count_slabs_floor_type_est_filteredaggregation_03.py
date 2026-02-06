"""
Count slabs with PredefinedType = FLOOR in the given IFC model.

This script defines a function `count_slabs_with_predefinedtype_floor` which
opens an IFC file, filters IfcSlab elements with attribute PredefinedType equal
to 'FLOOR' (case-insensitive), and returns the count.

The top-level execution will print the result so that the testing harness can
capture the output.
"""
from typing import List
from skills.learned.quantities.scripts.count_entities import count_entities
import ifcopenshell
import ifcopenshell.util.selector


def count_slabs_with_predefinedtype_floor(ifc_path: str) -> int:
    """Count IfcSlab entities with PredefinedType equal to 'FLOOR'.

    Args:
        ifc_path (str): Path to the IFC file.

    Returns:
        int: Number of IfcSlab entities whose PredefinedType is 'FLOOR'.

    Example:
        >>> count_slabs_with_predefinedtype_floor('./projects/fnde/EST.ifc')
        10
    """
    model = ifcopenshell.open(ifc_path)
    # Use selector to find IfcSlab elements first
    slabs = ifcopenshell.util.selector.filter_elements(model, 'IfcSlab')
    count = 0
    for s in slabs:
        # Some slabs may not have PredefinedType attribute
        predefined = getattr(s, 'PredefinedType', None)
        if predefined is None:
            continue
        # Compare case-insensitive and support enum-like values
        if isinstance(predefined, str) and predefined.upper() == 'FLOOR':
            count += 1
        else:
            # If value is an enumeration object, try to stringify
            try:
                if str(predefined).upper() == 'FLOOR':
                    count += 1
            except Exception:
                pass
    return count


if __name__ == '__main__':
    result = count_slabs_with_predefinedtype_floor('./projects/fnde/EST.ifc')
    print(result)
