"""
Filter IFC elements by GlobalId.

Example: Find specific elements by their unique identifiers.
"""
import ifcopenshell
import ifcopenshell.util.selector

def filter_by_globalid_example():
    """Demonstrate filtering elements by GlobalId."""
    model = ifcopenshell.open('model.ifc')
    
    # Filter by single GlobalId
    element = ifcopenshell.util.selector.filter_elements(
        model,
        "325Q7Fhnf67OZC$$r43uzK"
    )
    print(f"Found {len(element)} element with specific GlobalId")
    
    # Filter by multiple GlobalIds
    elements = ifcopenshell.util.selector.filter_elements(
        model,
        "325Q7Fhnf67OZC$$r43uzK, 2VlJ7nbF5AFfQQuRvSWexT"
    )
    print(f"Found {len(elements)} elements with specified GlobalIds")
    
    # Exclude specific GlobalId
    filtered = ifcopenshell.util.selector.filter_elements(
        model,
        "IfcWall, ! 325Q7Fhnf67OZC$$r43uzK"
    )
    print(f"Found {len(filtered)} walls excluding specific GlobalId")

if __name__ == "__main__":
    filter_by_globalid_example()
