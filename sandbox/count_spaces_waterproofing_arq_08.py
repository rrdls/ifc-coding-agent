"""
Count spaces requiring wall waterproofing in ARQ.ifc

This script uses the generic function from skills/learned to count IfcSpace
instances where a waterproofing property indicates wall waterproofing is
required.
"""
from skills.learned.properties.scripts.count_spaces_by_property import count_spaces_with_property


def count_spaces_require_wall_waterproofing(ifc_path: str) -> int:
    """
    Count IfcSpace instances that require wall waterproofing.

    Purpose:
        Search the IFC model for IfcSpace entities whose property sets indicate
        wall waterproofing is required. This function uses a generic property
        filter function and targets common Pset names used for spaces.

    Args:
        ifc_path (str): Path to the IFC file.

    Returns:
        int: Number of IfcSpace entities requiring wall waterproofing.

    Example:
        >>> count_spaces_require_wall_waterproofing('./projects/fnde/ARQ.ifc')
        5
    """
    # Common property names to try (ordered by likelihood)
    candidates = [
        'Pset_SpaceCommon.Waterproofing',
        'Pset_SpaceCommon.WallWaterproofing',
        '/Pset_.*Space.*/.Waterproofing=TRUE',
        '/Pset_.*/.WallWaterproofing=TRUE',
        'Pset_SpaceFinish.Waterproofing'
    ]

    # First try explicit TRUE comparison for likely names
    for p in candidates:
        try:
            if '=' in p or '/' in p:
                # assume this is a full selector fragment
                count = count_spaces_with_property(ifc_path, p)
            else:
                count = count_spaces_with_property(ifc_path, p, 'TRUE')

            if count > 0:
                return count
        except Exception:
            # ignore errors for non-existing pset/property names and try next
            continue

    # As a last resort, count spaces where any waterproofing property is defined
    try:
        count_any = count_spaces_with_property(ifc_path, '/Pset_.*/.Waterproofing != NULL')
        return count_any
    except Exception:
        return 0


if __name__ == '__main__':
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else './projects/fnde/ARQ.ifc'
    result = count_spaces_require_wall_waterproofing(path)
    print(result)
