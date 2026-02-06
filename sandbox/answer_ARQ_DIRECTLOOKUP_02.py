from skills.learned.quantities.scripts.get_length_units import get_length_units


def length_units_in_arq(ifc_path: str) -> str:
    """
    Return the length units used in the provided IFC file.

    Args:
        ifc_path (str): Relative path to the IFC model.

    Returns:
        str: Description of length units found in the model, or 'NOT FOUND'.

    Example:
        >>> length_units_in_arq('./projects/fnde/ARQ.ifc')
        'METRE'
    """
    return get_length_units(ifc_path)


if __name__ == '__main__':
    result = length_units_in_arq('./projects/fnde/ARQ.ifc')
    print(result)
