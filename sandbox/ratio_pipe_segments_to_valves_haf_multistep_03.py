from typing import Tuple
from skills.learned.quantities.scripts.count_entities import count_entities


def ratio_pipe_segments_to_valves(ifc_path: str) -> Tuple[int, int, float]:
    """Compute counts and ratio of IfcPipeSegment to IfcValve in an IFC model.

    Args:
        ifc_path (str): Path to the IFC (.ifc) file.

    Returns:
        Tuple[int, int, float]: A tuple with (pipe_segments_count, valves_count, ratio).
            - pipe_segments_count: Number of IfcPipeSegment entities
            - valves_count: Number of IfcValve entities
            - ratio: pipe_segments_count / valves_count if valves_count > 0, else float('inf')

    Example:
        >>> ratio_pipe_segments_to_valves('./projects/fnde/HAF.ifc')
        (120, 30, 4.0)
    """
    pipe_count = count_entities(ifc_path, 'IfcPipeSegment')
    valve_count = count_entities(ifc_path, 'IfcValve')

    if valve_count == 0:
        ratio = float('inf')
    else:
        ratio = pipe_count / valve_count

    return pipe_count, valve_count, ratio


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = './projects/fnde/HAF.ifc'

    pipes, valves, ratio = ratio_pipe_segments_to_valves(path)
    if valves == 0:
        print(f"Pipe segments: {pipes}\nValves: {valves}\nRatio (pipes/valves): undefined (no valves)")
    else:
        print(f"Pipe segments: {pipes}\nValves: {valves}\nRatio (pipes/valves): {ratio}")
