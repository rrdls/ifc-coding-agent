"""
Get materials and styles from geometry.

Example: Access material colors and transparency.
"""
import ifcopenshell
import ifcopenshell.geom

def get_materials_example():
    """Demonstrate accessing style/material data."""
    model = ifcopenshell.open('model.ifc')
    element = model.by_type('IfcWall')[0]
    
    settings = ifcopenshell.geom.settings()
    shape = ifcopenshell.geom.create_shape(settings, element)
    
    # Styles list
    for style in shape.geometry.materials:
        print(f"Name: {style.name}")
        
        if style.has_diffuse:
            print(f"  Diffuse RGB: {style.diffuse}")
        
        if style.has_transparency:
            print(f"  Transparency: {style.transparency}")
    
    # Material IDs per face
    material_ids = shape.geometry.material_ids

if __name__ == "__main__":
    get_materials_example()
