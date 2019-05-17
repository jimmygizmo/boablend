
###############################################################################
################################ BOABLEND HOOK ################################
# boablend_hook_version = '2019-001'
# boablend_hook_hash = '18c49c41d997e9e7adb88e8b0ef187977cb257fa'
# boablend_hook_date = 'Thu May 16 00:20:29 2019 -0700'
###############################################################################
# Install all of the code in this file into a Text object within Blender.
# Click 'Run Script' on this Text object or perform an equivalent action to
# run the current Boablend project configuration.
# Other modes of execution may be available in the future.
###############################################################################

import bpy  # See comments below about bpy import errors showning in your IDE.
import os

# Print status and diagnostic info to STDOUT.
verbose = True

###############################################################################

###################### BOABLEND ENTRY POINT CONFIGURATION #####################
# The executable python file which imports most of this projects dependencies
# and runs the main code. It may never be necessary to change this and in fact
# it may not be recommended to. To fork/customize execution in your Boablend
# project, you will probably have a better method and location to do this
# within the entry point file itself and that would usually be more
# appropriate.

# The following path must be expressed:
# RELATIVE TO THE CURRENT BLEND FILE CONTAINING THIS HOOK CODE.
boablend_entry_point = 'test_boablend_camera.py'

###############################################################################

# NOTE: IDE Indication of bpy import errors:
# Since bpy is imported here within Blenders internal Python environment, we
# do not need to import bpy in the external python code, and that's not
# currently possible with the setup this project currently is using anyhow.
# This project is setup to use the VSCode (or Atom, IDEA CE, or a similar IDE)
# to edit all of the source code. Under the current setup bpy is not yet
# installed externally due to compilation errors in the first pass
# installation attempt, and so any 'import bpy' statements done in external
# python files will show an error in the IDE.
# Note that a small piece of hook code will reside in the blender file, but
# this will likely always be a very small amount of code. If any changes are
# ever needed to the hook code or if it is updated along with this project,
# you will need to manually (cut/paste) the updated hook code.


if verbose:
    print()
    print("~~~~~~~~~~~~~~~~~~~~ Boablend starting.")

current_working_directory = os.getcwd()

if verbose:
    print("Blender file current working directory: ")
    print(current_working_directory)
    print("Boablend entry point filename: {}".\
        format(boablend_entry_point))

filepath = bpy.path.abspath("//{}".format(boablend_entry_point))

if verbose:
    print("Executing entry point at: ")
    print(filepath)

exec(compile(open(filepath).read(), filepath, 'exec'))


##
#
