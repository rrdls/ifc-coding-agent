"""
Query ARQ_FILTEREDAGGREGATION_12
Check whether any wall material contains the word 'TIJOLO'.
"""
from typing import List, Dict
import ifcopenshell


def _extract_material_names(mat) -> List[str]:
    """Extract human-readable material names from various IfcMaterial* entities.

    Args:
        mat: An IfcOpenShell entity representing a material (can be None).

    Returns:
        List[str]: A list of material names (may be empty).
    """
    names: List[str] = []
    if mat is None:
        return names
    t = mat.is_a()
    try:
        if t == 'IfcMaterial':
            if getattr(mat, 'Name', None):
                names.append(str(mat.Name))
        elif t == 'IfcMaterialLayerSetUsage':
            # mat.ForLayerSet.MaterialLayers -> list of IfcMaterialLayer
            layer_set = getattr(mat, 'ForLayerSet', None)
            if layer_set:
                for layer in getattr(layer_set, 'MaterialLayers', []) or []:
                    m = getattr(layer, 'Material', None)
                    if m and getattr(m, 'Name', None):
                        names.append(str(m.Name))
        elif t == 'IfcMaterialLayerSet':
            for layer in getattr(mat, 'MaterialLayers', []) or []:
                m = getattr(layer, 'Material', None)
                if m and getattr(m, 'Name', None):
                    names.append(str(m.Name))
        elif t == 'IfcMaterialProfileSet':
            for profile in getattr(mat, 'MaterialProfileSet', []) or []:
                m = getattr(profile, 'ForProfile', None)
                if m and getattr(m, 'Material', None) and getattr(m.Material, 'Name', None):
                    names.append(str(m.Material.Name))
        elif t == 'IfcMaterialProfile':
            m = getattr(mat, 'ForProfile', None)
            if m and getattr(m, 'Material', None) and getattr(m.Material, 'Name', None):
                names.append(str(m.Material.Name))
        else:
            # Fallback: try common attributes
            if getattr(mat, 'Name', None):
                names.append(str(mat.Name))
            # If it's a container with 'Materials' or similar
            for attr in ('Materials', 'MaterialProfiles', 'MaterialLayers'):
                items = getattr(mat, attr, None)
                if items:
                    for it in items:
                        if getattr(it, 'Name', None):
                            names.append(str(it.Name))
    except Exception:
        # Be defensive: return whatever we've collected so far
        pass
    return names


def find_walls_with_material_keyword(ifc_path: str, keyword: str) -> List[Dict[str, object]]:
    """Find walls whose associated material names contain the given keyword (case-insensitive).

    Args:
        ifc_path (str): Path to the IFC file.
        keyword (str): Keyword to search for inside material names.

    Returns:
        List[Dict[str, object]]: A list of matches. Each entry contains:
            - global_id (str)
            - name (str or None)
            - wall_type (str) the IFC class
            - materials (List[str]) list of material name strings associated with the wall

    Example:
        >>> find_walls_with_material_keyword('./projects/fnde/ARQ.ifc', 'TIJOLO')
        [{'global_id': '0x..', 'name': 'Wall 1', 'materials': ['Tijolo vermelho']}]
    """
    model = ifcopenshell.open(ifc_path)

    # Map from entity id to list of material names
    mat_map = {}
    for rel in model.by_type('IfcRelAssociatesMaterial'):
        relating = getattr(rel, 'RelatingMaterial', None)
        names = _extract_material_names(relating)
        for obj in getattr(rel, 'RelatedObjects', []) or []:
            mat_map.setdefault(obj.id(), [])
            mat_map[obj.id()].extend(names)

    matches: List[Dict[str, object]] = []
    kw = keyword.lower()
    # Consider both IfcWall and IfcWallStandardCase
    for wall in list(model.by_type('IfcWall')) + list(model.by_type('IfcWallStandardCase')):
        names = mat_map.get(wall.id(), [])
        # Normalize and deduplicate
        names = [n for n in names if n is not None]
        uniq = list(dict.fromkeys(names))
        # Check keyword
        if any(kw in n.lower() for n in uniq):
            matches.append({
                'global_id': getattr(wall, 'GlobalId', None),
                'name': getattr(wall, 'Name', None),
                'wall_type': wall.is_a(),
                'materials': uniq
            })
    return matches


if __name__ == "__main__":
    import sys
    ifc = './projects/fnde/ARQ.ifc'
    keyword = 'TIJOLO'
    results = find_walls_with_material_keyword(ifc, keyword)
    if results:
        print(f"Found {len(results)} wall(s) with material containing '{keyword}':")
        for r in results:
            print(f"- GlobalId: {r['global_id']}, Name: {r['name']}, Type: {r['wall_type']}")
            for m in r['materials']:
                print(f"    material: {m}")
    else:
        print(f"No wall material containing '{keyword}' found in {ifc}.")
