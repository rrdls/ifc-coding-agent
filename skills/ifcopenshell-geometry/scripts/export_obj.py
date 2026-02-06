"""
Export geometry to OBJ format.

Example: Serialize IFC model to OBJ and MTL files.
"""
import multiprocessing
import ifcopenshell
import ifcopenshell.geom

def export_obj_example():
    """Demonstrate OBJ export."""
    model = ifcopenshell.open('model.ifc')
    
    # Settings for OBJ
    settings = ifcopenshell.geom.settings()
    settings.set("dimensionality", ifcopenshell.ifcopenshell_wrapper.CURVES_SURFACES_AND_SOLIDS)
    settings.set("apply-default-materials", True)
    settings.set("use-world-coords", True)
    
    # Serializer settings
    ser_settings = ifcopenshell.geom.serializer_settings()
    ser_settings.set("use-element-guids", True)
    
    # Create OBJ serializer (with MTL for materials)
    serialiser = ifcopenshell.geom.serializers.obj(
        'output.obj', 'output.mtl', settings, ser_settings
    )
    serialiser.setFile(model)
    serialiser.writeHeader()
    
    # Iterate and write
    iterator = ifcopenshell.geom.iterator(
        settings, model, multiprocessing.cpu_count()
    )
    
    if iterator.initialize():
        while True:
            serialiser.write(iterator.get())
            if not iterator.next():
                break
    
    serialiser.finalize()
    print("Exported to output.obj")

if __name__ == "__main__":
    export_obj_example()
