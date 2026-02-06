from typing import List
from skills.learned.quantities.scripts.find_entities import find_entities


def count_flow_terminals(ifc_path: str) -> int:
    """
    Count total flow terminals in an IFC model, including sanitary, waste, and stack terminals.

    Args:
        ifc_path (str): Path to the IFC file.

    Returns:
        int: Total number of flow terminal entities found.

    Example:
        >>> count = count_flow_terminals('./projects/fnde/HEP.ifc')
    """
    selectors: List[str] = [
        'IfcFlowTerminal',
        'IfcSanitaryTerminal',
        'IfcWasteTerminal',
        'IfcStackTerminal'
    ]
    entities = find_entities(ifc_path, selectors)
    return len(entities)


if __name__ == '__main__':
    total = count_flow_terminals('./projects/fnde/HEP.ifc')
    print(total)
