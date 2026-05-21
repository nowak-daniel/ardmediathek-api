import ardmediathek

PROGRAM_ID = "Y3JpZDovL25kci5kZS80NQ"
MAX_BROADCASTS = 10

program = ardmediathek.get_program(PROGRAM_ID)
print(f"Programm: {program.title}")
print(f"Anzahl Broadcasts laut API: {program.num_broadcasts}")

broadcasts = program.get_broadcasts()[:MAX_BROADCASTS]
print(f"Prüfe die ersten {len(broadcasts)} Broadcasts ...")

for broadcast in broadcasts:
    print(f"\n{broadcast.title}")
    print(f"ID: {broadcast.id}")
    print(f"Geo-Blocked: {broadcast.geoblocked}")
    if not broadcast.streams:
        print("Keine Streams gefunden.")
        continue

    for stream in broadcast.streams:
        print(f"- {stream.quality} {stream.width}x{stream.height}: {stream.url}")
