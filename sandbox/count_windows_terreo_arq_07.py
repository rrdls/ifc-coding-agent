"""
Script to count the number of IfcWindow elements on storey 'TÉRREO' in the ARQ.ifc model.

Creates a function `count_windows_on_storey` that uses the learned skill
`count_entities_on_storey`.

Execute with:
    python3 sandbox/count_windows_terreo_arq_07.py
"""
from skills.learned.quantities.scripts.count_entities_on_storey import count_entities_on_storey


def count_windows_on_storey(ifc_path: str, storey_name: str) -> int:
    """Count IfcWindow elements on a given storey.

    Args:
        ifc_path: Path to the IFC file.
        storey_name: Exact storey name to filter by (e.g., 'T\u00c9RREO').

    Returns:
        int: Number of IfcWindow instances on the specified storey.

    Example:
        >>> count_windows_on_storey('./projects/fnde/ARQ.ifc', 'T\u00c9RREO')
    """
    return count_entities_on_storey(ifc_path, 'IfcWindow', storey_name=storey_name)


if __name__ == '__main__':
    model_path = './projects/fnde/ARQ.ifc'
    storey = 'T\u00c9RREO'  # TÉRREO with acute accent
    count = count_windows_on_storey(model_path, storey)
    print(count)
