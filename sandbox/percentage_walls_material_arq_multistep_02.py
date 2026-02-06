"""
Compute percentage of IfcWall elements that use a specified material name.

This script defines a function `percentage_walls_with_material` that opens an IFC
model, counts total walls and those that reference the given material name via
material association, and prints the percentage.

It reuses the generic `count_entities` function from skills.learned.quantities.
"""
from typing import Tuple
from skills.learned.quantities.scripts.count_entities import count_entities
import ifcopenshell
import ifcopenshell.util.selector


def percentage_walls_with_material(ifc_path: str, material_name: str) -> Tuple[int, int, float]:
    """Calculate the percentage of IfcWall entities that use the specified material.

    Args:
        ifc_path (str): Path to the IFC file.
        material_name (str): Material name to match (exact match, case-sensitive).

    Returns:
        Tuple[int, int, float]: (total_walls, walls_with_material, percentage)

    Example:
        >>> percentage_walls_with_material('./projects/fnde/ARQ.ifc', 'TIJOLO - MACIÇO 5x10x20')
        (120, 30, 25.0)
    """
    # Count total walls using the learned skill
    total_walls = count_entities(ifc_path, 'IfcWall')

    model = ifcopenshell.open(ifc_path)
    # Use selector to filter walls by material name if possible
    # Selector supports material=, but material names in IFC can be attached in various ways.
    # First try selector with material filter (quick path)
    try:
        query = f"IfcWall, material=\"{material_name}\""
        matched = ifcopenshell.util.selector.filter_elements(model, query)
        walls_with_material = len(matched)
    except Exception:
        # Fallback: manual inspection of material associations
        walls_with_material = 0
        walls = ifcopenshell.util.selector.filter_elements(model, 'IfcWall')
        for w in walls:
            # Check HasAssociations -> IfcRelAssociatesMaterial -> RelatingMaterial
            assoc = getattr(w, 'HasAssociations', None)
            if not assoc:
                continue
            for a in assoc:
                # Look for IfcRelAssociatesMaterial
                if a.is_a('IfcRelAssociatesMaterial'):
                    rm = a.RelatingMaterial
                    if not rm:
                        continue
                    # If the material is a single material use Name, or check for layers
                    name = getattr(rm, 'Name', None)
                    if name == material_name:
                        walls_with_material += 1
                        break
                    # If it's a material layer set, traverse ForLayerSet
                    # Check Common representations
                    if rm.is_a('IfcMaterialLayerSet'):
                        for layer in getattr(rm, 'MaterialLayers', []):
                            m = layer.Material
                            if getattr(m, 'Name', None) == material_name:
                                walls_with_material += 1
                                break
                    if rm.is_a('IfcMaterialLayerSetUsage'):
                        ls = rm.ForLayerSet
                        if ls:
                            for layer in getattr(ls, 'MaterialLayers', []):
                                m = layer.Material
                                if getattr(m, 'Name', None) == material_name:
                                    walls_with_material += 1
                                    break

    percentage = (walls_with_material / total_walls * 100.0) if total_walls > 0 else 0.0
    print(f"Total walls: {total_walls}")
    print(f"Walls with material '{material_name}': {walls_with_material}")
    print(f"Percentage: {percentage:.2f}%")
    return total_walls, walls_with_material, percentage


if __name__ == '__main__':
    percentage_walls_with_material('./projects/fnde/ARQ.ifc', 'TIJOLO - MACIÇO 5x10x20')
