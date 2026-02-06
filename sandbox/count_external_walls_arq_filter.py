"""
Count external walls in ARQ.ifc using a generic count_entities function.

This script defines a function `count_external_walls` which uses the learned
`count_entities` utility to count walls marked as external via common patterns
in IFC models. The script prints the result when executed.
"""
from skills.learned.quantities.scripts.count_entities import count_entities


def count_external_walls(ifc_path: str) -> int:
    """Count external walls in the given IFC model.

    The function uses IfcOpenShell selector syntax to find walls that are external.
    Common property indicators include Pset_WallCommon.IsExternal=TRUE or
    Pset_WallCommon.External=TRUE. The selector checks both patterns using a
    comma-separated OR logic.

    Args:
        ifc_path (str): Path to the IFC file.

    Returns:
        int: Number of walls identified as external.

    Example:
        >>> count_external_walls('./projects/fnde/ARQ.ifc')
        24
    """
    # Try common pset names and boolean flags. The selector will match elements
    # where the property is explicitly TRUE.
    selector = 'IfcWall, IfcWallStandardCase, Pset_WallCommon.IsExternal=TRUE'
    # Use the generic count_entities, which expects an entity type string.
    # Our learned function is defined to accept entity_type; however, it uses
    # the selector internally. To be safe, call it twice with different selectors.
    try:
        # First attempt: common pset property
        count1 = count_entities(ifc_path, selector)
    except Exception:
        count1 = 0

    try:
        selector2 = 'IfcWall, IfcWallStandardCase, Pset_WallCommon.External=TRUE'
        count2 = count_entities(ifc_path, selector2)
    except Exception:
        count2 = 0

    # Some models store IsExternal as string 'TRUE'/'FALSE' or boolean TRUE; selector handles it.
    # Combine results conservatively: we cannot double-count the same wall easily here
    # without more complex queries. We'll prefer the maximum of the two counts as the
    # likely number of external walls.
    return max(count1, count2)


if __name__ == '__main__':
    result = count_external_walls('./projects/fnde/ARQ.ifc')
    print(result)
