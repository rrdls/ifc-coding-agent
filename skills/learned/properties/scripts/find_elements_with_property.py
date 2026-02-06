"""
Find elements of a given IFC class that have a specific property with an expected value.

Purpose:
    Search an IFC model for elements of a specified class (e.g., IfcWall) where a named
    property (within any property set) matches one of the provided expected values.

Args:
    ifc_path (str): Path to the IFC file.
    entity_class (str): IFC entity class name to filter (e.g., "IfcWall").
    pset_name (str): Name of the property set to search (e.g., "Pset_WallCommon").
    prop_name (str): Name of the property to match (e.g., "LoadBearing").
    expected_values (list): List of values to consider a match. Values may be bool, int or str.

Returns:
    list: A list of matching Ifc entities. Empty list if none found.

Example:
    from skills.learned.properties.scripts.find_elements_with_property import find_elements_with_property
    matches = find_elements_with_property('./projects/fnde/ARQ.ifc', 'IfcWall', 'Pset_WallCommon', 'LoadBearing', [True, 'YES'])
"""
from typing import List, Any
import ifcopenshell


def _prop_value_to_string(val: Any) -> str:
    """Helper to convert a property value to a comparable lowercase string."""
    if val is None:
        return ""
    if isinstance(val, bool):
        return str(val).lower()
    try:
        return str(val).lower()
    except Exception:
        return ""


def find_elements_with_property(ifc_path: str, entity_class: str, pset_name: str, prop_name: str, expected_values: List[Any]) -> List[object]:
    """
    Search the IFC model for entities of type `entity_class` that have a property
    named `prop_name` (inside any property set, optionally matching `pset_name`) whose
    value matches one of `expected_values`.

    Args:
        ifc_path (str): Path to the IFC file.
        entity_class (str): IFC entity class name to filter (e.g., "IfcWall").
        pset_name (str): Property set name to match. If empty string, any PSet is considered.
        prop_name (str): Property name to look for.
        expected_values (List[Any]): Values to match (case-insensitive for strings).

    Returns:
        List[object]: List of matching IFC entities. Empty list if none.

    Example:
        matches = find_elements_with_property('./projects/fnde/ARQ.ifc', 'IfcWall', 'Pset_WallCommon', 'LoadBearing', [True, 'YES'])
    """
    model = ifcopenshell.open(ifc_path)
    matches: List[object] = []

    # Normalize expected values to lowercase strings for comparison
    expected_norm = set(_prop_value_to_string(v) for v in expected_values)

    # Collect elements of the requested class
    try:
        elements = model.by_type(entity_class)
    except Exception:
        # If the entity type is unknown, return empty
        elements = []

    for elem in elements:
        # Some models may store load-bearing info as an attribute on the element itself
        # Check direct attribute first if present
        attr_val = None
        if hasattr(elem, 'LoadBearing'):
            attr_val = getattr(elem, 'LoadBearing')
            if _prop_value_to_string(attr_val) in expected_norm:
                matches.append(elem)
                continue

        # Now check property sets via IsDefinedBy relationships
        if not hasattr(elem, 'IsDefinedBy'):
            continue
        for rel in elem.IsDefinedBy:
            # We expect IfcRelDefinesByProperties with RelatingPropertyDefinition as IfcPropertySet
            propdef = getattr(rel, 'RelatingPropertyDefinition', None)
            if propdef is None:
                continue

            # Some property sets may have names; if pset_name provided, check it
            pset_name_match = True
            if pset_name:
                try:
                    actual_pset_name = getattr(propdef, 'Name', '')
                    if actual_pset_name is None:
                        actual_pset_name = ''
                    if actual_pset_name != pset_name:
                        pset_name_match = False
                except Exception:
                    pset_name_match = False

            if not pset_name_match:
                continue

            # Iterate properties
            has_props = getattr(propdef, 'HasProperties', [])
            for prop in has_props:
                try:
                    name = getattr(prop, 'Name', '')
                except Exception:
                    name = ''
                if name != prop_name:
                    continue

                # Extract value depending on property type
                val = None
                # If property has NominalValue (IfcPropertySingleValue)
                if hasattr(prop, 'NominalValue') and prop.NominalValue is not None:
                    nv = prop.NominalValue
                    # Try wrappedValue (common in ifcopenshell)
                    if hasattr(nv, 'wrappedValue'):
                        val = nv.wrappedValue
                    else:
                        val = nv
                # If property is an enumerated value
                elif hasattr(prop, 'EnumerationValues') and prop.EnumerationValues:
                    ev = prop.EnumerationValues
                    try:
                        # EnumerationValues is a list; take first
                        if len(ev) > 0 and hasattr(ev[0], 'wrappedValue'):
                            val = ev[0].wrappedValue
                        else:
                            val = ev[0]
                    except Exception:
                        val = None
                # Fallback: try property directly
                else:
                    try:
                        val = getattr(prop, 'Value', None)
                    except Exception:
                        val = None

                if _prop_value_to_string(val) in expected_norm:
                    matches.append(elem)
                    break  # no need to check more properties for this element

            # If already matched, skip to next element
            if elem in matches:
                break

    return matches
