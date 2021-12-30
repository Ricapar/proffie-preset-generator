#!/usr/bin/env python
import ruamel.yaml
import json

try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources



class BladeStyleFunction:

	_spec = {}

	def __init__(self):
		if not BladeStyleFunction._spec:
			spec_fh = pkg_resources.read_text(
				__package__,
				"FunctionSpecification.yaml"
			)
			spec = ruamel.yaml.load(spec_fh, Loader=ruamel.yaml.Loader)

			print(json.dumps(spec, indent=2))

			BladeStyleFunction._spec = spec

	def get_function(self, function):
		if function in BladeStyleFunction._spec["Functions"]:
			return BladeStyleFunction._spec["Functions"][function]
		else:
			return None

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

	def parsed_to_yaml(self, function, args, callback):

		function_spec = self.get_function(function)

		# if a spec isn't found in our function specification file,
		# we'll use the generic/default spec function to return a
		# generic enough data structure that'll still translate back
		# to what we want to output
		if not function_spec:
			print(f"did not find a spec for {function}")
			return BladeStyleFunction.default_spec(function, args, callback)


		print(f"FOUND spec for {function}")


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
					raise Exception(f"Function {function}<> is missing required argument at position {missing_position}")


		output = {}
		output[function] = output_args

		return output
