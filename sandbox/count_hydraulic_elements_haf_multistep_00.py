from typing import Tuple
from skills.learned.quantities.scripts.count_entities import count_entities


def count_hydraulic_elements(ifc_path: str) -> Tuple[int, int, int, int]:
    """
    Count hydraulic elements (pipes, fittings, valves) in the given IFC model.

    Args:
        ifc_path (str): Path to the IFC file.

    Returns:
        Tuple[int, int, int, int]: Counts for (pipes, fittings, valves, total).

    Example:
        >>> count_hydraulic_elements('./projects/fnde/HAF.ifc')
        (120, 45, 10, 175)
    """
    pipes = count_entities(ifc_path, 'IfcPipeSegment')
    fittings = count_entities(ifc_path, 'IfcPipeFitting')
    valves = count_entities(ifc_path, 'IfcValve')
    total = pipes + fittings + valves
    return pipes, fittings, valves, total


if __name__ == '__main__':
    ifc_file = './projects/fnde/HAF.ifc'
    pipes, fittings, valves, total = count_hydraulic_elements(ifc_file)
    print(f'Pipes: {pipes}')
    print(f'Fittings: {fittings}')
    print(f'Valves: {valves}')
    print(f'Total hydraulic elements (pipes + fittings + valves): {total}')
