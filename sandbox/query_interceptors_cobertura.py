"""
Script to check for interceptors on the COBERTURA storey in the HEP.ifc model.

Creates a function `interceptors_on_storey` that returns a list of elements matching
interceptor-like classes or names on the specified storey.

Usage:
    python3 sandbox/query_interceptors_cobertura.py
"""
from typing import List
from skills.learned.spatial.scripts.find_elements_on_storey import find_elements_on_storey


def interceptors_on_storey(ifc_path: str, storey_name: str) -> List[str]:
    """
    Check the IFC model for interceptors located on a given building storey.

    Args:
        ifc_path (str): Path to the IFC file (e.g., './projects/fnde/HEP.ifc').
        storey_name (str): Name of the IfcBuildingStorey to search (e.g., 'COBERTURA').

    Returns:
        List[str]: List of string descriptions for found interceptor elements. Empty list if none found.

    Example:
        >>> interceptors_on_storey('./projects/fnde/HEP.ifc', 'COBERTURA')
        ['#12345 IfcFlowTreatmentDevice Name="Interceptor 1"']
    """
    # Potential classes that might represent interceptors in plumbing/sewage models
    candidate_classes = [
        'IfcFlowTreatmentDevice',
        'IfcDistributionControlElement',
        'IfcSanitaryTerminal',
        'IfcDistributionElement',
        'IfcElement'
    ]

    found = []
    for cls in candidate_classes:
        elems = find_elements_on_storey(ifc_path, storey_name, ifc_class=cls)
        for e in elems:
            name = getattr(e, 'Name', None)
            # crude name-based heuristic for 'interceptor' keyword
            if name and 'interceptor' in name.lower():
                found.append(f"#{e.id()} {e.is_a()} Name=\"{name}\"")
            else:
                # Also consider elements of FlowTreatmentDevice class as likely interceptors
                if e.is_a() == 'IfcFlowTreatmentDevice' or cls == 'IfcFlowTreatmentDevice':
                    found.append(f"#{e.id()} {e.is_a()} Name=\"{name}\"")
    # Deduplicate
    found_unique = list(dict.fromkeys(found))
    return found_unique


if __name__ == '__main__':
    results = interceptors_on_storey('./projects/fnde/HEP.ifc', 'COBERTURA')
    if results:
        print('Found interceptors:')
        for r in results:
            print(r)
    else:
        print('No interceptors found on storey COBERTURA')
