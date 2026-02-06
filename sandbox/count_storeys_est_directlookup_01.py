from skills.learned.spatial.scripts.count_entities import count_entities


def count_building_storeys(ifc_path: str) -> int:
    """Count the number of IfcBuildingStorey entities in the IFC model.

    Args:
        ifc_path (str): Path to the IFC (.ifc) model file.

    Returns:
        int: Number of building storeys (IfcBuildingStorey) found in the model.

    Example:
        >>> count_building_storeys('./projects/fnde/EST.ifc')
        3
    """
    return count_entities(ifc_path, 'IfcBuildingStorey')


if __name__ == '__main__':
    import sys
    path = './projects/fnde/EST.ifc'
    result = count_building_storeys(path)
    print(result)
