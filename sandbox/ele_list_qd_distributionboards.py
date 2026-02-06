"""
Script: ele_list_qd_distributionboards.py

Purpose:
    List all distribution board names that contain 'QD' in their Name attribute
    from the provided IFC model.

This script imports the reusable function `find_entities_by_name` from the
learned skills and executes it against ./projects/fnde/ELE.ifc.
"""
from typing import List
from skills.learned.properties.scripts.find_entities_by_name import find_entities_by_name


def list_qd_distribution_boards(ifc_path: str) -> List[str]:
    """Return distribution board names containing 'QD'.

    Args:
        ifc_path (str): Path to the IFC file.

    Returns:
        List[str]: Names of distribution board entities that contain 'QD'.

    Example:
        >>> list_qd_distribution_boards('./projects/fnde/ELE.ifc')
        ['QD01', 'QD-AB-02']
    """
    # Try the common possible entity names. Some schemas use IfcElectricDistributionBoard.
    results: List[str] = []
    for et in ('IfcDistributionBoard', 'IfcElectricDistributionBoard'):
        try:
            res = find_entities_by_name(ifc_path, et, 'QD')
        except Exception:
            res = []
        for r in res:
            if r not in results:
                results.append(r)
    return results


if __name__ == '__main__':
    results = list_qd_distribution_boards('./projects/fnde/ELE.ifc')
    print(results)
