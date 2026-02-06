import ifcopenshell
import ifcopenshell.util.selector
from typing import Dict, Tuple, List


def _extract_material_names_from_element(elem) -> List[str]:
    """Helper: attempt to extract one or more material names from an IFC element.

    The function uses selector paths that commonly appear in IFC models and
    falls back to a generic inspection of related material entities.
    """
    names = []
    try:
        # Try simple direct name
        name = ifcopenshell.util.selector.get_element_value(elem, "material.Name")
        if name:
            names.append(name)
    except Exception:
        pass

    try:
        # Try layered material first item
        name2 = ifcopenshell.util.selector.get_element_value(elem, "material.item.0.Name")
        if name2 and name2 not in names:
            names.append(name2)
    except Exception:
        pass

    try:
        # Try materials.count and iterate
        count = ifcopenshell.util.selector.get_element_value(elem, "materials.count")
        if isinstance(count, int) and count > 0:
            for i in range(count):
                try:
                    n = ifcopenshell.util.selector.get_element_value(elem, f"material.item.{i}.Name")
                    if n and n not in names:
                        names.append(n)
                except Exception:
                    continue
    except Exception:
        pass

    # If still empty, try to inspect IfcRelAssociatesMaterial relations directly
    if not names:
        try:
            # Many models attach IfcRelAssociatesMaterial to product or type
            rels = getattr(elem, 'HasAssociations', None) or []
            for rel in rels:
                try:
                    relating = getattr(rel, 'RelatingMaterial', None)
                    if relating is None:
                        continue
                    # If IfcMaterial
                    name = getattr(relating, 'Name', None)
                    if name and name not in names:
                        names.append(name)
                        continue
                    # If material list or layer set
                    # attempt common attributes
                    mats = getattr(relating, 'Materials', None) or getattr(relating, 'MaterialLayers', None) or []
                    for m in mats:
                        n = getattr(m, 'Name', None)
                        if n and n not in names:
                            names.append(n)
                except Exception:
                    continue
        except Exception:
            pass

    return names


def count_entities_grouped(ifc_path: str, entity_type: str) -> Dict[str, int]:
    """Count entities of a given IFC class grouped by storey and material.

    Purpose:
        Open an IFC model and count how many entities of `entity_type` exist for
        each combination of storey (location) and material name.

    Args:
        ifc_path (str): Path to the IFC file.
        entity_type (str): IFC entity class name to query (e.g., "IfcWall").

    Returns:
        Dict[str, int]: Mapping of keys formatted as "STOREY/Material" to counts.

    Example:
        >>> from skills.learned.quantities.scripts.count_entities_grouped import count_entities_grouped
        >>> counts = count_entities_grouped('./projects/fnde/ARQ.ifc', 'IfcWall')
        >>> print(list(counts.items())[:5])
    """
    model = ifcopenshell.open(ifc_path)
    elements = model.by_type(entity_type)

    results: Dict[str, int] = {}

    for elem in elements:
        # Get storey name (location)
        try:
            storey = ifcopenshell.util.selector.get_element_value(elem, "storey.Name")
        except Exception:
            storey = None
        if not storey:
            storey = "UNASSIGNED_STOREY"

        # Get material names (may be multiple)
        material_names = _extract_material_names_from_element(elem)
        if not material_names:
            material_names = ["UNASSIGNED_MATERIAL"]

        # For each material referenced by this element, increment the combination
        for mat in material_names:
            key = f"{storey}/{mat}"
            results[key] = results.get(key, 0) + 1

    return results
