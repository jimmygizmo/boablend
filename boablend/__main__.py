#! /usr/bin/env python3
####################################################################################################
# This module code is not meant to be executed, but the shebang is here to support issuing a warning
# if direct execution is attempted.

import sys

####################################################################################################
# This file is only here in case an attempt is made to execute this module directly
# via "python3 -m boablend" or "python3 path_to_boablend".
# This helps guide the user to proper usage. There is a small piece of similar code in the standard
# if-__main__ section of the module's code in its __init__.py file, for completeness.

sys.exit('The boablend module is meant to be imported only, not executed.')

# Passing an error message via sys.exit(errmsg) also results in an exit code of 1, signaling failure
# to the shell or caller. The error message argument is sent to stderr.


##
#
