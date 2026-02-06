from typing import Any
from skills.learned.properties.scripts.get_property import get_property_value


def get_walls_fire_rating(ifc_path: str) -> Any:
    """Retrieve the fire resistance rating of walls from an IFC model.

    This function uses the learned helper `get_property_value` to query the first
    IfcWall element for common fire rating properties. It tries common pset keys
    and returns the first non-None value.

    Args:
        ifc_path (str): Path to the IFC file.

    Returns:
        Any: The fire rating value if found, otherwise None.

    Example:
        >>> get_walls_fire_rating('./projects/fnde/ARQ.ifc')
    """
    # Try common property keys for fire rating
    candidate_keys = [
        'Pset_WallCommon.FireRating',
        '/Pset_.*Common/.FireRating',
        'Pset_WallCommon.FireResistance',
        '/Pset_.*Common/.FireResistance',
        '/Pset_.*/.FireRating',
        '/Pset_.*/.FireResistance'
    ]

    for key in candidate_keys:
        value = get_property_value(ifc_path, 'IfcWall', key)
        if value is not None:
            return value
    return None


if __name__ == '__main__':
    result = get_walls_fire_rating('./projects/fnde/ARQ.ifc')
    print(result)
