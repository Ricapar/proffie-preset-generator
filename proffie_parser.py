#!/usr/bin/env python
import json


def handle_function(function, args):

	if function == "RotateColorsX":
		output = {
			"RotateColorsX": {
				"Rotation": myprint(None, args[0]),
				"Color": myprint(None, args[1])
			}
		}
		return output

	if function == "Rgb":
		output = {
			"Rgb": {
				"R": myprint(None, args[0]),
				"G": myprint(None, args[1]),
				"B": myprint(None, args[2])
			}
		}
		return output

	if function == "Random":
		output = {
			"Random": {
				"min": myprint(None, args[0]),
				"max": myprint(None, args[1])
			}
		}
		return output


	# All other functions
	output = {}
	output[function] = []
	for index, value in enumerate(args):
		output[function].append(myprint(function, args[index]))

	# If we have a single-item array, then return it as-is
	if len(output[function]) == 1:
		output[function] = output[function][0]

	return output

def myprint(parent, data):

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
			return handle_function(function=k, args=v)

	if isinstance(data, list):
		for v in data:
			if isinstance(v, dict) or isinstance(v, list):
				myprint(parent="", data=v)

	return output


class ProffieParser:

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


	def cleanup_types(self):

		newdata = myprint(parent="StylePtr", data=self._data)

		return newdata

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

			if token and token not in self._parent:
				self._parent.append(token)

			self._level = self._level - 1
			self._stack.pop()
			self._parent = self._data_stack.pop()

			return


		if token and token not in self._parent:
			self._parent.append(token)


		return


	def indent(self):
		return self._level * "  "

	def get_data(self):
		return self._data
