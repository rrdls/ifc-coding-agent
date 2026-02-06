"""
Filter IFC elements by type.

Example: Find walls of a specific type on a specific level.
"""
import ifcopenshell
import ifcopenshell.util.selector

def filter_by_type_example():
    """Demonstrate filtering elements by type."""
    model = ifcopenshell.open('model.ifc')
    
    # Filter by type and location
    walls = ifcopenshell.util.selector.filter_elements(
        model,
        'IfcWall, type=WT01, location="Level 3"'
    )
    print(f"Found {len(walls)} walls of type WT01 on Level 3")

if __name__ == "__main__":
    filter_by_type_example()
