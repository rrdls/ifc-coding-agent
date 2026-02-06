from typing import Tuple
from skills.learned.spatial.scripts.get_project_and_storeys import get_project_and_storeys


def query_project_and_storeys(ifc_path: str) -> Tuple[str, int]:
    """
    Query wrapper that returns the project name and storey count for a given IFC file.

    Args:
        ifc_path (str): Path to the IFC file.

    Returns:
        Tuple[str, int]: (project_name, storey_count)

    Example:
        >>> query_project_and_storeys('./projects/fnde/ARQ.ifc')
        ('Project Name', 4)
    """
    return get_project_and_storeys(ifc_path)


if __name__ == '__main__':
    project_name, storey_count = query_project_and_storeys('./projects/fnde/ARQ.ifc')
    print(f"Project name: {project_name}")
    print(f"Storey count: {storey_count}")
