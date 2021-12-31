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

## Usage

```
usage: parse.py [-h] --input INPUT --mode {yaml_to_function,function_to_yaml}
```

* `--input`: The input file. If you're calling `yaml_to_function`, this should be a properly formatted YAML file.
  If calling `function_to_yaml`, this should be a plaintext file containing the string that would be within a blade's
  `StylePtr<>` function template within the `blades[]` array in the configuration header file.
* `--mode`: Either `yaml_to_function` or `function_to_yaml`.


# References

* [ProffieOS](https://github.com/profezzorn/ProffieOS)
* [ProffieOS Style Editor](https://fredrik.hubbe.net/lightsaber/style_editor.html) ([GitHub](https://github.com/profezzorn/ProffieOS-StyleEditor))


# Inspiration

I work in AWS on a daily basis, and building thigs with CloudFormation a large part of that.
CloudFormation gives you a streamlined way of describing your infrastructure as code, and
to achieve that AWS maintains a pretty robust list of resource specifications for everything
that's "valid" within a CloudFormation template. A lot of what what's built here was designed
with a similar mindset - produce a large "spec" file that contains all of the valid functions,
their arguments, what's required and what's not, etc. and use that to build a template language
that can be used to perform certain tasks - in this case, describe ProffieOS's blade styles.
