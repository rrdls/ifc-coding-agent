"""
Combine filters using OR logic (+ separator).

Example: Find concrete slabs OR doors (multiple groups).
"""
import ifcopenshell
import ifcopenshell.util.selector

def combine_filters_or_example():
    """Demonstrate combining multiple filter groups with OR logic."""
    model = ifcopenshell.open('model.ifc')
    
    # OR: Any group can match (+ between groups)
    elements = ifcopenshell.util.selector.filter_elements(
        model,
        'IfcSlab, material=concrete + IfcDoor'
    )
    print(f"Found {len(elements)} concrete slabs OR doors (OR)")
    
    # Complex OR with multiple groups
    complex_selection = ifcopenshell.util.selector.filter_elements(
        model,
        'IfcDoor, IfcWindow + IfcWall, IfcSlab, material=concrete + 325Q7Fhnf67OZC$$r43uzK'
    )
    print(f"Found {len(complex_selection)} elements matching complex OR criteria")

if __name__ == "__main__":
    combine_filters_or_example()
