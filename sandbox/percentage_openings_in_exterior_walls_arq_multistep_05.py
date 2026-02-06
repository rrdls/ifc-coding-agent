from skills.learned.relationships.scripts.percentage_openings import percentage_openings_in_exterior_walls


def main():
    ifc_path = "./projects/fnde/ARQ.ifc"
    percent = percentage_openings_in_exterior_walls(ifc_path)
    print(f"Percentage of openings in exterior walls: {percent:.2f}%")


if __name__ == "__main__":
    main()
