"""
Count total structural elements (beams + columns + footings) in the EST.ifc model.

This script defines a function `count_structural_elements` which uses the
learned skill `count_entities` to count IfcBeam, IfcColumn, and IfcFooting
and returns the total.

Run as:
    python3 sandbox/est_count_structural.py
"""
from typing import Tuple
from skills.learned.quantities.scripts.count_entities import count_entities


def count_structural_elements(ifc_path: str) -> Tuple[int, int, int, int]:
    """Count beams, columns, footings and total in the specified IFC model.

    Args:
        ifc_path (str): Path to the IFC file.

    Returns:
        Tuple[int, int, int, int]: A tuple with counts (n_beams, n_columns, n_footings, total).

    Example:
        >>> count_structural_elements('./projects/fnde/EST.ifc')
        (10, 8, 5, 23)
    """
    n_beams = count_entities(ifc_path, 'IfcBeam')
    n_columns = count_entities(ifc_path, 'IfcColumn')
    # Some models may use IfcFooting or IfcFootingElement; try IfcFooting first.
    n_footings = count_entities(ifc_path, 'IfcFooting')
    total = n_beams + n_columns + n_footings
    return n_beams, n_columns, n_footings, total


if __name__ == '__main__':
    ifc_file = './projects/fnde/EST.ifc'
    beams, columns, footings, total = count_structural_elements(ifc_file)
    print(f"Beams: {beams}")
    print(f"Columns: {columns}")
    print(f"Footings: {footings}")
    print(f"Total structural elements (beams+columns+footings): {total}")
