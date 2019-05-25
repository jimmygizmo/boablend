
####################################################################################################

import pprint
import sys

# Moving this into the Logger class __init__, which is more specifically where it will be used.
# This is a more logical/correct location for it.
# pp = pprint.PrettyPrinter(indent=4)


################################## FUNCTION AND CLASS DEFINITIONS ##################################


class Logger:
    def __init__(self):
        self.pp = pprint.PrettyPrinter(indent=4)

    def line(self):
        print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
    
    def log(self, msg):
        self.line()
        print(msg)

    def dump(self, obj):
        self.line()
        self.pp.pprint(obj)

    def dump_environment_info(self):
        self.line()
        print("sys.path: ")
        print("\n".join(sys.path))


##
#
