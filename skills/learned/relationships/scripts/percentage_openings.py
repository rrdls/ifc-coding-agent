"""
Compute percentage of openings that are in exterior walls.

This module provides a reusable function to calculate what percentage of
IfcOpeningElement instances in an IFC model are associated with exterior walls.

Functions
---------
percentage_openings_in_exterior_walls(ifc_path: str) -> float
    Calculate percentage of openings that are in exterior walls.
"""
from typing import Optional
import ifcopenshell


def _get_pset_property_value(prop) -> Optional[object]:
    """Return a best-effort value for an IfcProperty (handles SingleValue wrappers).

    Args:
        prop: An IfcProperty instance (IfcPropertySingleValue, etc.).

    Returns:
        The Python value of the property if found, otherwise None.
    """
    try:
        # If property is IfcPropertySingleValue there is a NominalValue attribute
        nominal = getattr(prop, "NominalValue", None)
        if nominal is not None:
            # Try common attribute names used by ifcopenshell wrappers
            for attr in ("wrappedValue", "WrappedValue", "Value", "value"):
                val = getattr(nominal, attr, None)
                if val is not None:
                    return val
        # Some property types store direct values
        for attr in ("BooleanValue", "IntegerValue", "RealValue", "TextValue"):
            val = getattr(prop, attr, None)
            if val is not None:
                return val
    except Exception:
        return None
    return None


def _is_wall_exterior(wall) -> Optional[bool]:
    """Determine whether a wall entity is exterior.

    Strategy (best-effort):
    - Check for attribute `IsExternal` on the wall entity.
    - If not present, search property sets (IfcPropertySet) for properties
      named like 'IsExternal' (case-insensitive) and use their boolean value.

    Args:
        wall: An IfcWall / IfcWallStandardCase entity.

    Returns:
        True if wall is explicitly marked exterior, False if explicitly marked
        interior, or None if no explicit information is found.
    """
    # Check direct attribute
    try:
        if hasattr(wall, "IsExternal"):
            val = getattr(wall, "IsExternal")
            if val is not None:
                return bool(val)
    except Exception:
        pass

    # Inspect property sets
    try:
        rels = getattr(wall, "IsDefinedBy", []) or []
        for rel in rels:
            # Guard: ensure this is a property-definition relation
            if rel is None:
                continue
            if rel.is_a("IfcRelDefinesByProperties"):
                prop_def = getattr(rel, "RelatingPropertyDefinition", None)
                if prop_def is None:
                    continue
                if prop_def.is_a("IfcPropertySet"):
                    for prop in getattr(prop_def, "HasProperties", []) or []:
                        name = getattr(prop, "Name", "") or ""
                        if name and name.lower().replace(" ", "") in ("isexternal","isexternalwall","external"):
                            val = _get_pset_property_value(prop)
                            if val is None:
                                continue
                            # Interpret common truthy values
                            if isinstance(val, str):
                                v = val.strip().lower()
                                if v in ("true","yes","1"):
                                    return True
                                if v in ("false","no","0"):
                                    return False
                            try:
                                return bool(val)
                            except Exception:
                                continue
    except Exception:
        pass

    return None


def percentage_openings_in_exterior_walls(ifc_path: str) -> float:
    """Calculate percentage of openings that are located in exterior walls.

    The function uses IfcRelVoidsElement relationships to associate
    IfcOpeningElement instances with their host building elements. An opening
    is counted as "in an exterior wall" if any of its host walls is explicitly
    marked as exterior (via attribute `IsExternal` or a property named like
    'IsExternal' in a property set).

    Args:
        ifc_path (str): Path to the IFC file.

    Returns:
        float: Percentage of openings in exterior walls (0.0 - 100.0). If the
               model contains zero openings the function returns 0.0.

    Example:
        >>> percentage_openings_in_exterior_walls('./projects/fnde/ARQ.ifc')
        23.5
    """
    model = ifcopenshell.open(ifc_path)

    openings = model.by_type("IfcOpeningElement")
    total = len(openings)
    if total == 0:
        return 0.0

    # Build mapping from opening id to list of host elements using IfcRelVoidsElement
    rels = model.by_type("IfcRelVoidsElement")
    opening_to_hosts = {}
    for rel in rels:
        try:
            opening = getattr(rel, "RelatedOpeningElement", None)
            host = getattr(rel, "RelatingBuildingElement", None)
            if opening is None or host is None:
                continue
            opening_to_hosts.setdefault(opening.id(), []).append(host)
        except Exception:
            continue

    exterior_count = 0
    for op in openings:
        hosts = opening_to_hosts.get(op.id(), [])
        is_exterior = False
        for h in hosts:
            # consider only walls
            try:
                if not (h.is_a("IfcWall") or h.is_a("IfcWallStandardCase")):
                    continue
            except Exception:
                continue
            val = _is_wall_exterior(h)
            if val is True:
                is_exterior = True
                break
            # If val is None, we don't count yet; only explicit True counts
        if is_exterior:
            exterior_count += 1

    percent = (exterior_count / total) * 100.0
    return percent
