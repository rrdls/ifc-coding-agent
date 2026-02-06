from skills.learned.quantities.scripts.count_entities_grouped import count_entities_grouped


def list_wall_counts_by_storey_and_material(ifc_path: str) -> None:
    """Compute and print counts of IfcWall by storey and material.

    Args:
        ifc_path (str): Path to the IFC model.

    Returns:
        None: Prints the results in the format 'STOREY/Material: N'.

    Example:
        >>> list_wall_counts_by_storey_and_material('./projects/fnde/ARQ.ifc')
    """
    counts = count_entities_grouped(ifc_path, 'IfcWall')
    # Sort results by storey then material
    for key in sorted(counts.keys()):
        print(f"{key}: {counts[key]}")


if __name__ == '__main__':
    list_wall_counts_by_storey_and_material('./projects/fnde/ARQ.ifc')
