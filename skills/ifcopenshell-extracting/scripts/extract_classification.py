"""
Extract classification, group, and system information.

Example: Get classification references and group assignments.
"""
import ifcopenshell
import ifcopenshell.util.selector

def extract_classification_example():
    """Demonstrate extracting classification and groups."""
    model = ifcopenshell.open('model.ifc')
    element = model.by_type('IfcElement')[0]
    
    # Classifications and groups
    classification = ifcopenshell.util.selector.get_element_value(element, "classification")
    group = ifcopenshell.util.selector.get_element_value(element, "group")
    system = ifcopenshell.util.selector.get_element_value(element, "system")
    zone = ifcopenshell.util.selector.get_element_value(element, "zone")
    
    print(f"Classification: {classification}")
    print(f"Group: {group}")
    print(f"System: {system}")
    print(f"Zone: {zone}")

if __name__ == "__main__":
    extract_classification_example()
