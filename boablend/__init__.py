#! /usr/bin/env python3

# The import of bpy works within Blender. Extra steps are needed in order to
# make it work for external execution as well as to make it recognized by the IDE
# as a valid import. To install bpy requires a compiling it and this is currently
# failing. When the bpy build and python module install is working, then we
# can make 'import bpy' work for external exection and for the VSCode/IDE code
# inspection features. See the build error log in this repo and comments in init.sh
# for more information on the bpy build failure.
# This does not prevent the use of boablend within Blender, but it would be nice to fix
# for a more complete and full-featured project.

import bpy
import sys










if __name__ == '__main__':
    sys.exit(f"This file [{__file__}] is meant to be imported, "
"not executed directly.")

##
#
