"""
Filter IFC elements by attribute values.

Example: Find doors with specific names using exact match or regex.
"""
import ifcopenshell
import ifcopenshell.util.selector

def filter_by_attribute_example():
    """Demonstrate filtering elements by attribute values."""
    model = ifcopenshell.open('model.ifc')
    
    # Filter by exact attribute value
    doors = ifcopenshell.util.selector.filter_elements(
        model,
        'IfcDoor, Name=D01'
    )
    print(f"Found {len(doors)} doors named 'D01'")
    
    # Filter by regex pattern
    doors_pattern = ifcopenshell.util.selector.filter_elements(
        model,
        'IfcDoor, Name=/D[0-9]{2}/'
    )
    print(f"Found {len(doors_pattern)} doors matching pattern D[0-9]{{2}}")

if __name__ == "__main__":
    filter_by_attribute_example()
