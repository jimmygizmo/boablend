#! /usr/bin/env bash

# Use a console command like the one below to launch the Blender application
# in a way which leaves a console window open in which you can see Python
# errors. This is currently the only way I know of to see Python error details
# while running and debugging Python code within Blender.

# The below command is for MacOS. The command and the behavior may be a little
# different on Windows and Linux of course.

# Open the included boablend project blend file which has the boablend hook
# code installed.
/Applications/Blender/blender.app/Contents/MacOS/blender \
./blender280b_boablend_hook_enabled.blend


# Open the Blender application only. Presumably, you will then manually open a
# blend file which has boablend hook code installed within it.
#/Applications/Blender/blender.app/Contents/MacOS/blender


###############################################################################

# Docs on Blender command-line arguments and env vars:
# https://docs.blender.org/manual/en/latest/advanced/command_line/arguments.html
# There are many but none appeared immediately useful to boablend.

