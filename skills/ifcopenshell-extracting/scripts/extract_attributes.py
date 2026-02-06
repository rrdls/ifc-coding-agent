"""
Extract basic attributes from IFC elements.

Example: Get class, id, Name, and predefined_type.
"""
import ifcopenshell
import ifcopenshell.util.selector

def extract_attributes_example():
    """Demonstrate extracting basic attributes."""
    model = ifcopenshell.open('model.ifc')
    wall = model.by_type('IfcWall')[0]
    
    # Basic attributes
    ifc_class = ifcopenshell.util.selector.get_element_value(wall, "class")
    step_id = ifcopenshell.util.selector.get_element_value(wall, "id")
    name = ifcopenshell.util.selector.get_element_value(wall, "Name")
    predefined = ifcopenshell.util.selector.get_element_value(wall, "predefined_type")
    
    print(f"Class: {ifc_class}")
    print(f"ID: {step_id}")
    print(f"Name: {name}")
    print(f"Predefined Type: {predefined}")

if __name__ == "__main__":
    extract_attributes_example()
