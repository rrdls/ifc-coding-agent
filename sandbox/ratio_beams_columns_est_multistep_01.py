"""
Script to compute the ratio of beams to columns in the EST.ifc model.

This script defines a function `ratio_beams_to_columns` that uses the
reusable `count_entities` function from skills.learned.quantities.scripts.

Run: python3 sandbox/ratio_beams_columns_est_multistep_01.py
"""
from typing import Tuple
from skills.learned.quantities.scripts.count_entities import count_entities


def ratio_beams_to_columns(ifc_path: str) -> Tuple[int, int, float]:
    """Compute counts and ratio of IfcBeam to IfcColumn in an IFC model.

    Args:
        ifc_path (str): Path to the IFC file.

    Returns:
        Tuple[int, int, float]: A tuple with (beam_count, column_count, ratio).
            - beam_count: number of IfcBeam entities
            - column_count: number of IfcColumn entities
            - ratio: beam_count / column_count as float. If column_count is 0,
              ratio will be float('inf') to indicate undefined/infinite ratio.

    Example:
        >>> ratio_beams_to_columns('./projects/fnde/EST.ifc')
        (10, 5, 2.0)

    """
    beams = count_entities(ifc_path, 'IfcBeam')
    columns = count_entities(ifc_path, 'IfcColumn')
    if columns == 0:
        ratio = float('inf')
    else:
        ratio = beams / columns
    return beams, columns, ratio


if __name__ == '__main__':
    ifc = './projects/fnde/EST.ifc'
    b, c, r = ratio_beams_to_columns(ifc)
    print(f"Beams: {b}")
    print(f"Columns: {c}")
    if r == float('inf'):
        print("Ratio (beams/columns): Infinity (no columns found)")
    else:
        print(f"Ratio (beams/columns): {r}")
