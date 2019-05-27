#! /usr/bin/env python3
####################################################################################################
# This module code is not meant to be executed, but the shebang is here to support issuing a warning
# through the __main__ block at the end of the file if direct execution occurs.
####################################################################################################

import pprint
import sys


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


########################################## MAIN EXECUTION ##########################################
# This module and this file are only intended to be imported for use, not directly executed.


if __name__ == '__main__':
    sys.exit("This file [{}] is part of the boablend module which is meant to be imported, "
             "not executed directly.".format(__file__))


##
#
