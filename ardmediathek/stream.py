#-*- coding:utf-8 -*-

import copy

class Stream:
	def __init__(self, data):
		# Legacy schema
		if "_stream" in data:
			self.width = data.get("_width")
			self.height = data.get("_height")
			self.url = data.get("_stream")
			self.quality = data.get("_quality")
			return
		# Current ARD schema
		self.width = data.get("maxHResolutionPx")
		self.height = data.get("maxVResolutionPx")
		self.url = data.get("url")
		self.quality = data.get("forcedLabel") or data.get("mimeType") or "unknown"
	
	def json(self):
		d = copy.copy(self.__dict__)
		return d
