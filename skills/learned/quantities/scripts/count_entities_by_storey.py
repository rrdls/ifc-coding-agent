import ifcopenshell
import ifcopenshell.util.selector
from typing import Any

def count_entities_by_storey(ifc_path: str, entity_type: str, storey_name: str) -> int:
    """
    Count entities of a given IFC class located on a specific storey (location filter).

    Args:
        ifc_path (str): Path to the IFC file.
        entity_type (str): IFC entity class name to count (e.g., "IfcWall", "IfcSanitaryTerminal").
        storey_name (str): Name of the storey/location to filter by (exact match, case-sensitive).

    Returns:
        int: Number of entities of the specified class found on the given storey.

    Example:
        >>> count_entities_by_storey("./projects/fnde/HAF.ifc", "IfcSanitaryTerminal", "TÉRREO")
        12
    """
    model = ifcopenshell.open(ifc_path)
    # Build selector query using location filter; use quotes around storey name to allow spaces and special chars
    query = f"{entity_type}, location=\"{storey_name}\""
    elements = ifcopenshell.util.selector.filter_elements(model, query)
    return len(elements)
