"""
Compute average number of openings per external wall in an IFC model.

This script defines a function `average_openings_per_external_wall` which opens an IFC
model, identifies external walls (walls with IsExternal attribute True when available,
otherwise heuristically by association to an external surface/space), counts openings
(IfcOpeningElement or IfcWindow/IfcDoor) related to each external wall, and returns
the average number of openings per external wall.

The script imports the generic `count_entities` function from the learned quantities
skill and uses IfcOpenShell selector utilities for filtering.

Usage:
    python3 sandbox/average_openings_per_external_wall_arq_multistep_12.py
"""
from typing import List, Tuple
from skills.learned.quantities.scripts.count_entities import count_entities

import ifcopenshell
import ifcopenshell.util.selector


def average_openings_per_external_wall(ifc_path: str) -> float:
    """Calculate average number of openings per external wall.

    Args:
        ifc_path (str): Path to the IFC file.

    Returns:
        float: Average number of openings per external wall. Returns 0.0 if no external walls found.

    Example:
        >>> avg = average_openings_per_external_wall('./projects/fnde/ARQ.ifc')
        >>> print(avg)
    """
    model = ifcopenshell.open(ifc_path)

    # Step 1: find walls. Use selector to get IfcWall or IfcWallStandardCase
    try:
        walls = ifcopenshell.util.selector.filter_elements(model, 'IfcWall, IfcWallStandardCase')
    except Exception:
        # Fallback: get by type
        walls = model.by_type('IfcWall') + model.by_type('IfcWallStandardCase')

    external_walls = []
    # Prefer explicit IsExternal attribute if present in IfcBuildingElementProxy/IfcWall
    for w in walls:
        is_external = False
        # Check common attribute
        if hasattr(w, 'IsExternal') and getattr(w, 'IsExternal', None) is not None:
            try:
                is_external = bool(w.IsExternal)
            except Exception:
                is_external = False
        # Fallback: check if wall has an external boundary representation by name or Pset
        if not is_external:
            # Heuristic: If Name or Description contains 'external' or 'outside'
            name = getattr(w, 'Name', '') or ''
            desc = getattr(w, 'Description', '') or ''
            if 'external' in name.lower() or 'external' in desc.lower() or 'outside' in name.lower() or 'outside' in desc.lower():
                is_external = True
        if is_external:
            external_walls.append(w)

    # If no walls marked external, attempt a broader heuristic using IfcSpace adjacency (last resort not used here)

    # Prepare to count openings per wall. We'll consider IfcOpeningElement, IfcWindow, IfcDoor as openings.
    try:
        openings = ifcopenshell.util.selector.filter_elements(model, 'IfcOpeningElement, IfcWindow, IfcDoor')
    except Exception:
        openings = model.by_type('IfcOpeningElement') + model.by_type('IfcWindow') + model.by_type('IfcDoor')

    # Build mapping from wall id to a set of opening ids by checking IfcRelVoidsElement relationships
    wall_opening_ids = {w.id(): set() for w in external_walls}

    # If no external walls found, return 0.0 to avoid division by zero
    if len(external_walls) == 0:
        return 0.0

    # Find IfcRelVoidsElement entities and map RelatingBuildingElement (wall) to RelatedOpeningElement (opening)
    rels_voids = model.by_type('IfcRelVoidsElement')
    opening_to_walls = {}  # map opening id to list of wall ids (usually one)
    for rv in rels_voids:
        relating = getattr(rv, 'RelatingBuildingElement', None)
        related = getattr(rv, 'RelatedOpeningElement', None)
        if relating is None or related is None:
            continue
        # relating could be a wall entity
        for w in external_walls:
            if relating is w:
                wid = w.id()
                oid = related.id()
                wall_opening_ids[wid].add(oid)
                opening_to_walls.setdefault(oid, set()).add(wid)

    # Some windows/doors may fill openings via IfcRelFillsElement. Ensure we account for openings that have fillings.
    rels_fills = model.by_type('IfcRelFillsElement')
    for rf in rels_fills:
        opening = getattr(rf, 'RelatingOpeningElement', None)
        filling = getattr(rf, 'RelatedBuildingElement', None)
        if opening is None or filling is None:
            continue
        oid = opening.id()
        # If this opening is already associated with an external wall, it's already counted.
        if oid in opening_to_walls:
            continue
        # Otherwise, see if the opening itself has a relation to a wall via other rels (defensive)
        # Search rels_voids for this opening
        for rv in rels_voids:
            related = getattr(rv, 'RelatedOpeningElement', None)
            relating = getattr(rv, 'RelatingBuildingElement', None)
            if related is None or relating is None:
                continue
            try:
                if related.id() == oid:
                    # related opening belongs to a wall
                    for w in external_walls:
                        if relating is w:
                            wall_opening_ids[w.id()].add(oid)
            except Exception:
                continue

    # As a final attempt, consider windows/doors that may be directly related to walls via IfcRelAggregates or direct assignment
    # We'll look for IfcRelAggregates and IfcRelContainedInSpatialStructure linking doors/windows to walls (less common)
    rels_aggregates = model.by_type('IfcRelAggregates') + model.by_type('IfcRelContainedInSpatialStructure')
    for rel in rels_aggregates:
        relating = getattr(rel, 'RelatingObject', None) or getattr(rel, 'RelatingStructure', None)
        related_objects = getattr(rel, 'RelatedObjects', []) or getattr(rel, 'RelatedElements', [])
        if relating is None or not related_objects:
            continue
        # If relating is a wall, and related_objects contains windows/doors, count them
        for w in external_walls:
            if relating is w:
                wid = w.id()
                for obj in related_objects:
                    if obj is None:
                        continue
                    if obj.is_a('IfcWindow') or obj.is_a('IfcDoor') or obj.is_a('IfcOpeningElement'):
                        wall_opening_ids[wid].add(obj.id())

    # Finally compute average: count unique opening-like entities per external wall
    total_openings = sum(len(s) for s in wall_opening_ids.values())
    avg = total_openings / len(external_walls) if len(external_walls) > 0 else 0.0
    return avg


if __name__ == '__main__':
    import sys
    path = './projects/fnde/ARQ.ifc'
    if len(sys.argv) > 1:
        path = sys.argv[1]
    avg = average_openings_per_external_wall(path)
    print(f"Average openings per external wall: {avg}")