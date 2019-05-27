#! /usr/bin/env python3
####################################################################################################
# This module code is not meant to be executed, but the shebang is here to support issuing a warning
# through the __main__ block at the end of the file if direct execution occurs.
####################################################################################################

import sys


####################################################################################################
# This file is only here in case an attempt is made to execute this module directly
# via "python3 -m boablend" or "python3 path_to_boablend".
# This helps guide the user to proper usage. There is a small piece of similar code in the standard
# "if __name__ == '__main__'" section of all module code files.
####################################################################################################

sys.exit('The boablend module is meant to be imported only, not executed.')

# Passing an error message via sys.exit(errmsg) also results in an exit code of 1, signaling failure
# to the shell or caller. The error message argument is sent to stderr.


##
#
