"""
Filter IFC elements by spatial location.

Example: Find pumps on a specific building storey.
"""
import ifcopenshell
import ifcopenshell.util.selector

def filter_by_location_example():
    """Demonstrate filtering elements by spatial location."""
    model = ifcopenshell.open('model.ifc')
    
    # Filter by location (includes spaces within the level)
    pumps = ifcopenshell.util.selector.filter_elements(
        model,
        'IfcPump, location="Level 3"'
    )
    print(f"Found {len(pumps)} pumps on Level 3")

if __name__ == "__main__":
    filter_by_location_example()
