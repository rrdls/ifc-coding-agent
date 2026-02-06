"""
Compute the percentage of IfcFooting elements that are of type PAD_FOOTING in the provided IFC model.

This script defines a function `percentage_pad_footings` which opens the IFC file, counts all IfcFooting
entities and counts how many have a PredefinedType, ObjectType or Name indicating PAD_FOOTING. It prints the counts
and percentage when run as main.
"""
from typing import Tuple
from skills.learned.quantities.scripts.count_entities import count_entities
import ifcopenshell


def percentage_pad_footings(ifc_path: str) -> Tuple[int, int, float]:
    """Calculate counts and percentage of pad footings.

    Args:
        ifc_path (str): Path to the IFC model file.

    Returns:
        Tuple[int, int, float]: (total_footings, pad_footings, percentage_pad)
            - total_footings: Total number of IfcFooting entities found.
            - pad_footings: Number of IfcFooting entities whose Type or Name indicates PAD_FOOTING.
            - percentage_pad: pad_footings / total_footings * 100.0 (0.0 if total is 0)

    Example:
        >>> percentage_pad_footings('./projects/fnde/EST.ifc')
        (10, 7, 70.0)
    """
    model = ifcopenshell.open(ifc_path)

    # Count total footings using generic helper
    total = count_entities(ifc_path, 'IfcFooting')

    # Find all IfcFooting entities and inspect their attributes
    footings = model.by_type('IfcFooting')
    pad_count = 0
    for f in footings:
        # Check for PredefinedType, ObjectType, or Name mentioning PAD_FOOTING
        dtype = getattr(f, 'PredefinedType', None)
        otype = getattr(f, 'ObjectType', None)
        name = getattr(f, 'Name', None)
        if isinstance(dtype, str) and dtype.upper() == 'PAD_FOOTING':
            pad_count += 1
            continue
        if isinstance(otype, str) and 'PAD_FOOTING' in otype.upper():
            pad_count += 1
            continue
        if isinstance(name, str) and 'PAD_FOOTING' in name.upper():
            pad_count += 1
            continue
        # Also check linked type object if present
        if hasattr(f, 'ObjectType') and getattr(f, 'ObjectType', None) is not None:
            # Already checked ObjectType string; if it's a referenced type, check its Name or PredefinedType
            ref = getattr(f, 'ObjectType')
            try:
                ref_name = getattr(ref, 'Name', None)
                ref_pt = getattr(ref, 'PredefinedType', None)
                if isinstance(ref_name, str) and 'PAD_FOOTING' in ref_name.upper():
                    pad_count += 1
                    continue
                if isinstance(ref_pt, str) and ref_pt.upper() == 'PAD_FOOTING':
                    pad_count += 1
                    continue
            except Exception:
                pass
    percentage = (pad_count / total * 100.0) if total > 0 else 0.0
    return total, pad_count, percentage


if __name__ == '__main__':
    total, pad, pct = percentage_pad_footings('./projects/fnde/EST.ifc')
    print(f"Total IfcFooting: {total}")
    print(f"PAD_FOOTING count: {pad}")
    print(f"Percentage PAD_FOOTING: {pct:.2f}%")
