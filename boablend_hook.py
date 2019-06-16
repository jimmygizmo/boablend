
########################################## BOABLEND HOOK ###########################################
# boablend_hook_version = '2019-007'
# See: /docs/boablend_hook_installation.txt
####################################################################################################

import bpy  # This import works when executing within Blender but will show an import error in IDEs.
# See: /docs/import_bpy_error_in_ide.txt

import os

# Set verbose_hook to True to print status and diagnostic info to STDOUT.
# This flag only affects output from this boablend hook code.
verbose_hook = True

# Path to the Boablend entry point file, relative to the current Blender blend file containing
# this boablend hook code:
boablend_entry_point = 'boablend_start.py'

filepath = bpy.path.abspath(f"//{boablend_entry_point}")

if verbose_hook:
    print()
    print("################################################################################"
          "####################")
    print("BOABLEND STARTING")
    print()
    print("Executing entry point at: ")
    print(filepath)

exec(compile(open(filepath).read(), filepath, 'exec'))


##
#
