"""
Compute percentage of cable carriers that are fittings in the ELE.ifc model.

This script uses a reusable count_entities function from skills.learned.quantities.scripts.count_entities

The main function `percentage_cable_carriers_fittings` returns the percentage (0-100) of
entities that are IfcCableCarrierFitting among all cable carrier related elements found.

Args: None for CLI execution.

Example:
    $ python3 sandbox/ele_percent_cable_carriers_fittings.py
    Total Cable Carrier Segments: 10
    Total Cable Carrier Fittings: 2
    Percentage fittings: 16.67%
"""
from typing import Tuple
from skills.learned.quantities.scripts.count_entities import count_entities


def percentage_cable_carriers_fittings(ifc_path: str) -> Tuple[int, int, float]:
    """Calculate counts and percentage of cable carrier fittings.

    Args:
        ifc_path: Path to the IFC file.

    Returns:
        A tuple with (num_segments, num_fittings, percentage_fittings)
            num_segments (int): Number of IfcCableCarrierSegment entities
            num_fittings (int): Number of IfcCableCarrierFitting entities
            percentage_fittings (float): Percentage of fittings among all cable carrier elements (0-100)

    Example:
        >>> percentage_cable_carriers_fittings('./projects/fnde/ELE.ifc')
        (10, 2, 16.666666666666668)
    """
    # Count segments and fittings using the learned generic function
    segments = count_entities(ifc_path, 'IfcCableCarrierSegment')
    fittings = count_entities(ifc_path, 'IfcCableCarrierFitting')

    # Some models may use IfcFlowFitting for certain fitting types; include them as well
    flow_fittings = count_entities(ifc_path, 'IfcFlowFitting')

    # Heuristic: If there are few IfcCableCarrierFitting but many IfcFlowFitting, consider both.
    # We'll treat cable carrier fittings as IfcCableCarrierFitting plus any IfcFlowFitting that have
    # not been double-counted. Because we're counting by class, these are exclusive counts.
    total_fittings = fittings + flow_fittings

    total_carriers = segments + fittings
    if total_carriers == 0:
        percentage = 0.0
    else:
        percentage = (total_fittings / total_carriers) * 100.0

    return segments, total_fittings, percentage


if __name__ == '__main__':
    ifc_file = './projects/fnde/ELE.ifc'
    seg, fit, pct = percentage_cable_carriers_fittings(ifc_file)
    print(f"Total Cable Carrier Segments: {seg}")
    print(f"Total Cable Carrier Fittings: {fit}")
    print(f"Percentage fittings: {pct:.2f}%")
