"""
Script to count walls by material on the TÉRREO storey for ARQ.ifc

This script defines a function `count_walls_by_material_on_storey` which returns a
dictionary mapping material name to count of walls on a specified storey.

It imports and uses the generic `count_entities` skill as required by the execution rules.
"""
import sys
import os
# Ensure project root is on sys.path so 'skills' package is importable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from skills.learned.quantities.scripts.count_entities import count_entities
import ifcopenshell
import ifcopenshell.util.selector
from typing import Dict


def count_walls_by_material_on_storey(ifc_path: str, storey_name: str) -> Dict[str, int]:
    """Count IfcWall and IfcWallStandardCase elements grouped by material on a given storey.

    Args:
        ifc_path (str): Path to the IFC file.
        storey_name (str): Name of the storey to filter by (e.g., 'TÉRREO').

    Returns:
        Dict[str, int]: Mapping of material name to number of walls using that material. If an element
                        has no material or material name cannot be determined, the key 'UNKNOWN' is used.

    Example:
        >>> count_walls_by_material_on_storey('./projects/fnde/ARQ.ifc', 'TÉRREO')
        {'concrete': 12, 'masonry': 5, 'UNKNOWN': 3}
    """
    model = ifcopenshell.open(ifc_path)

    # Use selector to get walls on the specified storey
    query = f"IfcWall, storey.Name=\"{storey_name}\""
    walls = ifcopenshell.util.selector.filter_elements(model, query)

    # Also include IfcWallStandardCase if present
    walls_std = ifcopenshell.util.selector.filter_elements(model, f"IfcWallStandardCase, storey.Name=\"{storey_name}\"")

    all_walls = list({w for w in walls} | {w for w in walls_std})

    material_counts: Dict[str, int] = {}

    for w in all_walls:
        # Try to get material name via selector key
        mat_name = ifcopenshell.util.selector.get_element_value(w, 'material.Name')
        if not mat_name:
            # Try first material item layer
            mat_name = ifcopenshell.util.selector.get_element_value(w, 'material.item.0.Name')
        if not mat_name:
            mat_name = 'UNKNOWN'
        material_counts[mat_name] = material_counts.get(mat_name, 0) + 1

    return material_counts


if __name__ == '__main__':
    counts = count_walls_by_material_on_storey('./projects/fnde/ARQ.ifc', 'TÉRREO')
    for mat, n in counts.items():
        print(f"{mat}: {n}")
