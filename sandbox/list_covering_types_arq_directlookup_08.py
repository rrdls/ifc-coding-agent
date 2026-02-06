"""
Script to list all unique covering types in the ARQ.ifc model.

This script imports a reusable function from skills/learned and prints the found types.
"""
from skills.learned.quantities.scripts.list_entity_attribute_values import get_unique_covering_types


def list_covering_types(ifc_path: str) -> None:
    """
    Print unique covering types found in the IFC model.

    Args:
        ifc_path (str): Path to the IFC file.

    Returns:
        None

    Example:
        python3 sandbox/list_covering_types_arq_directlookup_08.py
    """
    types = get_unique_covering_types(ifc_path)
    if not types:
        print("No covering types found in the model")
    else:
        for t in sorted(types):
            print(t)


if __name__ == "__main__":
    list_covering_types('./projects/fnde/ARQ.ifc')
