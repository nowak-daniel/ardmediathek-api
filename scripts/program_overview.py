#!/usr/bin/env python3
# coding=utf-8

from collections import Counter

import ardmediathek

TOP_STATIONS = 10
TOP_PROGRAMS = 15


def bucket_for_count(count: int) -> str:
    if count == 0:
        return "0"
    if count <= 5:
        return "1-5"
    if count <= 20:
        return "6-20"
    if count <= 50:
        return "21-50"
    if count <= 100:
        return "51-100"
    return "101+"


def main() -> None:
    print("Lade Programme aus der ARD Mediathek ...")
    programs = ardmediathek.get_programs()
    print(f"Gefundene Sendungen: {len(programs)}")

    station_counter = Counter(p.station.name for p in programs if p.station and p.station.name)
    bucket_counter = Counter(bucket_for_count(p.num_broadcasts or 0) for p in programs)

    print("\nTop Sender (nach Anzahl Sendungen):")
    for station, count in station_counter.most_common(TOP_STATIONS):
        print(f"- {station}: {count}")

    print("\nVerteilung nach Broadcast-Anzahl je Sendung:")
    bucket_order = ["0", "1-5", "6-20", "21-50", "51-100", "101+"]
    for bucket in bucket_order:
        print(f"- {bucket}: {bucket_counter.get(bucket, 0)}")

    print("\nBeispielsendungen mit den meisten Broadcasts:")
    for program in sorted(programs, key=lambda p: p.num_broadcasts or 0, reverse=True)[:TOP_PROGRAMS]:
        station = program.station.name if program.station else "Unbekannt"
        print(f"- {program.title} | Sender: {station} | Broadcasts: {program.num_broadcasts}")


if __name__ == "__main__":
    main()
