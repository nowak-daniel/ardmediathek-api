import argparse
import json

import ardmediathek


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Liefert eine vollständige Liste aller Sendungen (Programme) aus der ARD Mediathek."
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Gibt die vollständige Liste als JSON aus.",
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Optionaler Dateipfad für die Ausgabe.",
    )
    args = parser.parse_args()

    programs = ardmediathek.get_programs()
    programs_sorted = sorted(programs, key=lambda p: (p.title or "").lower())

    if args.json:
        payload = [
            {
                "id": p.id,
                "title": p.title,
                "description": p.description,
                "station": p.station.name if p.station else None,
                "num_broadcasts": p.num_broadcasts,
            }
            for p in programs_sorted
        ]
        content = json.dumps(payload, ensure_ascii=False, indent=2)
    else:
        lines = []
        for idx, p in enumerate(programs_sorted, start=1):
            station = p.station.name if p.station else "Unbekannt"
            lines.append(
                f"{idx:4d}. {p.title} | Sender: {station} | Broadcasts: {p.num_broadcasts}"
            )
        content = "\n".join(lines)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"{len(programs_sorted)} Sendungen in '{args.output}' geschrieben.")
    else:
        print(content)
        print(f"\nGesamt: {len(programs_sorted)} Sendungen")


if __name__ == "__main__":
    main()
