"""
Discovery script to list building storeys and wall counts per storey.

Defines:
 - list_storeys(ifc_path: str) -> list

Example:
    >>> list_storeys('./projects/fnde/ARQ.ifc')
    ['TÉRREO', '1º ANDAR']
"""
import ifcopenshell
from typing import List, Dict


def list_storeys(ifc_path: str) -> List[str]:
    """Return a list of storey names present in the IFC model.

    Args:
        ifc_path (str): Path to the IFC file.

    Returns:
        List[str]: List of storey names (Name attribute) found in the model.

    Example:
        >>> list_storeys('./projects/fnde/ARQ.ifc')
        ['TÉRREO', '1º ANDAR']
    """
    model = ifcopenshell.open(ifc_path)
    storeys = model.by_type('IfcBuildingStorey')
    names = []
    for s in storeys:
        if hasattr(s, 'Name') and s.Name:
            names.append(s.Name)
    return names


def wall_counts_per_storey(ifc_path: str) -> Dict[str, int]:
    """Count IfcWall and IfcWallStandardCase occurrences per storey Name.

    Args:
        ifc_path (str): Path to the IFC file.

    Returns:
        Dict[str, int]: Mapping of storey name to number of walls on that storey.
    """
    model = ifcopenshell.open(ifc_path)
    storeys = model.by_type('IfcBuildingStorey')
    counts = {}
    for s in storeys:
        name = s.Name if hasattr(s, 'Name') and s.Name else 'UNKNOWN'
        # Use selector by evaluating spatial containment: check all walls and see if contained in this storey
        walls = []
        for w in model.by_type('IfcWall') + model.by_type('IfcWallStandardCase'):
            # check related spatial structure
            if hasattr(w, 'ContainedInStructure') and w.ContainedInStructure:
                for rel in w.ContainedInStructure:
                    if hasattr(rel, 'RelatingStructure') and rel.RelatingStructure == s:
                        walls.append(w)
        counts[name] = len(walls)
    return counts

if __name__ == '__main__':
    path = './projects/fnde/ARQ.ifc'
    names = list_storeys(path)
    print('Storeys found:')
    for n in names:
        print(n)
    print('\nWall counts per storey:')
    counts = wall_counts_per_storey(path)
    for k, v in counts.items():
        print(f"{k}: {v}")
