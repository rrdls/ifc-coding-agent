from skills.learned.quantities.scripts.count_entities import count_entities


def count_beams_in_model(ifc_path: str) -> int:
    """Count the number of IfcBeam entities in the specified IFC model.

    Args:
        ifc_path (str): Path to the IFC file.

    Returns:
        int: Number of IfcBeam entities found in the model.

    Example:
        >>> count = count_beams_in_model('./projects/fnde/EST.ifc')
        >>> print(isinstance(count, int))
        True
    """
    return count_entities(ifc_path, "IfcBeam")


if __name__ == "__main__":
    path = './projects/fnde/EST.ifc'
    total = count_beams_in_model(path)
    print(total)
