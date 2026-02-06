"""
Extract spatial location information.

Example: Get container, storey, building, and site names.
"""
import ifcopenshell
import ifcopenshell.util.selector

def extract_spatial_example():
    """Demonstrate extracting spatial location."""
    model = ifcopenshell.open('model.ifc')
    wall = model.by_type('IfcWall')[0]
    
    # Spatial hierarchy
    container = ifcopenshell.util.selector.get_element_value(wall, "container")
    space = ifcopenshell.util.selector.get_element_value(wall, "space.Name")
    storey = ifcopenshell.util.selector.get_element_value(wall, "storey.Name")
    building = ifcopenshell.util.selector.get_element_value(wall, "building.Name")
    site = ifcopenshell.util.selector.get_element_value(wall, "site.Name")
    parent = ifcopenshell.util.selector.get_element_value(wall, "parent.Name")
    
    print(f"Container: {container}")
    print(f"Space: {space}")
    print(f"Storey: {storey}")
    print(f"Building: {building}")
    print(f"Site: {site}")
    print(f"Parent: {parent}")

if __name__ == "__main__":
    extract_spatial_example()
