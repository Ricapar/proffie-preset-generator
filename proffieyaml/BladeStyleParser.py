"""
Copyright 2021 Rich Acosta <rich@ricapar.net>
Part of proffieyaml, a yaml-to-cpp parser/generator for ProffieOS's saber styles
"""
import json
from . import BladeStyleFunction


class BladeStyleParser:

	_data = {
		"StylePtr": []
	}
	_parent = _data["StylePtr"]
	_data_stack = [_parent]

	_stack = ["StylePtr"]
	_level = 0

	_key_chars = [
		"<",
		">",
		",",
	]

	_skip_chars = [
		"\n",
		"\r",
	]

	def __init__(self):
		self.function_parser = BladeStyleFunction.BladeStyleFunction()

	def cleanup_types(self):
		newdata = BladeStyleParser._cleanup_types(
			data=self._data,
			callback=BladeStyleParser._cleanup_types
		)

		return newdata

	@staticmethod
	def _cleanup_types(data, callback):
		output = {}

		# Return if we're not dealing with a dict or a list, meaning we've
		# probably hit the bottom of something iterable.
		if not isinstance(data, dict) and not isinstance(data, list):
			return data

		# If we have a single element list, return that element alone
		if isinstance(data, list) and len(data) == 1:
			return data[0]

		if isinstance(data, dict):
			for k, v in data.items():
				bsf = BladeStyleFunction.BladeStyleFunction()
				return bsf.parsed_to_yaml(function=k, args=v, callback=callback)

		if isinstance(data, list):
			for v in data:
				if isinstance(v, dict) or isinstance(v, list):
					callback(data=v, callback=callback)

		return output

	def parse(self, style):

		parse_buffer = ""
		for char in style:
			if char in self._skip_chars:
				continue

			if char in self._key_chars:
				self.handle_key_char(char=char, token=parse_buffer)
				parse_buffer = ""
			else:
				parse_buffer += char
				parse_buffer = parse_buffer.strip()


	def handle_key_char(self, char, token):

		if char == "<":
			self._level = self._level + 1
			self._stack.append(token)

			token_struct = {}
			token_struct[token] = []

			self._parent.append(token_struct)
			self._data_stack.append(self._parent)
			self._parent = token_struct[token]
			return

		if char == ">":
			if token:
				self._parent.append(token)

			self._level = self._level - 1
			self._stack.pop()
			self._parent = self._data_stack.pop()

			return

		if token:
			self._parent.append(token)

		return


	def indent(self):
		return self._level * "  "

	def get_data(self):

		return self.cleanup_types()
