"""
Script to count unique material names containing 'Cerâmica' in the ARQ.ifc model.

This script imports the generic function from skills/learned/properties and runs
it against the provided ARQ.ifc file.
"""
from skills.learned.properties.scripts.count_unique_materials import count_unique_materials


def main() -> None:
    """Run the unique material count and print the result."""
    ifc_path = './projects/fnde/ARQ.ifc'
    term = 'Cerâmica'
    count = count_unique_materials(ifc_path, term)
    print(count)


if __name__ == '__main__':
    main()
