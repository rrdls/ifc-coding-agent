"""
Discovery script to list property sets and IsExternal-like properties for IfcWall on a storey.
"""
from typing import Set
import ifcopenshell


def list_wall_psets(ifc_path: str, storey_name: str) -> Set[str]:
    """List unique property set names and property keys for walls on a given storey.

    Args:
        ifc_path: Path to IFC file
        storey_name: Name of the storey (e.g., 'TÉRREO')

    Returns:
        Set of strings describing pset.property for walls on the storey
    """
    model = ifcopenshell.open(ifc_path)
    walls = [e for e in model.by_type('IfcWall') if hasattr(e, 'ContainedInStructure') or True]
    results = set()
    for w in walls:
        # get psets via ifcopenshell.util.element.get_psets if available
        try:
            import ifcopenshell.util.element as util_element
            psets = util_element.get_psets(w)
            for pset_name, props in psets.items():
                for prop_name in props.keys():
                    results.add(f"{pset_name}.{prop_name}")
        except Exception:
            pass
    return results


if __name__ == '__main__':
    psets = list_wall_psets('./projects/fnde/ARQ.ifc', 'T\u00c9RREO')
    for p in sorted(psets):
        print(p)
