# ardmediathek-api

Python-Client für die inoffizielle Nutzung der ARD-Mediathek Page-Gateway-API (`api.ardmediathek.de`).

## Überblick

Das Paket kapselt zentrale Endpunkte der ARD-Mediathek und stellt sie als Python-Objekte bereit:

- `Program` (Sendung/Format)
- `Broadcast` (konkrete Ausstrahlung/Video)
- `Station` (Publisher/Sender)
- `Stream` (Auflösungen/URLs eines Videos)
- `Image` (Metadaten zu Bildern)

Hauptanwendungsfälle:

- Programme (A-Z) laden
- Programme per ID laden
- Broadcasts per ID laden
- Broadcast-IDs bzw. Broadcast-Objekte zu einem Programm abrufen
- IDs aus ARD-Mediathek-URLs extrahieren

## Terminologie

Die ARD-API verwendet Begriffe, die im Alltag oft vermischt werden. In dieser Library gelten sie wie folgt:

- `Program` (Programm/Format/Sendereihe):
  Das übergeordnete Format, z. B. `tagesthemen`, `Tatort` oder `Expeditionen ins Tierreich`.
  Ein `Program` enthält viele einzelne Veröffentlichungen.
- `Broadcast` (Ausstrahlung/Beitrag/Folge/Video):
  Eine konkrete Einheit innerhalb eines Programms, meist ein einzelnes Video mit Titel, Dauer, Datum und Streams.
- `Sendung`:
  Umgangssprachlich mehrdeutig. Je nach Kontext kann „Sendung“ entweder das Format (`Program`) oder eine konkrete Folge (`Broadcast`) meinen.
  Für technische Nutzung deshalb besser explizit `Program` vs. `Broadcast` unterscheiden.
- `Station` (Sender/Publisher):
  Der veröffentlichende Kanal, z. B. `Das Erste`, `NDR`, `WDR`.
- `Stream`:
  Eine abspielbare Medien-URL eines Broadcasts in einer bestimmten Qualität/Auflösung.

## Installation

Für lokale Entwicklung im Repo mit `uv`:

```bash
uv sync --dev
```

## Quickstart

```python
import ardmediathek

# Alle Programme laden (kann je nach API/Netz dauern)
programs = ardmediathek.get_programs()
print(len(programs), programs[0].title)

# Einzelnes Programm per ID
program = ardmediathek.get_program("Y3JpZDovL25kci5kZS80NQ")
print(program.title, program.num_broadcasts)

# Broadcasts zu einem Programm laden
broadcasts = program.get_broadcasts()
print(broadcasts[0].title, len(broadcasts[0].streams))

# Einzelnen Broadcast per ID laden
broadcast = ardmediathek.get_broadcast("Y3JpZDovL25kci5kZS80NV8yMDA4LTA0LTA2LTAzLTUx")
print(broadcast.title, broadcast.duration)
```

## URL -> ID auflösen

```python
import ardmediathek

kind, object_id = ardmediathek.get_id_from_url(
    "https://www.ardmediathek.de/video/expeditionen-ins-tierreich/titel/ndr/Y3JpZDovL25kci5kZS80NV8yMDA4LTA0LTA2LTAzLTUx"
)
print(kind, object_id)  # "broadcast", "..."
```

## API-Kurzreferenz

### Top-Level Funktionen

- `get_programs() -> list[Program]`
- `get_program(id: str) -> Program`
- `get_broadcast(id: str) -> Broadcast`
- `get_id_from_url(url: str) -> tuple[str, str]`
- `get_program_api_url(id: str) -> str`
- `get_broadcast_api_url(id: str) -> str`
- `get_quality_name(quality: int) -> str`

### Program

Attribute:

- `id`
- `title`
- `description`
- `station`
- `image`
- `num_broadcasts`

Methoden:

- `get_broadcast_ids() -> list[str]`
- `get_broadcasts() -> list[Broadcast]`
- `json() -> dict`

### Broadcast

Attribute (Auszug):

- `id`
- `title`
- `description`
- `duration`
- `emission_date_time`
- `geoblocked`
- `program_id`
- `station`
- `streams`
- `subtitle_url`

Methode:

- `json() -> dict`

## Caching

API-Requests laufen über `requests-cache` mit einem Dateisystem-Cache unter:

`~/.cache/ardmediathek-api/`

Dadurch werden wiederholte Requests deutlich schneller und die API wird entlastet.

## Tests

Projekt nutzt `pytest`:

```bash
uv run pytest
```

Hinweis: Die Tests sprechen gegen Live-Endpunkte und sind dadurch von Verfügbarkeit und Payload-Änderungen der ARD-API abhängig.

## Bekannte Einschränkungen

- Es gibt keine offizielle Stabilitätsgarantie für die genutzten ARD-Endpunkte; API-Änderungen können Breaking Changes verursachen.
- Geoblocking hängt von den von der API gelieferten Metadaten ab (`broadcast.geoblocked`).
- Bei sehr großen Programm-/Broadcast-Listen kann das Laden spürbar dauern (Paginierung über mehrere Requests).

## Lizenz

GPLv3. Siehe [LICENSE](LICENSE).
