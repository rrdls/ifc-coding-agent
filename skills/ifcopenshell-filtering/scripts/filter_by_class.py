"""
Filter IFC elements by class.

Example: Find all walls and slabs in a model.
"""
import ifcopenshell
import ifcopenshell.util.selector

def filter_by_class_example():
    """Demonstrate filtering elements by IFC class."""
    # Example with fictional model
    model = ifcopenshell.open('model.ifc')
    
    # Filter by single class
    walls = ifcopenshell.util.selector.filter_elements(model, "IfcWall")
    print(f"Found {len(walls)} walls")
    
    # Filter by multiple classes
    elements = ifcopenshell.util.selector.filter_elements(
        model, 
        "IfcWall, IfcSlab"
    )
    print(f"Found {len(elements)} walls and slabs")
    
    # Exclude specific class
    non_walls = ifcopenshell.util.selector.filter_elements(
        model,
        "IfcElement, ! IfcWall"
    )
    print(f"Found {len(non_walls)} elements (excluding walls)")

if __name__ == "__main__":
    filter_by_class_example()
