"""
Compare number of external vs internal walls on a given storey (TÉRREO) in an IFC model.

This script defines a function `compare_external_internal_walls_on_storey` that inspects
walls located on a named storey and counts how many are explicitly marked as external
or internal via the common property `Pset_WallCommon.IsExternal` (or equivalent truthy
string values).

Usage:
    python3 sandbox/compare_walls_terreo.py
"""
from typing import Tuple, Dict
from skills.learned.quantities.scripts.count_entities_on_storey import count_entities_on_storey
import ifcopenshell
import ifcopenshell.util.selector
import ifcopenshell.util.element as util_element


def compare_external_internal_walls_on_storey(ifc_path: str, storey_name: str) -> Tuple[int, int, int, int, bool]:
    """Compare external and internal wall counts on a named storey.

    The function examines all IfcWall elements located on the provided storey
    and checks their property sets (using ifcopenshell.util.element.get_psets)
    for `Pset_WallCommon.IsExternal`. Only explicit property values are used
    to classify a wall as external or internal. Values like True/False, 'TRUE'/'FALSE',
    'Yes'/'No', '1'/'0' are interpreted accordingly. Walls without an explicit
    IsExternal value are counted as unknown and excluded from the external/internal
    tallies.

    Args:
        ifc_path (str): Filesystem path to the IFC model.
        storey_name (str): Exact storey/location name to filter walls (e.g., 'T\u00c9RREO').

    Returns:
        Tuple[int, int, int, int, bool]: (total_on_storey, external_count, internal_count, unknown_count, more_external)
            - total_on_storey: total number of IfcWall instances located on the storey
            - external_count: number of walls explicitly marked as external
            - internal_count: number of walls explicitly marked as internal
            - unknown_count: number of walls without explicit IsExternal information
            - more_external: True if external_count > internal_count, False otherwise

    Example:
        >>> compare_external_internal_walls_on_storey('./projects/fnde/ARQ.ifc', 'T\u00c9RREO')
        (100, 40, 30, 30, True)
    """
    model = ifcopenshell.open(ifc_path)

    # Use selector to get walls on the storey
    selector = f'IfcWall, location="{storey_name}"'
    walls = ifcopenshell.util.selector.filter_elements(model, selector)
    total_on_storey = len(walls)

    external = 0
    internal = 0
    unknown = 0

    for w in walls:
        try:
            psets = util_element.get_psets(w)
        except Exception:
            psets = {}

        val = None
        # Common pset name
        if 'Pset_WallCommon' in psets:
            val = psets.get('Pset_WallCommon', {}).get('IsExternal')
        else:
            # Search any pset for a property name containing 'External' or 'IsExternal'
            for pset_name, props in psets.items():
                for prop_name, prop_val in props.items():
                    if prop_name and 'external' in prop_name.lower():
                        val = prop_val
                        break
                if val is not None:
                    break

        if val is None:
            unknown += 1
            continue

        # Interpret values
        if isinstance(val, str):
            v = val.strip().lower()
            if v in ('true', 'yes', '1'):
                external += 1
            elif v in ('false', 'no', '0'):
                internal += 1
            else:
                unknown += 1
        else:
            # Try boolean coercion for numeric/bool types
            try:
                if bool(val) is True:
                    external += 1
                else:
                    internal += 1
            except Exception:
                unknown += 1

    more_external = external > internal
    return (total_on_storey, external, internal, unknown, more_external)


if __name__ == '__main__':
    path = './projects/fnde/ARQ.ifc'
    storey = 'T\u00c9RREO'
    total, ext, inc, unk, more_ext = compare_external_internal_walls_on_storey(path, storey)
    print(f"Total walls on {storey}: {total}")
    print(f"External walls (explicit): {ext}")
    print(f"Internal walls (explicit): {inc}")
    print(f"Walls without explicit IsExternal: {unk}")
    print("More external than internal on {0}: {1}".format(storey, more_ext))
