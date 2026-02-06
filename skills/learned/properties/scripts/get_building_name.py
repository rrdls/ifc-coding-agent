import ifcopenshell
from typing import Optional


def get_building_name(ifc_path: str) -> Optional[str]:
    """Get the Name of the first IfcBuilding in the IFC file.

    Purpose:
        Open an IFC file and return the Name attribute of the first IfcBuilding entity.

    Args:
        ifc_path (str): Path to the IFC file to read.

    Returns:
        Optional[str]: The Name of the first IfcBuilding found, or None if not present.

    Example:
        >>> get_building_name('./projects/fnde/ARQ.ifc')
        'Building A'
    """
    model = ifcopenshell.open(ifc_path)
    buildings = model.by_type('IfcBuilding')
    if not buildings:
        return None
    building = buildings[0]
    # Name may be None or empty
    name = getattr(building, 'Name', None)
    return name
