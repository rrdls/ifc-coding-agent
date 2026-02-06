"""
Reusable functions for extracting attribute and related type values from IFC entities.
"""
import ifcopenshell
from typing import Set, List


def get_unique_covering_types(ifc_path: str) -> Set[str]:
    """
    Collect unique covering type identifiers from an IFC model.

    This function searches for all IfcCovering instances and collects:
    - The value of the "PredefinedType" attribute (if present and not None)
    - The Name of any related IfcCoveringType referenced via IfcRelDefinesByType (IsTypedBy)

    Args:
        ifc_path (str): Path to the IFC file.

    Returns:
        Set[str]: A set of unique covering type strings found in the model.

    Example:
        >>> get_unique_covering_types('./projects/fnde/ARQ.ifc')
        {'CEILING', 'FLOORING', 'CLADDING'}
    """
    model = ifcopenshell.open(ifc_path)
    coverings = model.by_type('IfcCovering')
    types: Set[str] = set()

    for cov in coverings:
        # PredefinedType attribute (enum)
        try:
            predefined = getattr(cov, 'PredefinedType', None)
        except Exception:
            predefined = None
        if predefined:
            types.add(str(predefined))

        # Check IsTypedBy relationships for a related IfcCoveringType with a Name
        # Element may have attribute IsTypedBy which is a list of IfcRelDefinesByType
        typed_by = getattr(cov, 'IsTypedBy', []) or []
        for rel in typed_by:
            try:
                relating = getattr(rel, 'RelatingType', None)
                if relating is None:
                    continue
                name = getattr(relating, 'Name', None)
                if name:
                    types.add(str(name))
            except Exception:
                continue

    return types
