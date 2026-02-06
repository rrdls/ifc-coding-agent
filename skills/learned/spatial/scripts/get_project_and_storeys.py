"""
Generic spatial skill: get project name and count building storeys.

Purpose:
    Open an IFC model and return the project name and number of IfcBuildingStorey entities.

Functions:
    get_project_and_storeys(ifc_path: str) -> tuple[str, int]

Args:
    ifc_path (str): Path to the IFC file to read.

Returns:
    tuple[str, int]: (project_name, storey_count)

Example:
    >>> get_project_and_storeys('./projects/fnde/ARQ.ifc')
    ('My Project', 5)
"""
from typing import Tuple
import ifcopenshell


def get_project_and_storeys(ifc_path: str) -> Tuple[str, int]:
    """
    Get the IfcProject.Name and count IfcBuildingStorey entities in the model.

    Args:
        ifc_path (str): Path to the IFC file.

    Returns:
        Tuple[str, int]: A tuple where the first element is the project name (empty string if not found)
                         and the second element is the number of IfcBuildingStorey entities.

    Example:
        >>> get_project_and_storeys('./projects/fnde/ARQ.ifc')
        ('Project Name', 4)
    """
    model = ifcopenshell.open(ifc_path)

    # Get IfcProject
    projects = model.by_type('IfcProject')
    project_name = ''
    if projects:
        project = projects[0]
        # Some models may have no Name, use empty string
        project_name = project.Name if hasattr(project, 'Name') and project.Name is not None else ''

    # Count storeys
    storeys = model.by_type('IfcBuildingStorey')
    storey_count = len(storeys)

    return project_name, storey_count
