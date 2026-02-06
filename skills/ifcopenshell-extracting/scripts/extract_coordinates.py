"""
Extract coordinate information from IFC elements.

Example: Get x, y, z and geospatial coordinates.
"""
import ifcopenshell
import ifcopenshell.util.selector

def extract_coordinates_example():
    """Demonstrate extracting coordinate values."""
    model = ifcopenshell.open('model.ifc')
    element = model.by_type('IfcPump')[0]
    
    # Local coordinates
    x = ifcopenshell.util.selector.get_element_value(element, "x")
    y = ifcopenshell.util.selector.get_element_value(element, "y")
    z = ifcopenshell.util.selector.get_element_value(element, "z")
    
    print(f"Local: ({x}, {y}, {z})")
    
    # Geospatial coordinates
    easting = ifcopenshell.util.selector.get_element_value(element, "easting")
    northing = ifcopenshell.util.selector.get_element_value(element, "northing")
    elevation = ifcopenshell.util.selector.get_element_value(element, "elevation")
    
    print(f"Geo: ({easting}, {northing}, {elevation})")

if __name__ == "__main__":
    extract_coordinates_example()
