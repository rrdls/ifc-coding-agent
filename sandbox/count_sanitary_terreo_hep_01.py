"""
Sandbox script for Query ID: HEP_FILTEREDAGGREGATION_01

This script counts the number of IfcSanitaryTerminal entities located on the storey named "TÉRREO"
in the provided IFC model (./projects/fnde/HEP.ifc) using the generic function
count_entities_on_storey from skills.learned.quantities.scripts.count_entities_on_storey.

Usage:
    python3 sandbox/count_sanitary_terreo_hep_01.py
"""
from skills.learned.quantities.scripts.count_entities_on_storey import count_entities_on_storey


def count_sanitary_on_terreo(ifc_path: str) -> int:
    """Count IfcSanitaryTerminal elements on the storey named 'TÉRREO'.

    Args:
        ifc_path: Path to the IFC model file.

    Returns:
        int: Number of sanitary terminals found on the 'TÉRREO' storey.

    Example:
        >>> count_sanitary_on_terreo('./projects/fnde/HEP.ifc')
        10
    """
    return count_entities_on_storey(ifc_path, 'IfcSanitaryTerminal', storey_name='TÉRREO')


if __name__ == '__main__':
    model_path = './projects/fnde/HEP.ifc'
    total = count_sanitary_on_terreo(model_path)
    print(total)
