"""
Reusable function to list IFC entities of a given class contained in a building storey.

Purpose:
    Find all entities of a specified IFC class that are located in (or assigned to)
    a building storey identified by its Name attribute.

Args:
    ifc_path (str): Path to the IFC file.
    storey_name (str): The Name of the IfcBuildingStorey to search (exact match).
    entity_class (str): IFC entity class to filter (e.g., "IfcWall", "IfcPile").

Returns:
    List[dict]: A list of dictionaries for each found entity. Each dict contains:
        - "global_id" (str): The GlobalId of the entity
        - "type" (str): The IFC type name (e.g., IfcPile)
        - "name" (str): The Name attribute (may be empty)

Example:
    >>> from skills.learned.relationships.scripts.list_entities_in_storey import list_entities_in_storey
    >>> results = list_entities_in_storey('./projects/fnde/EST.ifc', 'Cobertura', 'IfcPile')
    >>> print(len(results))
    3
"""
from typing import List, Dict
import ifcopenshell
import ifcopenshell.util.selector


def list_entities_in_storey(ifc_path: str, storey_name: str, entity_class: str) -> List[Dict[str, str]]:
    """
    List entities of a given IFC class that are assigned to a building storey by Name.

    Args:
        ifc_path: Path to the IFC model file.
        storey_name: Exact Name of the IfcBuildingStorey to filter by.
        entity_class: IFC class name to search for (e.g., "IfcPile").

    Returns:
        A list of dictionaries with keys: global_id, type, name.
    """
    model = ifcopenshell.open(ifc_path)

    # Use selector filter combining class and location (storey name)
    # Example filter: 'IfcPile, location="Cobertura"'
    selector_query = f'{entity_class}, location="{storey_name}"'
    elements = ifcopenshell.util.selector.filter_elements(model, selector_query)

    results: List[Dict[str, str]] = []
    for el in elements:
        gid = getattr(el, 'GlobalId', None)
        name = getattr(el, 'Name', '') or ''
        results.append({
            'global_id': gid,
            'type': el.is_a(),
            'name': name,
        })

    return results
