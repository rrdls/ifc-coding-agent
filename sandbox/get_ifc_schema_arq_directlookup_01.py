import ifcopenshell
from typing import Any


def get_ifc_schema(ifc_path: str) -> str:
    """
    Get the IFC schema version used in an IFC file.

    Args:
        ifc_path (str): Path to the IFC file.

    Returns:
        str: The IFC schema version string (e.g., "IFC4", "IFC2X3"). If the schema
             cannot be determined, returns an empty string.

    Example:
        >>> get_ifc_schema("./projects/fnde/ARQ.ifc")
        'IFC4'
    """
    model = ifcopenshell.open(ifc_path)
    # ifcopenshell file objects expose the schema attribute
    schema = getattr(model, "schema", None)
    if schema is None:
        # Fallback to header information if available
        header = getattr(model, "header", None)
        if header and isinstance(header, dict):
            # header may contain "FileSchema" or similar
            fs = header.get("FileSchema") or header.get("file_schema")
            if isinstance(fs, (list, tuple)) and len(fs) > 0:
                # fs may be like ['IFC4'] or ['IFC', '4']
                return str(fs[0])
        return ""
    return str(schema)


if __name__ == "__main__":
    path = "./projects/fnde/ARQ.ifc"
    schema = get_ifc_schema(path)
    print(schema)
