import ifcopenshell
import unicodedata
from typing import List


def _normalize_text(text: str) -> str:
    """Normalize text for comparison: uppercase and remove diacritics.

    Args:
        text: Input string

    Returns:
        Normalized string
    """
    if text is None:
        return ""
    nfkd = unicodedata.normalize('NFKD', text)
    only_ascii = ''.join([c for c in nfkd if not unicodedata.combining(c)])
    return only_ascii.upper()


def count_elements_in_storey(ifc_path: str, storey_name: str) -> int:
    """Count number of elements contained in a building storey by name.

    Purpose:
        Open an IFC model and count distinct IfcElement instances that are
        contained (via IfcRelContainedInSpatialStructure) in the storey
        whose Name matches storey_name.

    Args:
        ifc_path: Path to the IFC file (str)
        storey_name: Name of the storey to search for (str). Matching is
            case-insensitive and diacritics-insensitive (e.g., TÉRREO == TERREO).

    Returns:
        int: Number of distinct elements found in the specified storey.

    Example:
        >>> count_elements_in_storey('./projects/fnde/HEP.ifc', 'TÉRREO')
        123
    """
    model = ifcopenshell.open(ifc_path)

    target_norm = _normalize_text(storey_name)

    # Find matching storeys by Name or LongName
    candidates: List[ifcopenshell.entity_instance] = []
    for s in model.by_type('IfcBuildingStorey'):
        name = getattr(s, 'Name', None)
        longname = getattr(s, 'LongName', None)
        if _normalize_text(name) == target_norm or _normalize_text(longname) == target_norm:
            candidates.append(s)

    if not candidates:
        # No storey found -> return 0 as per zero-hallucination (explicit absence)
        return 0

    # Collect related elements for all matching storeys
    elems_set = set()
    for rel in model.by_type('IfcRelContainedInSpatialStructure'):
        rel_struct = getattr(rel, 'RelatingStructure', None)
        if rel_struct in candidates:
            related = getattr(rel, 'RelatedElements', []) or []
            for e in related:
                # Use GlobalId if available to deduplicate, otherwise Python id
                gid = getattr(e, 'GlobalId', None)
                if gid:
                    elems_set.add(gid)
                else:
                    elems_set.add(id(e))

    return len(elems_set)
