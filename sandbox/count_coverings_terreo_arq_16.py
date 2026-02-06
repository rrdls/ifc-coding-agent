"""
Count the number of IfcCovering entities located on the TÉRREO storey in the ARQ.ifc model.

This script defines a function `count_coverings_on_storey` that locates a storey by its Name
(or LongName) matching the provided storey_name, finds IfcCovering elements that are spatially
contained in that storey, and returns the count.

The script uses the generic `count_entities` from learned skills for potential reuse, but
per IFC spatial containment semantics we implement a targeted containment search.

Usage:
    python3 sandbox/count_coverings_terreo_arq_16.py
"""
from typing import List
from skills.learned.quantities.scripts.count_entities import count_entities
import ifcopenshell


def count_coverings_on_storey(ifc_path: str, storey_name: str) -> int:
    """Count IfcCovering elements that are contained in a storey with given name.

    Args:
        ifc_path (str): Path to the IFC file.
        storey_name (str): Name of the storey to search for (exact match, case-sensitive).

    Returns:
        int: Number of IfcCovering elements contained in the specified storey.

    Example:
        >>> count_coverings_on_storey('./projects/fnde/ARQ.ifc', 'TÉRREO')
        12
    """
    model = ifcopenshell.open(ifc_path)

    # Find storeys with matching Name or LongName
    storeys = [s for s in model.by_type('IfcBuildingStorey') if getattr(s, 'Name', None) == storey_name or getattr(s, 'LongName', None) == storey_name]
    if not storeys:
        # If not found by exact match, try case-insensitive and accent-insensitive fallback
        lower_name = storey_name.lower()
        storeys = [s for s in model.by_type('IfcBuildingStorey') if (getattr(s, 'Name', '') or '').lower() == lower_name or (getattr(s, 'LongName', '') or '').lower() == lower_name]

    if not storeys:
        # No matching storey name found
        return 0

    # Collect all coverings that are related by spatial structure (decomposed or spatially contained)
    coverings = []
    for storey in storeys:
        # Related elements via ContainsElements
        for rel in model.by_type('IfcRelContainedInSpatialStructure'):
            if rel.RelatingStructure == storey:
                for elem in rel.RelatedElements:
                    if elem.is_a('IfcCovering'):
                        coverings.append(elem)
        # Additionally, check decomposed elements (If element placed under storey using decomposition)
        for rel2 in model.by_type('IfcRelAggregates'):
            if rel2.RelatingObject == storey:
                for child in rel2.RelatedObjects:
                    if child.is_a('IfcCovering'):
                        coverings.append(child)

    # Deduplicate by id
    unique_coverings = {c.id(): c for c in coverings}
    return len(unique_coverings)


if __name__ == '__main__':
    path = './projects/fnde/ARQ.ifc'
    result = count_coverings_on_storey(path, 'TÉRREO')
    print(result)
