from skills.learned.spatial.scripts.count_elements_in_storey import count_elements_in_storey


def query_count_terreo(ifc_path: str) -> int:
    """Query wrapper to count elements on storey named 'TÉRREO'.

    Args:
        ifc_path: Path to IFC file

    Returns:
        int: Number of elements in the TÉRREO storey

    Example:
        >>> query_count_terreo('./projects/fnde/HEP.ifc')
        42
    """
    return count_elements_in_storey(ifc_path, 'TÉRREO')


if __name__ == '__main__':
    import sys
    path = './projects/fnde/HEP.ifc'
    result = query_count_terreo(path)
    print(result)
