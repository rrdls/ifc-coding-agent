from typing import Tuple
from skills.learned.quantities.scripts.count_entities import count_entities


def ratio_lightfixtures_to_boards(ifc_path: str) -> Tuple[int, int, str]:
    """Compute the counts and ratio of light fixtures to distribution boards in an IFC model.

    Args:
        ifc_path (str): Path to the IFC file.

    Returns:
        Tuple[int, int, str]: (num_light_fixtures, num_distribution_boards, ratio_string)
            - num_light_fixtures: count of IfcLightFixture entities
            - num_distribution_boards: count of IfcDistributionBoard entities
            - ratio_string: human-readable ratio "A:B" or special messages when one count is zero

    Example:
        >>> ratio_lightfixtures_to_boards('./projects/fnde/ELE.ifc')
        (120, 8, '15:1')
    """
    # Count IfcLightFixture
    num_lights = count_entities(ifc_path, 'IfcLightFixture')

    # Count IfcDistributionBoard (some IFCs may use IfcDistributionElement or IfcDistributionBoard)
    # Try exact class first
    num_boards = count_entities(ifc_path, 'IfcDistributionBoard')

    # If zero, also try a more generic class IfcDistributionElement to be safe
    if num_boards == 0:
        num_boards = count_entities(ifc_path, 'IfcDistributionElement')

    # Prepare ratio string
    if num_boards == 0 and num_lights == 0:
        ratio = 'No light fixtures and no distribution boards found in the model'
    elif num_boards == 0:
        ratio = 'Distribution boards not found in model (division by zero)'
    else:
        # Simplify ratio by integer division when possible
        from math import gcd
        g = gcd(num_lights, num_boards)
        a = num_lights // g
        b = num_boards // g
        ratio = f"{a}:{b}"

    return num_lights, num_boards, ratio


if __name__ == '__main__':
    import sys
    path = './projects/fnde/ELE.ifc'
    lights, boards, ratio = ratio_lightfixtures_to_boards(path)
    print(f"Light fixtures: {lights}")
    print(f"Distribution boards: {boards}")
    print(f"Ratio (lights:boards): {ratio}")
