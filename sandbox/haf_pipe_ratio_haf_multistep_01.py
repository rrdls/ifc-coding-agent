from skills.learned.quantities.scripts.count_entities import count_entities


def pipe_segment_to_fitting_ratio(ifc_path: str) -> (int, int, float):
    """
    Compute counts of IfcPipeSegment and IfcPipeFitting and return their ratio.

    Purpose:
        Open an IFC model and count the number of IfcPipeSegment and IfcPipeFitting
        entities, then compute the ratio: segments / fittings. If fittings count is
        zero, ratio will be returned as float('inf').

    Args:
        ifc_path (str): Path to the IFC file.

    Returns:
        tuple: (segments_count (int), fittings_count (int), ratio (float))
               ratio = segments_count / fittings_count or float('inf') if fittings_count == 0

    Example:
        >>> pipe_segment_to_fitting_ratio('./projects/fnde/HAF.ifc')
        (120, 30, 4.0)
    """
    segments = count_entities(ifc_path, 'IfcPipeSegment')
    fittings = count_entities(ifc_path, 'IfcPipeFitting')
    ratio = float('inf') if fittings == 0 else segments / fittings
    return segments, fittings, ratio


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = './projects/fnde/HAF.ifc'

    segs, fits, r = pipe_segment_to_fitting_ratio(path)
    print(f"IfcPipeSegment count: {segs}")
    print(f"IfcPipeFitting count: {fits}")
    if fits == 0:
        print("Ratio (segments/fittings): Infinity (no fittings found)")
    else:
        print(f"Ratio (segments/fittings): {r}")
