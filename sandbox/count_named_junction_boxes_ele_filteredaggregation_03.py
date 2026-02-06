"""
Count named junction boxes in the ELE.ifc model.

This script defines a function `count_named_junction_boxes` which uses the
reusable learned function `count_entities_with_name` to count IfcJunctionBox
entities that have a non-empty Name attribute.

Usage:
    python3 sandbox/count_named_junction_boxes_ele_filteredaggregation_03.py
"""
from skills.learned.quantities.scripts.count_entities_with_name import count_entities_with_name


def count_named_junction_boxes(ifc_path: str) -> int:
    """Count IfcJunctionBox entities that have a named identifier (Name attribute).

    Args:
        ifc_path (str): Path to the IFC file.

    Returns:
        int: Number of IfcJunctionBox entities with a non-empty Name attribute.

    Example:
        >>> count_named_junction_boxes('./projects/fnde/ELE.ifc')
    """
    return count_entities_with_name(ifc_path, 'IfcJunctionBox', 'Name')


if __name__ == '__main__':
    import sys
    path = './projects/fnde/ELE.ifc'
    if len(sys.argv) > 1:
        path = sys.argv[1]
    result = count_named_junction_boxes(path)
    print(result)
