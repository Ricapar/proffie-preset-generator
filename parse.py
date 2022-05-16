#!/usr/bin/env python
"""
Copyright 2021 Rich Acosta <rich@ricapar.net>
Part of proffieyaml, a yaml-to-cpp parser/generator for ProffieOS's saber styles
"""

import sys
import argparse
import json
import logging
import ruamel.yaml
import proffieyaml


logging.basicConfig(level=logging.DEBUG)


def load_file(file):
	with open(file, "r", encoding="utf-8") as file_fh:
		file_data = file_fh.read()

	return file_data

def main():
	"""
	main function, currently just for testing.
	To be later rewritten to with something that has argparse and other more useful options.
	"""

	parser = argparse.ArgumentParser()
	parser.add_argument(
		"--input",
		required=True,
		help="required: Input file"
	)

	parser.add_argument(
		"--mode",
		choices=["yaml_to_function", "function_to_yaml"],
		required=True
	)

	cli_args = parser.parse_args()


	data = load_file(cli_args.input)

	if cli_args.mode == "yaml_to_function":
		yaml_data = ruamel.yaml.load(data, Loader=ruamel.yaml.Loader)

		bsf = proffieyaml.BladeStyleFunction()
		output = bsf.yaml_to_function(data=yaml_data)

		print(output)




	if cli_args.mode == "function_to_yaml":
		parser = proffieyaml.BladeStyleParser()
		parser.parse(style=data)

		data = parser.get_data()
		yaml = ruamel.yaml.YAML()
		yaml.indent(sequence=4, offset=2)
		print("---")
		yaml.dump(data, sys.stdout)


if __name__ == '__main__':
	main()
