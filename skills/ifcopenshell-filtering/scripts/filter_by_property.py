"""
Filter IFC elements by property set values.

Example: Find walls with specific fire rating or load bearing properties.
"""
import ifcopenshell
import ifcopenshell.util.selector

def filter_by_property_example():
    """Demonstrate filtering elements by property set values."""
    model = ifcopenshell.open('model.ifc')
    
    # Filter by specific property value
    walls = ifcopenshell.util.selector.filter_elements(
        model,
        'IfcWall, Pset_WallCommon.FireRating=2HR'
    )
    print(f"Found {len(walls)} walls with 2HR fire rating")
    
    # Filter using regex for pset name
    structural = ifcopenshell.util.selector.filter_elements(
        model,
        'IfcWall, IfcColumn, IfcBeam, /Pset_.*Common/.LoadBearing=TRUE'
    )
    print(f"Found {len(structural)} load-bearing structural elements")
    
    # Filter where property is not null
    rated_elements = ifcopenshell.util.selector.filter_elements(
        model,
        'IfcElement, /Pset_.*Common/.FireRating != NULL'
    )
    print(f"Found {len(rated_elements)} elements with fire rating defined")

if __name__ == "__main__":
    filter_by_property_example()
