"""
find_entities_by_name

Reusable helper to find entity names that contain a given substring in an IFC model.

Purpose:
    Search an IFC file for entities of a given IFC class and return the Name values
    of those entities that contain the provided substring.

Args:
    ifc_path (str): Path to the IFC file.
    entity_type (str): IFC entity type to search for (e.g., "IfcWall", "IfcDistributionBoard").
    substring (str): Case-sensitive substring to match inside the entity Name.

Returns:
    List[str]: A list of matching Name strings (duplicates removed). If an entity has no
               Name or no matches are found, it is ignored and an empty list may be returned.

Example:
    >>> from skills.learned.properties.scripts.find_entities_by_name import find_entities_by_name
    >>> find_entities_by_name('./projects/fnde/ELE.ifc', 'IfcDistributionBoard', 'QD')
    ['QD01', 'QD-AB-02']
"""
from typing import List
import ifcopenshell


def find_entities_by_name(ifc_path: str, entity_type: str, substring: str) -> List[str]:
    """Find entity Name values containing a substring.

    Args:
        ifc_path (str): Path to the IFC file.
        entity_type (str): IFC entity type to search for (e.g., "IfcDistributionBoard").
        substring (str): Case-sensitive substring to match inside the entity Name.

    Returns:
        List[str]: List of matching Name values (duplicates removed).

    Example:
        >>> find_entities_by_name('./projects/fnde/ELE.ifc', 'IfcDistributionBoard', 'QD')
        ['QD01', 'QD-AB-02']
    """
    model = ifcopenshell.open(ifc_path)
    matches = []
    for ent in model.by_type(entity_type):
        name = getattr(ent, 'Name', None)
        if name and substring in name:
            matches.append(name)
    # Remove duplicates while preserving order
    seen = set()
    unique = []
    for v in matches:
        if v not in seen:
            unique.append(v)
            seen.add(v)
    return unique
