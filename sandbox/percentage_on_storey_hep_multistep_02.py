from typing import Tuple
from skills.learned.quantities.scripts.count_entities import count_entities
import ifcopenshell
import ifcopenshell.util.selector


def percentage_on_storey(ifc_path: str, storey_name: str) -> Tuple[int, int, float]:
    """
    Calculate how many elements are located on a specific storey and the percentage relative to all elements.

    Args:
        ifc_path (str): Path to the IFC model file.
        storey_name (str): Name of the storey (e.g., "COBERTURA").

    Returns:
        Tuple[int, int, float]: A tuple with (count_on_storey, total_elements, percentage_on_storey)
            - count_on_storey (int): Number of elements assigned to the specified storey.
            - total_elements (int): Total number of elements in the model.
            - percentage_on_storey (float): Percentage of elements on the storey (0-100).

    Example:
        >>> percentage_on_storey('./projects/fnde/HEP.ifc', 'COBERTURA')
        (12, 120, 10.0)
    """
    # total elements (IfcElement covers most building elements)
    total = count_entities(ifc_path, 'IfcElement')

    model = ifcopenshell.open(ifc_path)
    # Use selector to filter by location (storey)
    selector_query = f'IfcElement, location="{storey_name}"'
    elems_on_storey = ifcopenshell.util.selector.filter_elements(model, selector_query)
    count_on_storey = len(elems_on_storey)

    percentage = (count_on_storey / total * 100.0) if total > 0 else 0.0
    return count_on_storey, total, percentage


if __name__ == '__main__':
    import sys
    path = './projects/fnde/HEP.ifc'
    storey = 'COBERTURA'
    count_on_storey, total, percentage = percentage_on_storey(path, storey)
    print(f"Elements on '{storey}': {count_on_storey}")
    print(f"Total elements: {total}")
    print(f"Percentage on '{storey}': {percentage:.2f}%")
