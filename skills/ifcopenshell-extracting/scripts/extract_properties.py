"""
Extract property set values from IFC elements.

Example: Get values from Pset_WallCommon and other psets.
"""
import ifcopenshell
import ifcopenshell.util.selector

def extract_properties_example():
    """Demonstrate extracting property set values."""
    model = ifcopenshell.open('model.ifc')
    wall = model.by_type('IfcWall')[0]
    
    # Specific property
    status = ifcopenshell.util.selector.get_element_value(
        wall, "Pset_WallCommon.Status"
    )
    print(f"Status: {status}")
    
    # Property with regex for pset name
    fire_rating = ifcopenshell.util.selector.get_element_value(
        wall, "/Pset_.*Common/.FireRating"
    )
    print(f"Fire Rating: {fire_rating}")

if __name__ == "__main__":
    extract_properties_example()
