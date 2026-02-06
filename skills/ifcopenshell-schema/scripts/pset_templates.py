"""
Query property set templates from buildingSMART.

Example: Get applicable psets for an entity class.
"""
import ifcopenshell.util.pset

def pset_templates_example():
    """Demonstrate querying pset templates."""
    # Load templates for IFC4
    templates = ifcopenshell.util.pset.PsetQto("IFC4")
    
    # Get applicable pset names
    names = templates.get_applicable_names("IfcWall")
    print("Applicable psets for IfcWall:")
    for name in names[:5]:  # First 5
        print(f"  - {name}")
    
    # Get specific pset template
    pset = templates.get_by_name("Pset_WallCommon")
    print(f"\nPset_WallCommon: {pset.Description}")
    
    # List properties in template
    if hasattr(pset, 'HasPropertyTemplates'):
        print("Properties:")
        for prop in pset.HasPropertyTemplates:
            print(f"  - {prop.Name}: {prop.PrimaryMeasureType}")

if __name__ == "__main__":
    pset_templates_example()
