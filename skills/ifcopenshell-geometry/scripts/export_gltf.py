"""
Export geometry to glTF format.

Example: Serialize IFC model to glb file.
"""
import multiprocessing
import ifcopenshell
import ifcopenshell.geom

def export_gltf_example():
    """Demonstrate glTF export."""
    model = ifcopenshell.open('model.ifc')
    
    # Settings for glTF
    settings = ifcopenshell.geom.settings()
    settings.set("dimensionality", ifcopenshell.ifcopenshell_wrapper.CURVES_SURFACES_AND_SOLIDS)
    settings.set("apply-default-materials", True)
    
    # Serializer settings
    ser_settings = ifcopenshell.geom.serializer_settings()
    ser_settings.set("use-element-guids", True)
    
    # Create glTF serializer
    serialiser = ifcopenshell.geom.serializers.gltf(
        "output.glb", settings, ser_settings
    )
    serialiser.setFile(model)
    serialiser.setUnitNameAndMagnitude("METER", 1.0)
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
    print("Exported to output.glb")

if __name__ == "__main__":
    export_gltf_example()
