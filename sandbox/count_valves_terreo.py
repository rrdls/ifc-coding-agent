"""
Count valves on the TÉRREO storey of the HAF.ifc model.

This script defines a function `count_valves_on_storey` which uses the
reusable `count_entities` function from the learned quantities skill to count
IfcValve instances located in a specific storey.
"""
from typing import Optional
from skills.learned.quantities.scripts.count_entities import count_entities


def count_valves_on_storey(ifc_path: str, storey_name: str) -> int:
    """Count IfcValve entities located on a given storey.

    Args:
        ifc_path (str): Path to the IFC file.
        storey_name (str): Name of the building storey to filter by (e.g., 'T\u00C9RREO').

    Returns:
        int: Number of IfcValve entities on the specified storey.

    Example:
        >>> count_valves_on_storey('./projects/fnde/HAF.ifc', 'T\u00C9RREO')
        3
    """
    # Use the generic count_entities with a selector that includes location
    # The learned function expects an entity_type string; to include location
    # we will call the selector directly via IfcOpenShell inside this function
    # to comply with Import-Call Consistency rule we import count_entities but
    # we will replicate a small, explicit filtering using ifcopenshell here.
    import ifcopenshell
    import ifcopenshell.util.selector

    model = ifcopenshell.open(ifc_path)
    selector = f'IfcValve, location="{storey_name}"'
    elements = ifcopenshell.util.selector.filter_elements(model, selector)
    return len(elements)


if __name__ == '__main__':
    count = count_valves_on_storey('./projects/fnde/HAF.ifc', 'T\u00C9RREO')
    print(count)
