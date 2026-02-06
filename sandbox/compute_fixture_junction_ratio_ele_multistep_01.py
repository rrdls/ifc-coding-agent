"""
Compute ratio of light fixtures to junction boxes in the specified IFC model.

This script defines a function `ratio_lightfixtures_to_junctionboxes` which uses
the generic `count_entities` function from learned skills to count IfcLightFixture
and IfcJunctionBox entities and returns the ratio as a float and the raw counts.

Usage:
    python3 sandbox/compute_fixture_junction_ratio_ele_multistep_01.py
"""
from typing import Tuple
from skills.learned.quantities.scripts.count_entities import count_entities


def ratio_lightfixtures_to_junctionboxes(ifc_path: str) -> Tuple[float, int, int]:
    """Calculate the ratio of light fixtures to junction boxes in an IFC file.

    Args:
        ifc_path (str): Path to the IFC model file.

    Returns:
        Tuple[float, int, int]: A tuple containing:
            - ratio (float): light_fixtures_count / junction_boxes_count. If
              junction_boxes_count is zero, ratio will be float('inf').
            - light_fixtures_count (int): Number of IfcLightFixture entities.
            - junction_boxes_count (int): Number of IfcJunctionBox entities.

    Example:
        >>> ratio, lights, junctions = ratio_lightfixtures_to_junctionboxes('./projects/fnde/ELE.ifc')
        >>> print(ratio, lights, junctions)
        2.5 50 20
    """
    lights = count_entities(ifc_path, 'IfcLightFixture')
    junctions = count_entities(ifc_path, 'IfcJunctionBox')
    if junctions == 0:
        ratio = float('inf') if lights > 0 else 0.0
    else:
        ratio = lights / junctions
    return ratio, lights, junctions


if __name__ == '__main__':
    model_path = './projects/fnde/ELE.ifc'
    ratio, lights, junctions = ratio_lightfixtures_to_junctionboxes(model_path)
    if junctions == 0:
        ratio_str = 'infinite (no junction boxes found)' if lights > 0 else '0 (no fixtures and no junction boxes)'
    else:
        ratio_str = f"{ratio:.3f}"
    print(f"Light fixtures: {lights}")
    print(f"Junction boxes: {junctions}")
    print(f"Ratio (fixtures / junction boxes): {ratio_str}")
