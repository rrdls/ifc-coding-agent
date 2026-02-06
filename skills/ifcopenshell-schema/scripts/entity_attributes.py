"""
Get entity attributes from schema.

Example: Direct attributes, all attributes, inverse attributes.
"""
import ifcopenshell

def entity_attributes_example():
    """Demonstrate getting entity attributes."""
    schema = ifcopenshell.schema_by_name("IFC4")
    ifcwall = schema.declaration_by_name("IfcWall")
    
    # Direct attributes (defined in this class only)
    print("Direct attributes:")
    for attr in ifcwall.attributes():
        print(f"  - {attr.name()}")
    
    # All attributes (including inherited)
    print("\nAll attributes:")
    for attr in ifcwall.all_attributes():
        print(f"  - {attr.name()}: {attr.type_of_attribute()}")
    
    # Inverse attributes
    print("\nInverse attributes:")
    for attr in ifcwall.all_inverse_attributes():
        print(f"  - {attr.name()}")

if __name__ == "__main__":
    entity_attributes_example()
