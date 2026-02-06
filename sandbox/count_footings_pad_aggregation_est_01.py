"""
Count footings with predefined type PAD_FOOTING in the given IFC model.

This script defines a reusable function `count_footings_with_predefined_type` and
prints the result when executed as a script.
"""
from typing import Any
from skills.learned.quantities.scripts.count_entities import count_entities


def count_footings_with_predefined_type(ifc_path: str, predefined_type: str = "PAD_FOOTING") -> int:
    """Count IfcFooting elements that have the given PredefinedType.

    Args:
        ifc_path (str): Path to the IFC file.
        predefined_type (str): The PredefinedType to filter footings by (default: "PAD_FOOTING").

    Returns:
        int: Number of IfcFooting elements with the specified PredefinedType.

    Example:
        >>> count_footings_with_predefined_type('./projects/fnde/EST.ifc', 'PAD_FOOTING')
        5
    """
    # Use selector syntax: filter by class and attribute
    selector = f"IfcFooting, PredefinedType={predefined_type}"
    return count_entities(ifc_path, selector)


if __name__ == "__main__":
    import sys
    model_path = "./projects/fnde/EST.ifc"
    result = count_footings_with_predefined_type(model_path)
    print(result)
