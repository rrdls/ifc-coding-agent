"""
Count entities of a given IFC class that use a specific material.

Purpose:
    Generic reusable function to count the number of entities of a given
    IFC class (e.g., IfcWall) that are associated with a material by name.

Args:
    ifc_path (str): Path to the IFC file.
    entity_type (str): IFC entity class to filter (e.g., "IfcWall").
    material_name (str): Exact material name to match (case-sensitive).

Returns:
    int: Number of matching entities found in the model.

Example:
    >>> count_entities_by_material('./projects/fnde/ARQ.ifc', 'IfcWall', 'concrete')
    42
"""
from typing import Any
import ifcopenshell
import ifcopenshell.util.selector


def count_entities_by_material(ifc_path: str, entity_type: str, material_name: str) -> int:
    """Count entities of a given IFC class that reference a material by name.

    This function uses ifcopenshell.util.selector.filter_elements with a material
    filter. Material names that contain spaces or special characters are quoted
    in the selector automatically.

    Args:
        ifc_path: Path to the IFC model file.
        entity_type: IFC class name to filter (e.g., "IfcWall").
        material_name: Exact material name to match (case-sensitive).

    Returns:
        The integer count of matching entities.

    Example:
        >>> count_entities_by_material('./projects/fnde/ARQ.ifc', 'IfcWall', 'TIJOLO - MACIÇO 5x10x20')
        10
    """
    model = ifcopenshell.open(ifc_path)
    # Quote material value to be safe when it contains spaces or special characters
    selector_str = f'{entity_type}, material="{material_name}"'
    elements = ifcopenshell.util.selector.filter_elements(model, selector_str)
    return len(elements)
