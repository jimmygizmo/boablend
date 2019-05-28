
import pprint
import sys


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
