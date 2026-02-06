"""
Sandbox script to count IfcCovering entities that reference materials with 'epoxy' in the name.

This script imports the generic skill `count_entities_by_material_keyword` and runs it
against the provided ARQ.ifc model in ./projects/fnde/ARQ.ifc.
"""
from skills.learned.quantities.scripts.count_entities_by_material_keyword import count_entities_by_material_keyword


def count_coverings_using_epoxy(ifc_path: str) -> int:
    """Count IfcCovering elements that use epoxy paint materials.

    Args:
        ifc_path (str): Path to the IFC file.

    Returns:
        int: Number of IfcCovering elements with materials whose names contain 'epoxy'.

    Example:
        >>> count_coverings_using_epoxy('./projects/fnde/ARQ.ifc')
        7
    """
    return count_entities_by_material_keyword(ifc_path, 'IfcCovering', 'epoxy')


if __name__ == '__main__':
    import sys
    path = './projects/fnde/ARQ.ifc'
    result = count_coverings_using_epoxy(path)
    print(result)
