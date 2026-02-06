"""
Count IfcCableCarrierSegment elements on storey 'TÉRREO' in the ELE.ifc model.

This script defines a function `count_cable_carrier_segments_on_storey` which uses the
generic `count_entities` function from the learned skills to perform the query.

Run:
    python3 sandbox/count_cable_carrier_segments_elen01.py
"""
from typing import Optional
from skills.learned.quantities.scripts.count_entities import count_entities


def count_cable_carrier_segments_on_storey(ifc_path: str, storey_name: Optional[str] = 'TÉRREO') -> int:
    """Count IfcCableCarrierSegment elements located on a specific storey.

    Args:
        ifc_path (str): Path to the IFC model file.
        storey_name (Optional[str]): Name of the storey to filter by. Defaults to 'TÉRREO'.

    Returns:
        int: Number of IfcCableCarrierSegment elements on the specified storey.

    Example:
        >>> count_cable_carrier_segments_on_storey('./projects/fnde/ELE.ifc', 'TÉRREO')
        12
    """
    # use selector: class + location
    selector = f'IfcCableCarrierSegment, location="{storey_name}"'
    # delegate to generic function by building a temporary wrapper call
    # count_entities expects only class string, so we'll open model here if needed
    # but to obey Import-Call Consistency, call count_entities exactly as imported
    # The imported count_entities only accepts (ifc_path, entity_type)
    return count_entities(ifc_path, selector)


if __name__ == '__main__':
    model_path = './projects/fnde/ELE.ifc'
    result = count_cable_carrier_segments_on_storey(model_path)
    print(result)
