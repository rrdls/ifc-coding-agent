from typing import Any
from skills.learned.quantities.scripts.count_entities import count_entities


def count_distribution_elements(ifc_path: str) -> int:
    """Count all distribution elements in an IFC model (IfcDistributionElement).

    Args:
        ifc_path (str): Path to the IFC file.

    Returns:
        int: Total number of IfcDistributionElement instances in the model.

    Example:
        >>> count_distribution_elements('./projects/fnde/ELE.ifc')
        123
    """
    return count_entities(ifc_path, 'IfcDistributionElement')


if __name__ == '__main__':
    import sys
    path = './projects/fnde/ELE.ifc'
    total = count_distribution_elements(path)
    print(total)
