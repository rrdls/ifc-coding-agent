"""
Extract material information from IFC elements.

Example: Get material count and names.
"""
import ifcopenshell
import ifcopenshell.util.selector

def extract_materials_example():
    """Demonstrate extracting material information."""
    model = ifcopenshell.open('model.ifc')
    wall = model.by_type('IfcWall')[0]
    
    # Material info
    mat_count = ifcopenshell.util.selector.get_element_value(wall, "materials.count")
    mat_name = ifcopenshell.util.selector.get_element_value(wall, "material.Name")
    first_item = ifcopenshell.util.selector.get_element_value(wall, "material.item.0.Name")
    
    print(f"Material Count: {mat_count}")
    print(f"Material Name: {mat_name}")
    print(f"First Layer: {first_item}")

if __name__ == "__main__":
    extract_materials_example()
