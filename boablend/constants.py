#! /usr/bin/env python3
####################################################################################################
# This module code is not meant to be executed, but the shebang is here to support issuing a warning
# through the __main__ block at the end of the file if direct execution occurs.
####################################################################################################

import sys


# For converting XYZ Degrees values to Euler Values for Rotation
PI = 3.14159265
DEG_TO_EUL_FACTOR = (PI/180.0)  # 0.0174532925

# For converting Euler Values for Rotation to XYZ Degrees values
EUL_TO_DEG_FACTOR = (180.0/PI) # 57.29577957855229

ALPHA_FULL_OPAQUE = 1


########################################## MAIN EXECUTION ##########################################
# This module and this file are only intended to be imported for use, not directly executed.


if __name__ == '__main__':
    sys.exit("This file [{}] is part of the boablend module which is meant to be imported, "
             "not executed directly.".format(__file__))


##
#
