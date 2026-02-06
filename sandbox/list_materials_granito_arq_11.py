"""
Sandbox script to list materials containing 'Granito' in the ARQ.ifc model.

This script imports the generic list_materials function from skills.learned.materials
and prints the found materials (one per line) and a count summary.
"""
from skills.learned.materials.scripts.list_materials import list_materials


def main():
    ifc_path = './projects/fnde/ARQ.ifc'
    results = list_materials(ifc_path, keyword='Granito')
    for r in results:
        print(r)
    print(f"Total: {len(results)} materials")


if __name__ == '__main__':
    main()
