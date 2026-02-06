"""
Count entities of a specified type in an IFC model with optional material and storey filters.

Purpose:
    Provide a reusable function to count IFC entities by class and optional filters
    such as material name and spatial location (storey name).

Args:
    ifc_path (str): Path to the IFC file.
    entity_type (str): IFC entity class to count (e.g., "IfcWall").
    material_name (str | None): Optional material name to filter by (exact match).
    storey_name (str | None): Optional storey/location name to filter by (exact match).

Returns:
    int: Count of entities matching the filters.

Example:
    >>> from skills.learned.quantities.scripts.count_entities_filtered import count_entities_filtered
    >>> count = count_entities_filtered('./projects/fnde/ARQ.ifc', 'IfcWall', material_name='VEDAÇÃO EXTERNA', storey_name='TÉRREO')
    >>> print(count)
"""
from typing import Optional
import ifcopenshell
import ifcopenshell.util.selector


def count_entities_filtered(ifc_path: str, entity_type: str, material_name: Optional[str] = None, storey_name: Optional[str] = None) -> int:
    """Count IFC entities of a given type with optional material and storey filters.

    Args:
        ifc_path (str): Path to the IFC file.
        entity_type (str): IFC entity class to count (e.g., "IfcWall").
        material_name (str | None): Optional material name to filter by (exact match). If provided and contains spaces or special characters, it will be used as-is.
        storey_name (str | None): Optional storey/location name to filter by (exact match).

    Returns:
        int: Number of entities that match the criteria.

    Example:
        >>> count_entities_filtered('models/ARQ.ifc', 'IfcWall', material_name='VEDAÇÃO EXTERNA', storey_name='TÉRREO')
    """
    model = ifcopenshell.open(ifc_path)

    # Build selector query
    filters = [entity_type]
    if material_name:
        # Use quotes to allow spaces and special characters
        filters.append(f'material="{material_name}"')
    if storey_name:
        # location filter matches storey name
        filters.append(f'location="{storey_name}"')

    query = ', '.join(filters)

    elements = ifcopenshell.util.selector.filter_elements(model, query)
    return len(elements)
