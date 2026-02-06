"""
Check for junction boxes on the COBERTURA storey in the ELE.ifc model.

This script defines a function `junction_boxes_on_storey` which uses the
learned spatial helper to query IfcJunctionBox elements located on a given
storey name.

Usage:
    python3 sandbox/check_junction_boxes_cobertura.py
"""
from typing import List, Dict
from skills.learned.spatial.scripts.filter_elements_by_class_and_storey import filter_elements_by_class_and_storey


def junction_boxes_on_storey(ifc_path: str, storey_name: str) -> List[Dict[str, str]]:
    """Return junction boxes located on a specific building storey.

    Args:
        ifc_path (str): Path to the IFC file.
        storey_name (str): Name of the building storey to search (e.g., 'COBERTURA').

    Returns:
        List[Dict[str, str]]: A list of dictionaries for each found junction box with keys:
            - 'globalid': GlobalId of the element
            - 'ifctype': IFC type name
            - 'name': Name attribute (may be None)

    Example:
        >>> junction_boxes_on_storey('./projects/fnde/ELE.ifc', 'COBERTURA')
    """
    # Use IfcJunctionBox class; include distribution elements as backup
    selector = 'IfcJunctionBox, IfcDistributionElement'
    return filter_elements_by_class_and_storey(ifc_path, selector, storey_name)


if __name__ == '__main__':
    model_path = './projects/fnde/ELE.ifc'
    storey = 'COBERTURA'
    matches = junction_boxes_on_storey(model_path, storey)
    print(len(matches))
    for m in matches:
        print(m)
