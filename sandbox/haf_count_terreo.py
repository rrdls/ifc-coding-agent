from typing import Any
from skills.learned.quantities.scripts.count_entities_on_storey import count_entities_on_storey


def count_elements_on_terreo(ifc_path: str) -> int:
    """Count all IFC elements located on the storey named 'TÉRREO'.

    Purpose:
        Use the learned generic function `count_entities_on_storey` to count all
        instances of IfcElement that are located on the building storey named
        'TÉRREO' in the given IFC model.

    Args:
        ifc_path (str): Path to the IFC file.

    Returns:
        int: Number of elements located on the 'TÉRREO' storey. Returns 0 if
             the storey is not found or no elements are present.

    Example:
        >>> count_elements_on_terreo('./projects/fnde/HAF.ifc')
        42
    """
    # The learned function expects an entity_type and optional storey_name
    return count_entities_on_storey(ifc_path, 'IfcElement', storey_name='TÉRREO')


if __name__ == '__main__':
    import sys
    path = './projects/fnde/HAF.ifc'
    result = count_elements_on_terreo(path)
    print(result)
