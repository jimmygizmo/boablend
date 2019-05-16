import bpy
# Since bpy is imported here within Blenders internal Python environment, we do not
# need to import by in the external python code, which is helpful since we will be
# working on that code externally with an IDE (VSCode) and under the current setup
# we do not yet have bpy installed externally (compile errors) and so any 'import bpy'
# statements done in external python files will show an error in the IDE.


# The code in this file goes into a text document in a blender file in order to maintain
# the main python code file external to Blender.

# The following Python script file argument should be relative to the
# current .blend file.

filepath = bpy.path.abspath("//test_boablend_camera.py")
exec(compile(open(filepath).read(), filepath, 'exec'))

##
#
