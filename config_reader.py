#!/usr/bin/env python

from configparser import ConfigParser, ExtendedInterpolation
import io

# Load the configuration file
with open("config.ini") as f:
    sample_config = f.read()

parser = ConfigParser(interpolation=ExtendedInterpolation())

parser.readfp(io.BytesIO(sample_config))


# List all contents
# print("List all contents")
# for section in parser.sections():
#     print("Section: %s" % section)
#     for options in parser.options(section):
#         print("x %s:::%s:::%s" % (options,
#                                   parser.get(section, options),
#                                   str(type(options))))

# Print some contents
print("\nPrint some contents")
print(parser.get('paths', 'user_dir'))  # Just get the value
print(parser.get('paths', 'solution_dir'))
# print(config.getboolean('other', 'use_anonymous'))  # You know the datatype?