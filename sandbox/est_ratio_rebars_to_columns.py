from skills.learned.quantities.scripts.count_entities import count_entities


def ratio_rebars_to_columns(ifc_path: str) -> float:
    """
    Calculate the ratio of IfcReinforcingBar count to IfcColumn count in an IFC model.

    Args:
        ifc_path (str): Path to the IFC file.

    Returns:
        float: The ratio (rebar_count / column_count). If column_count is zero, returns float('inf').

    Example:
        >>> ratio_rebars_to_columns('./projects/fnde/EST.ifc')
        2.5
    """
    rebars = count_entities(ifc_path, 'IfcReinforcingBar')
    columns = count_entities(ifc_path, 'IfcColumn')
    if columns == 0:
        return float('inf')
    return rebars / columns


if __name__ == '__main__':
    import sys
    path = './projects/fnde/EST.ifc'
    ratio = ratio_rebars_to_columns(path)
    rebars = count_entities(path, 'IfcReinforcingBar')
    columns = count_entities(path, 'IfcColumn')
    print(f"Reinforcing bars: {rebars}")
    print(f"Columns: {columns}")
    print(f"Ratio (rebars/columns): {ratio}")
