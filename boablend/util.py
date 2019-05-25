
####################################################################################################

import pprint

pp = pprint.PrettyPrinter(indent=4)


################################## FUNCTION AND CLASS DEFINITIONS ##################################


class Logger:
    def __init__(self):
        pass
    
    def log(self, msg):
        print(msg)

    def dump(self, obj):
        pp.pprint(obj)


##
#
