"""
Script to determine if there are any IfcPile entities on the 'Cobertura' storey.

This script imports the reusable function from skills/learned and executes it.
"""
from typing import List, Dict
from skills.learned.relationships.scripts.list_entities_in_storey import list_entities_in_storey


def piles_on_cobertura(ifc_path: str) -> List[Dict[str, str]]:
    """
    Check for IfcPile entities located on the 'Cobertura' building storey.

    Args:
        ifc_path (str): Path to the IFC model file.

    Returns:
        List[Dict[str, str]]: List of found piles with basic identifiers.

    Example:
        >>> piles = piles_on_cobertura('./projects/fnde/EST.ifc')
        >>> print(len(piles))
        0
    """
    return list_entities_in_storey(ifc_path, 'Cobertura', 'IfcPile')


if __name__ == '__main__':
    results = piles_on_cobertura('./projects/fnde/EST.ifc')
    print(f'Found {len(results)} piles on Cobertura')
    for r in results:
        print(r)
