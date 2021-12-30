#!/usr/bin/env python
"""
Copyright 2021 Rich Acosta <rich@ricapar.net>
Part of proffieyaml, a yaml-to-cpp parser/generator for ProffieOS's saber styles
"""

import sys
import ruamel.yaml
import proffieyaml

def main():
	"""
	main function, currently just for testing.
	To be later rewritten to with something that has argparse and other more useful options.
	"""

	# Load file for testing
	with open("input.txt", "r", encoding="utf-8") as proffie_style_fh:
		proffie_style = proffie_style_fh.read()

	# Test parsing
	parser = proffieyaml.BladeStyleParser()
	parser.parse(style=proffie_style)

	data = parser.get_data()

	yaml = ruamel.yaml.YAML()
	yaml.indent(sequence=4, offset=2)

	print("---")
	yaml.dump(data, sys.stdout)

if __name__ == '__main__':
	main()
