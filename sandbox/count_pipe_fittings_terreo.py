from typing import List
from skills.learned.quantities.scripts.count_entities import count_entities
import ifcopenshell
import ifcopenshell.util.selector


def count_pipe_fittings_on_storey(ifc_path: str, storey_name: str) -> int:
    """
    Count the number of pipe fittings (IfcFlowFitting / IfcFitting) located on a given storey.

    Args:
        ifc_path (str): Path to the IFC file.
        storey_name (str): Name of the storey (e.g., "T\u00c9RREO").

    Returns:
        int: Number of pipe fittings found on the specified storey.

    Example:
        >>> count_pipe_fittings_on_storey('./projects/fnde/HEP.ifc', 'T\u00c9RREO')
        10
    """
    model = ifcopenshell.open(ifc_path)
    # Find the storey entity by name (case-sensitive match as stored in IFC)
    storeys = [s for s in model.by_type('IfcBuildingStorey') if s.Name and s.Name.strip() == storey_name]
    if not storeys:
        # Try case-insensitive
        storeys = [s for s in model.by_type('IfcBuildingStorey') if s.Name and s.Name.strip().lower() == storey_name.lower()]
    if not storeys:
        return 0
    storey = storeys[0]

    # Use selector to find IfcFlowFitting or IfcFitting located in that storey
    # Selector supports location filtering via parent/storey name
    query = f"IfcFlowFitting, IfcFitting, location=\"{storey_name}\""
    try:
        elements = ifcopenshell.util.selector.filter_elements(model, query)
    except Exception:
        # Fallback: find all fittings and check containment
        fittings = list(model.by_type('IfcFlowFitting')) + list(model.by_type('IfcFitting'))
        elements = []
        # Check spatial containment via IfcRelContainedInSpatialStructure
        for rel in model.by_type('IfcRelContainedInSpatialStructure'):
            if rel.RelatingStructure == storey:
                for inst in rel.RelatedElements:
                    if inst in fittings:
                        elements.append(inst)
    return len(elements)


if __name__ == '__main__':
    count = count_pipe_fittings_on_storey('./projects/fnde/HEP.ifc', 'T\u00c9RREO')
    print(count)
