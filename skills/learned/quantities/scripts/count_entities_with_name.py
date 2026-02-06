"""
Count entities of a given IFC class that have a non-empty name (or other text attribute).

Purpose:
    Provide a reusable function to count IFC entities by class where a specified
    text attribute (by default 'Name') is present and not empty.

Args:
    ifc_path (str): Path to the IFC file to open.
    entity_type (str): IFC entity class name to filter, e.g. "IfcWall" or "IfcJunctionBox".
    name_attribute (str): The attribute to check for a non-empty string (default: "Name").

Returns:
    int: Number of entities of the given class that have a non-empty specified attribute.

Example:
    >>> from skills.learned.quantities.scripts.count_entities_with_name import count_entities_with_name
    >>> count = count_entities_with_name('./projects/fnde/ELE.ifc', 'IfcJunctionBox')
    >>> print(count)
"""
from typing import Any
import ifcopenshell


def count_entities_with_name(ifc_path: str, entity_type: str, name_attribute: str = "Name") -> int:
    """Count entities of a given IFC class that have a non-empty name-like attribute.

    Args:
        ifc_path (str): Path to the IFC file to open.
        entity_type (str): IFC entity class name to filter, e.g. "IfcWall" or "IfcJunctionBox".
        name_attribute (str): The attribute to check for a non-empty string (default: "Name").

    Returns:
        int: Number of entities of the given class that have a non-empty specified attribute.

    Example:
        >>> count_entities_with_name('./projects/fnde/ELE.ifc', 'IfcJunctionBox')
    """
    model = ifcopenshell.open(ifc_path)
    # Get all entities of this type
    entities = model.by_type(entity_type)
    count = 0
    for e in entities:
        # Some IFC attributes can be None or empty string. Check safely.
        val = getattr(e, name_attribute, None)
        if val is None:
            continue
        # If attribute is a string, strip and check length
        try:
            if isinstance(val, str) and val.strip() != "":
                count += 1
            # If it's an IfcLabel or other object with .wrappedValue (unlikely), try str()
            elif not isinstance(val, str) and str(val).strip() != "":
                count += 1
        except Exception:
            # Be conservative: only count when we can confirm non-empty
            continue
    return count
