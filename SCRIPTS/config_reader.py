#!/usr/bin/env python

from configparser import ConfigParser, ExtendedInterpolation
import io

class config_reader:

    def __init__(self):
        # Load the configuration file
        with open("CONFIGURATION/config.ini") as f:
            sample_config = f.read()
            self.parser = ConfigParser(interpolation=ExtendedInterpolation())
            self.parser.readfp(io.BytesIO(sample_config))

    def get_assignemnts(self):
        return self.parser.get('paths', 'assignments_dir')

    def get_file_location(self, location):
        switcher = {
            'assignments':self.get_assignemnts(),
        }
        # print(switcher.get(location))
        return switcher.get(location)
        

    def get_deadline(self):
        return self.parser.get('deadlines', 'deadline')



# cr = config_reader()
# print(cr.get_assignemnts())

# List all contents
# print("List all contents")
# for section in parser.sections():
#     print("Section: %s" % section)
#     for options in parser.options(section):
#         print("x %s:::%s:::%s" % (options,
#                                   parser.get(section, options),
#                                   str(type(options))))

# Print some contents
# print("\nPrint some contents")
# print(parser.get('paths', 'user_dir'))  # Just get the value
# print(parser.get('paths', 'solution_dir'))
# print(config.getboolean('other', 'use_anonymous'))  # You know the datatype?