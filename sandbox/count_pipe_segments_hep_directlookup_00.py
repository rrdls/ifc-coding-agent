"""
Count IfcPipeSegment entities in the provided IFC model (HEP.ifc).

This script imports the generic count_entities function from the learned skills
and defines a wrapper function with a full docstring, then prints the result
when executed as a script.
"""
from typing import Any
from skills.learned.quantities.scripts.count_entities import count_entities


def count_pipe_segments(ifc_path: str) -> int:
    """Count IfcPipeSegment entities in an IFC model.

    Args:
        ifc_path (str): Path to the IFC file to open.

    Returns:
        int: Number of IfcPipeSegment entities found in the model.

    Example:
        >>> count_pipe_segments('./projects/fnde/HEP.ifc')
        123
    """
    return count_entities(ifc_path, 'IfcPipeSegment')


if __name__ == '__main__':
    model_path = './projects/fnde/HEP.ifc'
    total = count_pipe_segments(model_path)
    print(total)
