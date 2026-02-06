"""
Query IFC schema declarations.

Example: Load schema, list declarations, get by name.
"""
import ifcopenshell

def query_schema_example():
    """Demonstrate querying IFC schema."""
    # Load schema
    schema = ifcopenshell.schema_by_name("IFC4")
    
    # List all declarations (first 5)
    for decl in list(schema.declarations())[:5]:
        print(decl.name())
    
    # Get declaration by name
    ifcwall = schema.declaration_by_name("IfcWall")
    print(f"\nIfcWall: {ifcwall}")
    print(f"Is abstract: {ifcwall.is_abstract()}")

if __name__ == "__main__":
    query_schema_example()
