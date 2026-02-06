from skills.learned.quantities.scripts.count_entities_by_storey import count_entities_by_storey


def count_sanitary_on_terreo(ifc_path: str) -> int:
    """
    Count IfcSanitaryTerminal instances located on the "TÉRREO" storey in the provided IFC model.

    Args:
        ifc_path (str): Path to the IFC file.

    Returns:
        int: Number of IfcSanitaryTerminal entities on the TÉRREO storey.

    Example:
        >>> count_sanitary_on_terreo("./projects/fnde/HAF.ifc")
        15
    """
    return count_entities_by_storey(ifc_path, "IfcSanitaryTerminal", "TÉRREO")


if __name__ == "__main__":
    result = count_sanitary_on_terreo("./projects/fnde/HAF.ifc")
    print(result)
