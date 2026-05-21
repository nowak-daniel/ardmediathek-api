import copy

from .image import Image
from .station import Station
from .stream import Stream


class Broadcast:
    def __init__(self, data):
        self.description = data["synopsis"]
        embedded_media = data.get("mediaCollection", {}).get("embedded", {})
        self.duration = embedded_media.get("_duration", data.get("duration"))
        self.emission_date_time = data["broadcastedOn"]
        self.geoblocked = data["geoblocked"]
        self.id = data["id"]
        self.image = Image(data["image"])
        self.program_id = data["show"]["id"]
        self.program = None
        self.station = Station(data["publicationService"])
        self.streams = []
        self.subtitle_url = embedded_media.get("_subtitleUrl")
        self.title = data["title"]

        # Legacy schema
        media_arrays = embedded_media.get("_mediaArray", [])
        if media_arrays:
            stream_infos = media_arrays[0].get("_mediaStreamArray", [])
            for stream_info in stream_infos:
                if stream_info.get("_quality") == "auto":
                    continue
                self.streams.append(Stream(stream_info))
        # Current ARD schema
        else:
            for stream_group in embedded_media.get("streams", []):
                for stream_info in stream_group.get("media", []):
                    if stream_info.get("forcedLabel", "").lower() == "auto":
                        continue
                    self.streams.append(Stream(stream_info))
            subtitles = embedded_media.get("subtitles", [])
            if not self.subtitle_url and subtitles:
                self.subtitle_url = subtitles[0].get("url")

    def json(self):
        d = copy.copy(self.__dict__)
        d["image"] = self.image.json()
        if self.program:
            d["program"] = self.program.json()
        d["station"] = self.station.json()
        d["streams"] = []
        for stream in self.streams:
            d["streams"].append(stream.json())

        return d
