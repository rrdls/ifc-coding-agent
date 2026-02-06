"""
Extract element type information.

Example: Get type name and occurrence count.
"""
import ifcopenshell
import ifcopenshell.util.selector

def extract_type_example():
    """Demonstrate extracting type information."""
    model = ifcopenshell.open('model.ifc')
    wall = model.by_type('IfcWall')[0]
    
    # Type name
    type_name = ifcopenshell.util.selector.get_element_value(wall, "type.Name")
    print(f"Type Name: {type_name}")
    
    # Count of occurrences
    type_count = ifcopenshell.util.selector.get_element_value(wall, "types.count")
    print(f"Type Occurrences: {type_count}")

if __name__ == "__main__":
    extract_type_example()
