
########################################## BOABLEND HOOK ###########################################
# boablend_hook_version = '2019-006'
# See: /docs/boablend_hook_installation.txt
####################################################################################################

####################################################################################################
import bpy  # This import works when executing within Blender but will show an import error in IDEs.
# See: /docs/import_bpy_error_in_ide.txt
####################################################################################################

import os


# Set verbose to True to print status and diagnostic info to STDOUT.
# This flag only affects output from this boablend hook code.
verbose = True

################################ BOABLEND ENTRY POINT CONFIGURATION ################################

# Path to the Boablend entry point file, relative to the current Blender blend file containing
# this boablend hook code:
boablend_entry_point = 'boablend_start.py'

####################################################################################################


current_working_directory = os.getcwd()
filepath = bpy.path.abspath("//{}".format(boablend_entry_point))

if verbose:
    print()
    print("################################################################################"
          "####################")
    print("BOABLEND STARTING")
    print()
    print("Blender file current working directory: ")
    print(current_working_directory)
    print("Boablend entry point filename: {}".\
        format(boablend_entry_point))
    print("Executing entry point at: ")
    print(filepath)

exec(compile(open(filepath).read(), filepath, 'exec'))


##
#
