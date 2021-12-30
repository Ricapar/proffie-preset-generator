"""
Copyright 2021 Rich Acosta <rich@ricapar.net>
Part of proffieyaml, a yaml-to-cpp parser/generator for ProffieOS's saber styles
"""
import logging
import json
import importlib.resources as pkg_resources
import ruamel.yaml


class BladeStyleFunction:

	_spec = {}

	def __init__(self):
		if not BladeStyleFunction._spec:
			logging.debug("{__class__}: Loading FunctionSpecification.yaml")
			spec_fh = pkg_resources.read_text(
				__package__,
				"FunctionSpecification.yaml"
			)
			spec = ruamel.yaml.load(spec_fh, Loader=ruamel.yaml.Loader)
			BladeStyleFunction._spec = spec

	def get_function(self, function):
		"""Looks up a function in the function spec list. If found,
		returns a dictionary from the corresponding entry in the function
		spec. If not found, returns a None-type.
		"""
		if function in BladeStyleFunction._spec["Functions"]:
			return BladeStyleFunction._spec["Functions"][function]
		else:
			return None

	def parsed_to_yaml(self, function, args, callback):
		function_spec = self.get_function(function)

		# if a spec isn't found in our function specification file,
		# we'll use the generic/default spec function to return a
		# generic enough data structure that'll still translate back
		# to what we want to output
		if not function_spec:
			logging.debug(f"{__class__}: did not find a spec " \
						   "for {function}, using default_spec")
			return BladeStyleFunction.default_spec(function, args, callback)

		logging.debug(f"{__class__}: Found spec for {function}")

		# If we did find an entry in the specification file, then we can
		# iterate through the known arguments and give them names within
		# our resulting datastructure for pretty YAML printing.
		output_args = {}
		for arg, arg_spec in function_spec["Arguments"].items():
			try:
				output_args[arg] = callback(args[arg_spec["Position"]], callback)
			except IndexError:
				if arg_spec["Required"]:
					missing_position = arg_spec["Position"]
					error_message = f"Function {function}<> is missing required argument" \
									"at position {missing_position}"
					logging.error("{__class__}: {error_message}")
					raise Exception(error_message)
			except Exception as exp:
				logging.error("unplanned issue, probably a broken spec file?")
				logging.error(json.dumps(function_spec))
				raise exp

		output = {}
		output[function] = output_args
		return output

	@staticmethod
	def default_spec(function, args, callback):
		output = {}
		output[function] = []
		for index, value in enumerate(args):
			output[function].append(callback(args[index], callback))

		# If we have a single-item list, then return it as-is
		if isinstance(output[function], list) and len(output[function]) == 1:
			output[function] = output[function][0]

		return output