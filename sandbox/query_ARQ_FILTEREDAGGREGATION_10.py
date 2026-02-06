"""
Query script for ARQ_FILTEREDAGGREGATION_10
Lists all unique materials containing the word 'Pintura'
"""
from skills.learned.properties.scripts.find_materials_by_keyword import find_materials_by_keyword


def list_pintura_materials(ifc_path: str) -> list:
    """Find materials containing 'Pintura' in the IFC model.

    Args:
        ifc_path (str): Path to the IFC file.

    Returns:
        list: Sorted list of unique material names containing 'Pintura'.

    Example:
        >>> list_pintura_materials('./projects/fnde/ARQ.ifc')
        ['Pintura Branco']
    """
    return find_materials_by_keyword(ifc_path, 'Pintura')


if __name__ == '__main__':
    results = list_pintura_materials('./projects/fnde/ARQ.ifc')
    print(results)
