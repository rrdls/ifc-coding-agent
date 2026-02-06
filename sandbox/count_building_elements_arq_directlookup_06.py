from skills.learned.quantities.scripts.count_entities import count_entities


def count_building_elements(ifc_path: str) -> int:
    """
    Count total building elements in the given IFC model.

    Purpose:
        Use the generic count_entities function to count all instances of IfcBuildingElement
        and its subtypes in the provided IFC file.

    Args:
        ifc_path (str): Path to the IFC file to query.

    Returns:
        int: Total number of building elements (IfcBuildingElement and subclasses).

    Example:
        >>> total = count_building_elements('./projects/fnde/ARQ.ifc')
        >>> print(total)
    """
    # IfcBuildingElement is an abstract supertype; selector supports querying by class
    return count_entities(ifc_path, 'IfcBuildingElement')


if __name__ == '__main__':
    import sys
    path = './projects/fnde/ARQ.ifc'
    total = count_building_elements(path)
    print(total)
