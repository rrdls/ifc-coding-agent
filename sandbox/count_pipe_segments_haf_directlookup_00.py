"""
Count IfcPipeSegment entities in the provided HAF.ifc model.

This script imports the generic count_entities function from skills.learned.quantities and
uses it to count IfcPipeSegment instances in the model.

Usage:
    python3 sandbox/count_pipe_segments_haf_directlookup_00.py
"""
from skills.learned.quantities.scripts.count_entities import count_entities


def count_pipe_segments(ifc_path: str) -> int:
    """Count pipe segment elements (IfcPipeSegment) in an IFC file.

    Args:
        ifc_path (str): Path to the IFC file.

    Returns:
        int: Number of IfcPipeSegment entities in the model.

    Example:
        >>> count_pipe_segments('./projects/fnde/HAF.ifc')
        123
    """
    return count_entities(ifc_path, 'IfcPipeSegment')


if __name__ == '__main__':
    path = './projects/fnde/HAF.ifc'
    total = count_pipe_segments(path)
    print(total)
