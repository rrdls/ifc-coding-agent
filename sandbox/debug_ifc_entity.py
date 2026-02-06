"""
Debug script to inspect IFC entity object methods/attributes to discover how to read entity type names.
"""
import ifcopenshell


def inspect_first_entity(ifc_path: str):
    model = ifcopenshell.open(ifc_path)
    elems = model.by_type('IfcElement')
    if not elems:
        print('No IfcElement found')
        return
    e = elems[0]
    print('str(e):', str(e))
    print('repr(e):', repr(e))
    print('dir(e):')
    for a in dir(e)[:200]:
        print(a)


if __name__ == '__main__':
    inspect_first_entity('./projects/fnde/ELE.ifc')
