"""
Navigate class hierarchy in IFC schema.

Example: Get supertype, subtypes, inheritance chain.
"""
import ifcopenshell

def class_hierarchy_example():
    """Demonstrate class hierarchy navigation."""
    schema = ifcopenshell.schema_by_name("IFC4")
    ifcwall = schema.declaration_by_name("IfcWall")
    
    # Supertype (parent class)
    print(f"Supertype: {ifcwall.supertype()}")  # IfcBuildingElement
    
    # Full inheritance chain
    current = ifcwall.supertype()
    chain = [ifcwall.name()]
    while current:
        chain.append(current.name())
        current = current.supertype()
    print(f"Inheritance: {' <- '.join(chain)}")
    
    # Subtypes (child classes)
    print(f"Subtypes: {[s.name() for s in ifcwall.subtypes()]}")

if __name__ == "__main__":
    class_hierarchy_example()
