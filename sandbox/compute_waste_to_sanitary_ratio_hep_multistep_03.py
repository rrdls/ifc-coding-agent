"""
Compute the ratio of waste terminals to sanitary terminals in a given IFC model.

This script provides a function `compute_waste_to_sanitary_ratio` which uses the
reusable `count_entities` function from skills.learned.quantities.scripts.count_entities.

The script prints the counts and the ratio as a float (waste / sanitary) or reports
that information is not available when a count is zero.
"""
from typing import Tuple
from skills.learned.quantities.scripts.count_entities import count_entities


def compute_waste_to_sanitary_ratio(ifc_path: str) -> Tuple[int, int, float]:
    """Compute counts for waste and sanitary terminals and their ratio.

    Args:
        ifc_path (str): Path to the IFC file.

    Returns:
        Tuple[int, int, float]: (waste_count, sanitary_count, ratio)
            - waste_count: Number of IfcWasteTerminal entities
            - sanitary_count: Number of IfcSanitaryTerminal entities
            - ratio: waste_count / sanitary_count (float). If sanitary_count is 0,
                     ratio will be float('inf') if waste_count > 0, or 0.0 if both
                     are zero.

    Example:
        >>> compute_waste_to_sanitary_ratio('./projects/fnde/HEP.ifc')
        (3, 6, 0.5)
    """
    waste_count = count_entities(ifc_path, 'IfcWasteTerminal')
    sanitary_count = count_entities(ifc_path, 'IfcSanitaryTerminal')

    if sanitary_count == 0:
        if waste_count == 0:
            ratio = 0.0
        else:
            ratio = float('inf')
    else:
        ratio = waste_count / sanitary_count

    return waste_count, sanitary_count, ratio


if __name__ == '__main__':
    ifc_file = './projects/fnde/HEP.ifc'
    waste_count, sanitary_count, ratio = compute_waste_to_sanitary_ratio(ifc_file)
    print(f"Waste terminals: {waste_count}")
    print(f"Sanitary terminals: {sanitary_count}")
    if ratio == float('inf'):
        print('Ratio (waste/sanitary): Infinity (sanitary_count is 0, waste_count > 0)')
    else:
        print(f"Ratio (waste/sanitary): {ratio}")
