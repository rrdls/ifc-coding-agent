"""
Use geometry iterator for batch processing.

Example: Process all elements efficiently.
"""
import multiprocessing
import ifcopenshell
import ifcopenshell.geom

def geometry_iterator_example():
    """Demonstrate batch geometry processing."""
    model = ifcopenshell.open('model.ifc')
    settings = ifcopenshell.geom.settings()
    
    # Create iterator with multiprocessing
    iterator = ifcopenshell.geom.iterator(
        settings, model, multiprocessing.cpu_count()
    )
    
    if iterator.initialize():
        count = 0
        while True:
            shape = iterator.get()
            element = model.by_id(shape.id)
            
            # Process geometry...
            verts = shape.geometry.verts
            faces = shape.geometry.faces
            
            count += 1
            if not iterator.next():
                break
        
        print(f"Processed {count} elements")

if __name__ == "__main__":
    geometry_iterator_example()
