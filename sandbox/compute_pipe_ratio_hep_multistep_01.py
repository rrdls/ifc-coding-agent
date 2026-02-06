from typing import Tuple
from skills.learned.quantities.scripts.count_entities import count_entities


def compute_pipe_ratio(ifc_path: str) -> Tuple[int, int, float]:
    """Compute the counts and ratio of pipe segments to pipe fittings in an IFC model.

    Args:
        ifc_path (str): Path to the IFC file.

    Returns:
        Tuple[int, int, float]: A tuple with (num_pipe_segments, num_pipe_fittings, ratio_segments_to_fittings).
            If num_pipe_fittings is zero, ratio_segments_to_fittings will be float('inf').

    Example:
        >>> compute_pipe_ratio('./projects/fnde/HEP.ifc')
        (120, 30, 4.0)
    """
    # Entity type names for pipe segments and fittings
    seg_type = 'IfcPipeSegment'
    fit_type = 'IfcPipeFitting'

    num_segments = count_entities(ifc_path, seg_type)
    num_fittings = count_entities(ifc_path, fit_type)

    if num_fittings == 0:
        ratio = float('inf')
    else:
        ratio = num_segments / num_fittings

    return num_segments, num_fittings, ratio


if __name__ == '__main__':
    import sys
    path = './projects/fnde/HEP.ifc'
    segs, fits, ratio = compute_pipe_ratio(path)
    # Print results as required by the execution environment
    print(f"PipeSegments: {segs}")
    print(f"PipeFittings: {fits}")
    if ratio == float('inf'):
        print("Ratio (segments:fittings): Infinity (no fittings found)")
    else:
        print(f"Ratio (segments:fittings): {ratio:.4f}")
