#!/usr/bin/env python
import os
import json
import yaml
import argparse

from proffie_parser import ProffieParser

def main():


	# Load file for testing
	with open("input.txt", "r") as proffie_style_fh:
		proffie_style = proffie_style_fh.read()

	# Test parsing
	parser = ProffieParser()
	parser.parse(style=proffie_style)


	data = parser.get_data()


	print(json.dumps(data, indent=2))


	print("=" * 100)

	cleaned_data = parser.cleanup_types()
	print(yaml.dump(cleaned_data))


	return

if __name__ == '__main__':
	main()