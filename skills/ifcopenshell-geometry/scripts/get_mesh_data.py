"""
Get vertices, edges, and faces from geometry.

Example: Access mesh data.
"""
import ifcopenshell
import ifcopenshell.geom
import ifcopenshell.util.shape

def get_mesh_data_example():
    """Demonstrate accessing mesh data."""
    model = ifcopenshell.open('model.ifc')
    element = model.by_type('IfcWall')[0]
    
    settings = ifcopenshell.geom.settings()
    shape = ifcopenshell.geom.create_shape(settings, element)
    
    # Raw data (flat lists)
    verts = shape.geometry.verts  # [x1, y1, z1, x2, y2, z2, ...]
    edges = shape.geometry.edges  # [e1v1, e1v2, e2v1, e2v2, ...]
    faces = shape.geometry.faces  # [f1v1, f1v2, f1v3, ...]
    
    # Grouped with numpy
    grouped_verts = ifcopenshell.util.shape.get_vertices(shape.geometry)
    grouped_edges = ifcopenshell.util.shape.get_edges(shape.geometry)
    grouped_faces = ifcopenshell.util.shape.get_faces(shape.geometry)
    
    print(f"Vertices: {len(grouped_verts)}")
    print(f"Edges: {len(grouped_edges)}")
    print(f"Faces: {len(grouped_faces)}")

if __name__ == "__main__":
    get_mesh_data_example()
