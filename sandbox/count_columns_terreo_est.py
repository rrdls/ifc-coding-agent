"""
Script to count IfcColumn entities on the 'Térreo' storey in the EST.ifc model.

This script uses the reusable function count_entities_on_storey from the learned quantities skill.
"""
from skills.learned.quantities.scripts.count_entities_storey import count_entities_on_storey


def count_columns_on_terreo(ifc_path: str) -> int:
    """Count columns on the 'Térreo' storey of the given IFC model.

    Args:
        ifc_path (str): Path to the IFC file.

    Returns:
        int: Number of IfcColumn entities on the Térreo storey.

    Example:
        >>> count_columns_on_terreo('./projects/fnde/EST.ifc')
        10
    """
    return count_entities_on_storey(ifc_path, 'IfcColumn', 'Térreo')


if __name__ == '__main__':
    model_path = './projects/fnde/EST.ifc'
    count = count_columns_on_terreo(model_path)
    print(count)
