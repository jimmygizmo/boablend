
####################################################################################################
########################################## BOABLEND HOOK ###########################################
# boablend_hook_version = '2019-004'
####################################################################################################
# Install all of the code in this file into a Text Object within Blender.
# It is recommended to name this Text Object 'boablend_hook'.
# Click 'Run Script' on this Text Object or perform an equivalent action to run the current Boablend
# project configuration. Other modes of execution may be available in the future.
####################################################################################################

import bpy  # See comments below about bpy import errors showning in your IDE.


# Set verbose to True to print status and diagnostic info to STDOUT.
# This flag only affects output from this hook code.
verbose = True

####################################################################################################

################################ BOABLEND ENTRY POINT CONFIGURATION ################################
# The executable python file which imports most of this project's dependencies and runs the main
# code. It may never be necessary to change this and in fact it may not be recommended to. To fork
# or customize execution in your Boablend project, you will probably have a better method and
# location to do this within the entry point file itself and that would usually be more appropriate.
#
# TODO: Implement a dispatch mechanism in the entry point code so that some externalized and
# and configurable switching mechanism will select which project-specific code to execute. A naming
# convention is needed here. 'Projects' is the most immediate and simple concept, leading to:
# 'bloablend project'. The nomenclature will be under consideration until this starts getting
# implemented shortly. An obvious concept here is to have only generic code in the entry point as
# well as to enble important usability features.

# The following path must be expressed:
# RELATIVE TO THE CURRENT BLEND FILE CONTAINING THIS HOOK CODE.
boablend_entry_point = 'boablend_start.py'

####################################################################################################

# NOTE: IDE Indication of bpy import errors:
# Since bpy is imported here within Blenders internal Python environment, we do not need to import
# bpy in the external python code, and that's not currently possible with the setup this project
# currently is using anyhow. This project is setup to use the VSCode (or Atom, IDEA CE, or a
# similar) IDE to edit all of the source code. Under the current setup bpy is not yet installed
# externally due to compilation errors in the first pass installation attempt, and so any
# 'import bpy' statements done in external python files will show an error in the IDE.
#
# A small piece of hook code resides in the blender file, but this will likely always be a very
# small amount of code. If any changes are ever needed to the hook code or if it is updated along
# with this project, you will need to manually (cut/paste) the updated hook code back into the
# blend file Text object.


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
