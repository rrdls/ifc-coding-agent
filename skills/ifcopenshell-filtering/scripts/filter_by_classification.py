"""
Filter IFC elements by classification.

Example: Find elements with specific Uniclass classification.
"""
import ifcopenshell
import ifcopenshell.util.selector

def filter_by_classification_example():
    """Demonstrate filtering elements by classification."""
    model = ifcopenshell.open('model.ifc')
    
    # Filter by classification reference (using regex)
    maintainable = ifcopenshell.util.selector.filter_elements(
        model,
        'IfcElement, classification=/Pr_.*/'
    )
    print(f"Found {len(maintainable)} maintainable products (Uniclass Pr_)")

if __name__ == "__main__":
    filter_by_classification_example()
