#! /usr/bin/env python3
####################################################################################################
# This module code is not meant to be executed, but the shebang is here to support issuing a warning
# through the __main__ block at the end of the file if direct execution occurs.
####################################################################################################

import sys

# This file must be in place for module structure but currently has no funtional role in boablend.


########################################## MAIN EXECUTION ##########################################
# This module and this file are only intended to be imported for use, not directly executed.


if __name__ == '__main__':
    sys.exit("This file [{}] is part of the boablend module which is meant to be imported, "
             "not executed directly.".format(__file__))


##
#
