from typing import Tuple
from skills.learned.quantities.scripts.count_entities import count_entities
import ifcopenshell
import ifcopenshell.util.selector


def ratio_vedacao_walls(ifc_path: str) -> Tuple[int, int, float]:
    """Compute counts and ratio of walls with 'VEDAÇÃO EXTERNA' vs 'VEDAÇÃO INTERNA'.

    Args:
        ifc_path (str): Path to the IFC model file.

    Returns:
        Tuple[int, int, float]: (external_count, internal_count, ratio_external_to_internal).
            If internal_count is zero, ratio will be float('inf').

    Example:
        >>> external, internal, ratio = ratio_vedacao_walls('./projects/fnde/ARQ.ifc')
        >>> print(external, internal, ratio)
    """
    model = ifcopenshell.open(ifc_path)

    # Filter all walls
    walls = ifcopenshell.util.selector.filter_elements(model, "IfcWall")

    external_count = 0
    internal_count = 0

    # Check common property set names that might contain the wall classification
    # We'll inspect the Name and all property sets for a matching value.
    for w in walls:
        found = False
        # Check Name or Type
        name = getattr(w, 'Name', '') or ''
        if name and 'VEDA' in name.upper():
            if 'VEDAÇÃO EXTERNA' in name.upper() or 'VEDACAO EXTERNA' in name.upper():
                external_count += 1
                continue
            if 'VEDAÇÃO INTERNA' in name.upper() or 'VEDACAO INTERNA' in name.upper():
                internal_count += 1
                continue

        # Check property sets for properties with matching value
        for rel in w.IsDefinedBy:
            try:
                pset = rel.RelatingPropertyDefinition
            except Exception:
                continue
            # If it's a property single or set
            if pset is None:
                continue
            # Pset may have attribute .HasProperties
            props = getattr(pset, 'HasProperties', [])
            for p in props:
                # PropertySingleValue has .NominalValue or .Name
                val = None
                namep = getattr(p, 'Name', '') or ''
                # Try common value attributes
                for attr in ('NominalValue', 'Value', 'UpperValue', 'LowerValue'):
                    if hasattr(p, attr):
                        v = getattr(p, attr)
                        # If it's an IFC value, get .wrappedValue
                        val = getattr(v, 'wrappedValue', None) if v is not None else None
                        if val is None:
                            val = v
                        if val is not None:
                            break
                textval = '' if val is None else str(val).upper()
                # Search for keywords
                if 'VEDAÇÃO EXTERNA' in textval or 'VEDACAO EXTERNA' in textval:
                    external_count += 1
                    found = True
                    break
                if 'VEDAÇÃO INTERNA' in textval or 'VEDACAO INTERNA' in textval:
                    internal_count += 1
                    found = True
                    break
            if found:
                break

    ratio = float('inf') if internal_count == 0 else external_count / internal_count
    return external_count, internal_count, ratio


if __name__ == '__main__':
    ext, inter, ratio = ratio_vedacao_walls('./projects/fnde/ARQ.ifc')
    print(f"External walls (VEDAÇÃO EXTERNA): {ext}")
    print(f"Internal walls (VEDAÇÃO INTERNA): {inter}")
    print(f"Ratio (external / internal): {ratio}")
