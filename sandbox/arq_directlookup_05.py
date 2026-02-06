from skills.learned.properties.scripts.get_building_name import get_building_name


def query_building_name(ifc_path: str) -> str:
    """Query the IFC model for the building name and return a user-friendly message.

    Args:
        ifc_path (str): Path to the IFC file.

    Returns:
        str: The building name, or a message indicating the name is not available.

    Example:
        >>> query_building_name('./projects/fnde/ARQ.ifc')
        "Main Building"
    """
    name = get_building_name(ifc_path)
    if name:
        return name
    return "Information not available in the model"


if __name__ == '__main__':
    import sys
    path = './projects/fnde/ARQ.ifc'
    result = query_building_name(path)
    print(result)
