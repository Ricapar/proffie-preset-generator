#!/usr/bin/env python
import os
import sys
import json
import ruamel.yaml
import argparse

import proffieyaml

def main():


	# Load file for testing
	with open("input.txt", "r") as proffie_style_fh:
		proffie_style = proffie_style_fh.read()

	# Test parsing
	parser = proffieyaml.BladeStyleParser()
	parser.parse(style=proffie_style)

	data = parser.get_data()

	yaml = ruamel.yaml.YAML()
	yaml.indent(sequence=4, offset=2)

	print("---")
	yaml.dump(data, sys.stdout)

	return

if __name__ == '__main__':
	main()
