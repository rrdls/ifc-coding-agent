"""
Filter IFC elements by material.

Example: Find concrete walls and slabs.
"""
import ifcopenshell
import ifcopenshell.util.selector

def filter_by_material_example():
    """Demonstrate filtering elements by material."""
    model = ifcopenshell.open('model.ifc')
    
    # Filter by material name
    concrete_elements = ifcopenshell.util.selector.filter_elements(
        model,
        'IfcWall, IfcSlab, material=concrete'
    )
    print(f"Found {len(concrete_elements)} concrete walls and slabs")

if __name__ == "__main__":
    filter_by_material_example()
