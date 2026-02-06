"""
Count doors on storey TÉRREO in ARQ.ifc
"""
from skills.learned.quantities.scripts.count_entities_on_storey import count_entities_on_storey


def count_doors_on_terreo(ifc_path: str) -> int:
    """Count IfcDoor elements on storey named 'T\u00c9RREO'.

    Args:
        ifc_path (str): Path to the IFC file.

    Returns:
        int: Number of IfcDoor elements located on the TÉRREO storey.

    Example:
        >>> count_doors_on_terreo('./projects/fnde/ARQ.ifc')
        12
    """
    # Use the learned generic function
    return count_entities_on_storey(ifc_path, 'IfcDoor', storey_name='TÉRREO')


if __name__ == '__main__':
    import sys
    path = './projects/fnde/ARQ.ifc'
    if len(sys.argv) > 1:
        path = sys.argv[1]
    result = count_doors_on_terreo(path)
    print(result)
