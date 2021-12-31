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


	def yaml_to_function(self, data):

		output = ""

		# if we're not handling a list or a dictionary, return the basic type as a string
		if not isinstance(data, dict) and not isinstance(data, list):
			return str(data)

		if isinstance(data, dict):
			output_list = []
			for function, args in data.items():
				logging.debug(f"{__name__}: function={function}, args={args}")

				# If we have a defined function, then we have to deconstruct
				# the underlying data structure to remove the named arguments
				# and convert them back into positional ones

				function_spec = self.get_function(function)

				if not function_spec:
					logging.debug(f"{__name__}: Did NOT find function spec for {function}")

					output_list_str = f"{function}<"
					output_list_str += self.yaml_to_function(args)
					output_list_str += ">"

					output_list.append(output_list_str)


				if function_spec:
					logging.debug(f"{__name__}: Found function spec for {function}")
					logging.debug(function_spec)

					# Loop through all of the expected function arguments
					function_output_args = []
					for arg_name, arg_properties in function_spec["Arguments"].items():
						logging.debug(f"   arg_name={arg_name}, arg_properties={arg_properties}")
						logging.debug(f"   args={args}")

						try:
							function_output_args.insert(
								arg_properties["Position"],
								self.yaml_to_function(args[arg_name])
							)
						except KeyError as exp:
							if arg_properties["Required"]:
								raise Exception(f"Required property '{arg_name}' is missing from function {function}<>")

						except Exception as exp:
							raise exp


					output_list_str = f"{function}<"
					output_list_str += ",".join(function_output_args)
					output_list_str += ">"

					output_list.append(output_list_str)

			output = ",".join(output_list)

		if isinstance(data, list):
			output_list = []
			for args in data:
				logging.debug(f"{__name__}: args={args}")
				output_list.append(self.yaml_to_function(args))

			output = ",".join(output_list)

		return output


	def function_to_yaml(self, function, args, callback):
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