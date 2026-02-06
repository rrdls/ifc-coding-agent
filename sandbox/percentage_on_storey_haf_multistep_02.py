from skills.learned.quantities.scripts.count_entities import count_entities

import ifcopenshell
import ifcopenshell.util.selector


def percentage_elements_on_storey(ifc_path: str, storey_name: str) -> float:
    """
    Calculate the percentage of IfcElement instances located on a given storey.

    Purpose:
        Open an IFC model, count total IfcElement instances and the subset whose
        spatial location (storey) matches the provided storey_name, then compute
        the percentage.

    Args:
        ifc_path (str): Path to the IFC file.
        storey_name (str): Name of the storey to filter by (e.g., "COBERTURA").

    Returns:
        float: Percentage (0-100) of IfcElement instances that are on the specified storey.

    Example:
        >>> percentage_elements_on_storey('./projects/fnde/HAF.ifc', 'COBERTURA')
        12.5
    """
    model = ifcopenshell.open(ifc_path)

    # Total elements: use the learned function
    total = count_entities(ifc_path, 'IfcElement')

    # Filter elements by location (storey) using selector syntax
    selector = f"IfcElement, location=\"{storey_name}\""
    elements_on_storey = ifcopenshell.util.selector.filter_elements(model, selector)
    count_on_storey = len(elements_on_storey)

    if total == 0:
        return 0.0
    return (count_on_storey / total) * 100.0


if __name__ == '__main__':
    import sys
    ifc_path = './projects/fnde/HAF.ifc'
    storey = 'COBERTURA'
    pct = percentage_elements_on_storey(ifc_path, storey)
    print(f"Elements on storey '{storey}': {pct:.6f}%")
