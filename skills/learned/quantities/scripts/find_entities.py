import ifcopenshell
import ifcopenshell.util.selector
from typing import List


def find_entities(ifc_path: str, selectors: List[str]) -> List[object]:
    """
    Find and return IFC entities matching any of the selector class names or selector queries.

    Args:
        ifc_path (str): Path to the IFC file.
        selectors (List[str]): List of selector strings (e.g., ["IfcFlowTerminal", "IfcSanitaryTerminal"]).

    Returns:
        List[ifcopenshell.entity_instance.EntityInstance]: List of matching IFC entities. Duplicates are removed.

    Example:
        >>> entities = find_entities('./projects/fnde/HEP.ifc', ['IfcSanitaryTerminal', 'IfcWasteTerminal'])
    """
    model = ifcopenshell.open(ifc_path)
    found = []
    for sel in selectors:
        try:
            elements = ifcopenshell.util.selector.filter_elements(model, sel)
        except Exception:
            # Fallback: try class-based filter using model.by_type
            elements = model.by_type(sel) if hasattr(model, 'by_type') else []
        for e in elements:
            if e not in found:
                found.append(e)
    return found
