import ifcopenshell


def get_length_units(ifc_path: str) -> str:
    """
    Get the length units used in an IFC file.

    Args:
        ifc_path (str): Path to the IFC file.

    Returns:
        str: Human-readable description of the length units (e.g., "METRE", "CENTIMETRE"). If multiple units are found, returns a comma-separated list. If no length unit is present, returns 'NOT FOUND'.

    Example:
        >>> get_length_units('./projects/fnde/ARQ.ifc')
        'METRE'
    """
    model = ifcopenshell.open(ifc_path)
    # Unit assignment is usually in project.UnitsInContext
    units = []

    # Check IfcUnitAssignment entity
    for ua in model.by_type('IfcUnitAssignment'):
        if ua.Units:
            for u in ua.Units:
                # If SI Unit
                if u.is_a('IfcSIUnit'):
                    if hasattr(u, 'UnitType') and u.UnitType:
                        if u.UnitType == 'LENGTHUNIT' or str(u.UnitType).upper() == 'LENGTHUNIT':
                            if hasattr(u, 'Prefix') and u.Prefix:
                                units.append(f"{u.Prefix}_{u.Name}")
                            else:
                                units.append(str(u.Name))
                # If conversion based unit
                elif u.is_a('IfcConversionBasedUnit'):
                    # Check dimensions
                    if hasattr(u, 'Dimensions') and u.Dimensions:
                        # Dimensions may point to an IfcDimensionalExponents; length exponent 1 indicates length
                        # However, easier approach: check if UnitType attribute exists
                        if hasattr(u, 'UnitType') and (u.UnitType == 'LENGTHUNIT' or str(u.UnitType).upper() == 'LENGTHUNIT'):
                            units.append(u.Name if hasattr(u, 'Name') and u.Name else 'ConversionBasedUnit')
                    else:
                        units.append(u.Name if hasattr(u, 'Name') and u.Name else 'ConversionBasedUnit')
                else:
                    # Generic IfcUnit with Name attribute
                    if hasattr(u, 'Name') and u.Name:
                        units.append(u.Name)
    # If still empty, look for IfcSIUnit directly
    if not units:
        for si in model.by_type('IfcSIUnit'):
            if hasattr(si, 'UnitType') and (si.UnitType == 'LENGTHUNIT' or str(si.UnitType).upper() == 'LENGTHUNIT'):
                units.append(si.Name if hasattr(si, 'Name') and si.Name else 'SI_UNIT')

    if units:
        # Normalize and unique
        cleaned = []
        for it in units:
            it_str = str(it).upper()
            if it_str not in cleaned:
                cleaned.append(it_str)
        return ', '.join(cleaned)
    return 'NOT FOUND'
