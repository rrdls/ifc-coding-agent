"""
Combine filters using AND logic (comma separator).

Example: Find concrete walls with specific fire rating.
"""
import ifcopenshell
import ifcopenshell.util.selector

def combine_filters_and_example():
    """Demonstrate combining multiple filters with AND logic."""
    model = ifcopenshell.open('model.ifc')
    
    # AND: All conditions must be met (comma between filters)
    walls = ifcopenshell.util.selector.filter_elements(
        model,
        'IfcWall, material=concrete, /Pset_.*Common/.FireRating=2HR'
    )
    print(f"Found {len(walls)} concrete walls with 2HR fire rating (AND)")

if __name__ == "__main__":
    combine_filters_and_example()
