# Proffie Blade Style Parser/Template Engine

First and foremost, this project is entirely experimental, and is mostly
for my own amusement and practice with some data manipulation and parsing
techniques.

This project uses Python to read a string of C++ code from ProffieOS's
blade configuration array and turns it into a data structure that can then
be saved as a YAML file. Conversely, it can also take the resulting YAML
file and generate the corresponding lines of C++ code that can then be put
back into ProffieOS's `blades[]` array.

My initial idea behind this is to be able to better understand the layers
and patterns that are used within complex blade styles and be able to
represent them in a more human-readable and self-documenting format, as
oppposed to the massive one-liners we typically see on blade styles.

Where will this go? Probably nowhere, but what I may do is build upon this
to build a simple Flask site where you can upload a number of YAML files
and it'll "compile" them into a `Preset blade[] = { ... }` section that
can be easily dropped into the Arduino project directory and then flashed
over to your Proffie saber.


# Usage

## Requirements

1. Python (I've only tested with python3.x)
1. `pip install -r ./requirements.txt`

## Run

1. Find a blade style you want to use and place it in `input.txt`. Include
   everything within `StylePtr< ... >` but not the `StylePtr` piece itself.
1. Run `./parse.py`

# References

* [ProffieOS](https://github.com/profezzorn/ProffieOS)
* [ProffieOS Style Editor](https://fredrik.hubbe.net/lightsaber/style_editor.html) ([GitHub](https://github.com/profezzorn/ProffieOS-StyleEditor))
