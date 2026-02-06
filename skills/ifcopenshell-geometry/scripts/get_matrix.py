"""
Get transformation matrix from shape.

Example: Extract position and rotation.
"""
import ifcopenshell
import ifcopenshell.geom
import ifcopenshell.util.shape

def get_matrix_example():
    """Demonstrate accessing transformation matrix."""
    model = ifcopenshell.open('model.ifc')
    element = model.by_type('IfcWall')[0]
    
    settings = ifcopenshell.geom.settings()
    shape = ifcopenshell.geom.create_shape(settings, element)
    
    # Raw matrix (4x4 flat list)
    matrix = shape.transformation.matrix
    
    # As numpy array (for math operations)
    np_matrix = ifcopenshell.util.shape.get_shape_matrix(shape)
    
    # Extract position (last column)
    location = np_matrix[:, 3][0:3]
    print(f"Position: {location}")

if __name__ == "__main__":
    get_matrix_example()
