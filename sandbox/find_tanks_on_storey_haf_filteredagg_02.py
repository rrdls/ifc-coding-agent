"""
Script: find_tanks_on_storey_haf_filteredagg_02.py
Purpose: Determine whether there are Any IfcTanks on the COBERTURA storey in the HAF.ifc model.

This script defines a function `tanks_on_storey` which uses the generic
`count_entities` function from skills.learned.quantities.scripts.count_entities
to count IfcTank occurrences filtered by location.

The script prints the count and exits with a printed answer:
- "Tanks found: N" and a summary line.

Usage:
    python3 sandbox/find_tanks_on_storey_haf_filteredagg_02.py
"""
from typing import Any
from skills.learned.quantities.scripts.count_entities import count_entities


def tanks_on_storey(ifc_path: str, storey_name: str) -> int:
    """Count tanks on a named storey in an IFC model.

    Args:
        ifc_path (str): Path to the IFC file.
        storey_name (str): Name of the storey to search for (e.g., "COBERTURA").

    Returns:
        int: Number of IfcTank entities located on the specified storey.

    Example:
        >>> tanks_on_storey('./projects/fnde/HAF.ifc', 'COBERTURA')
        1
    """
    # Use selector: class and location
    selector = f"IfcTank, location=\"{storey_name}\""
    return count_entities(ifc_path, selector)


if __name__ == '__main__':
    ifc = './projects/fnde/HAF.ifc'
    storey = 'COBERTURA'
    count = tanks_on_storey(ifc, storey)
    print(f"Tanks found: {count}")
    if count > 0:
        print('Answer: Yes — there are tanks on the COBERTURA storey.')
    else:
        print('Answer: No — there are no tanks on the COBERTURA storey.')
