"""
Count electric distribution boards in the specified IFC model (ELE.ifc).

This script defines a function `count_distribution_boards` which uses the
generic `count_entities` function from learned skills to count instances of
IfcDistributionBoard in the given IFC file.

Run:
    python3 sandbox/count_distribution_boards_ele_directlookup_01.py
"""
from skills.learned.quantities.scripts.count_entities import count_entities


def count_distribution_boards(ifc_path: str) -> int:
    """Count electric distribution boards (IfcDistributionBoard) in an IFC file.

    Args:
        ifc_path (str): Path to the IFC file.

    Returns:
        int: Number of IfcDistributionBoard entities in the model.

    Example:
        >>> count_distribution_boards('./projects/fnde/ELE.ifc')
        3
    """
    return count_entities(ifc_path, 'IfcDistributionBoard')


if __name__ == '__main__':
    path = './projects/fnde/ELE.ifc'
    count = count_distribution_boards(path)
    print(count)
