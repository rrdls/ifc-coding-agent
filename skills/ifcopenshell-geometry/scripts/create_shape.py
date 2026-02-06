"""
Process geometry for a single IFC element.

Example: Create shape and get basic geometry data.
"""
import ifcopenshell
import ifcopenshell.geom

def create_shape_example():
    """Demonstrate processing single element geometry."""
    model = ifcopenshell.open('model.ifc')
    element = model.by_type('IfcWall')[0]
    
    # Settings
    settings = ifcopenshell.geom.settings()
    
    # Process element
    shape = ifcopenshell.geom.create_shape(settings, element)
    
    # Element info
    print(f"GUID: {shape.guid}")
    print(f"ID: {shape.id}")
    print(f"Geometry ID: {shape.geometry.id}")

if __name__ == "__main__":
    create_shape_example()
