"""
Count light fixtures in the ELE.ifc model.

This script defines a function `count_light_fixtures` that counts instances
of IfcLightFixture and IfcLamp classes (common representations for lighting)
in the provided IFC file and prints the result.
"""
from typing import Any
from skills.learned.quantities.scripts.count_entities import count_entities


def count_light_fixtures(ifc_path: str) -> int:
    """
    Count light fixtures in an IFC model.

    Args:
        ifc_path (str): Path to the IFC (.ifc) file.

    Returns:
        int: Total number of light fixtures found (IfcLightFixture + IfcLamp).

    Example:
        >>> count_light_fixtures('./projects/fnde/ELE.ifc')
        10
    """
    # Count both IfcLightFixture and IfcLamp as some models use one or the other
    count_fixture = count_entities(ifc_path, 'IfcLightFixture')
    count_lamp = count_entities(ifc_path, 'IfcLamp')
    return count_fixture + count_lamp


if __name__ == '__main__':
    total = count_light_fixtures('./projects/fnde/ELE.ifc')
    print(total)
