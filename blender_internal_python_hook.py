# No shebang. Boa files are currently only supported for direct execution from withing the Python
# environment of a currently-running Blender instance and open blend file with a Text object
# containing the boablend hook code. You cannot currently run Boas from a standard Python env.
####################################################################################################
########################################## BOABLEND HOOK ###########################################
# boablend_hook_version = '2019-005'
####################################################################################################
# Install all of the code in this file into a Text Object within Blender.
# It is recommended to name this Text Object 'boablend_hook'.
# Click 'Run Script' on this Text Object or perform an equivalent action to run the current Boablend
# project configuration. Other modes of execution may be available in the future. Dispatching of
# different/specific Boa files occurs in boablend_start.py. This hook code should remain as generic
# and simple as possible.
# Hook code  will likely always be a very small amount of code. If any changes are ever needed to
# the hook code or if it is updated along with this project, you will need to manually (cut/paste)
# the updated hook code back into the blend file Text object.
####################################################################################################

####################################################################################################
import bpy  # This import works when executing within Blender but will show an import error in IDEs.
# Regarding import errors showing in your IDE for 'import bpy':
# /docs/import_bpy_error_in_ide.txt
####################################################################################################


# Set verbose to True to print status and diagnostic info to STDOUT.
# This flag only affects output from this hook code.
verbose = True


################################ BOABLEND ENTRY POINT CONFIGURATION ################################
# The executable python file which imports most of this project's dependencies and runs the main
# code. It may never be necessary to change this and in fact it may not be recommended to. To fork
# or customize execution in your Boablend project, you will probably have a better method and
# location to do this within the entry point file itself and that would usually be more appropriate.
#
# TODO: Implement a dispatch mechanism in the entry point code so that some externalized and
# and configurable switching mechanism will select which project-specific code to execute. A naming
# convention is needed here.

# The following path must be expressed:
# RELATIVE TO THE CURRENT BLEND FILE CONTAINING THIS HOOK CODE.
boablend_entry_point = 'boablend_start.py'

####################################################################################################


if verbose:
    print()
    print("~~~~~~~~~~~~~~~~~~~~ Boablend starting.")

# Current working directory is not so relevant here. It appears (at least on MacOS) to be the
# user's home directory of the user running Blender and so is not relevant to the current
# blend file, which is the reference point we currently use in how boablend is imported and
# executed. So we won't log it anymore from here.
# import os
# current_working_directory = os.getcwd()
# print("Blender file current working directory: ")
# print(current_working_directory)

if verbose:
    print("Boablend entry point filename: {}".\
        format(boablend_entry_point))

filepath = bpy.path.abspath("//{}".format(boablend_entry_point))

if verbose:
    print("Executing entry point at: ")
    print(filepath)

exec(compile(open(filepath).read(), filepath, 'exec'))


##
#
