
####################################################################################################
# BOA: rgb_cube_tower
# A few small steps are proving difficult to automate. Please read the following for instructions
# on any steps you need to perform manually in the Blender GUI prior to rendering the animation.
# See: /boas/rgb_cube_tower.txt

import bpy  # This import works when executing within Blender but will show an import error in IDEs.
# See: /docs/import_bpy_error_in_ide.txt

import sys
import os

# See: /docs/sys_path_hack_in_boa_files.txt
dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir)

import boablend

# See: /docs/use_of_importlib_reload.txt
import importlib
importlib.reload(boablend)


########################################## CONFIGURATION ###########################################

# Camera Settings

# These camera settings are optimal for the animation of the tower falling and shattering and were
# used for the rendering of the following YouTube video:
# https://www.youtube.com/watch?v=1j7_nHfTeaw
# The FOV represents a fairly wide-angle lense which helps to capture everything from the beginning
# of the tower's fall to the cubes that roll out on the surface towards the camera.

rgb_cube_tower_camera_settings = {
    'name': 'RGB Cube Tower Camera',
    'comment': 'boablend.Camera settings for the RGB Cube Tower project',
    'scene.camera.location.x': 67.37174224853516,
    'scene.camera.location.y': 62.108951568603516,
    'scene.camera.location.z': -22.072437286376953,
    'rot_eul0x_deg': 98.04878632691747,
    'rot_eul1y_deg': 0.00013285419354253954,
    'rot_eul2z_deg': -585.7637994372828,
    'render_resolution_x': 854,
    'render_resolution_y': 480,
    'scene.camera.data.angle': 88.22523942116491,
    'scene.camera.data.clip_start': 0.1,
    'scene.camera.data.clip_end': 1000
}

# Tower/Cube Settings

# This version now creates a custom material for each cube and maps the entire RGB color space into
# the XYZ space based on the position/index of each cube. Pure black to pure white is fully mapped
# across RGB/XYZ space.

# This code will be compiled and run inside Blender using the built in Python
# interpreter which is a version 2.x interpreter.

# This code is compatible with Blender 2.79b. Cube size set via 'radius='.
# This code is not compatible with Blender 2.80b. Cube size set via 'size='.
# When porting between the two version note that size = 2 * radius.

# The cube origin is in the volumetric center of the cube as instantiated by
# bpy.ops.mesh.primitive_cube_add(). Obviously this is necessary to know in order
# to perform location calculations in the main execution code.

# Dimensions of the tower of cubes as number of cubes.
# The 8x8x24 dimensions are what were used in the linked YouTube video.
cubes_x_width = 8
cubes_y_depth = 8
cubes_z_height = 24
# 8x8x24 takes about 10 minutes to run.
#
# For rapid dev/test iterations, 4x4x6 runs in a few seconds:
#cubes_x_width = 4
#cubes_y_depth = 4
#cubes_z_height = 6

# Cube dimensions
cube_size = 2
cube_side_length = cube_size

rgb_tower_cube_template = {
    'xloc': 0,
    'yloc': 0,
    'zloc': 0,
    'rot_eul0x_deg': 0.0,
    'rot_eul1y_deg': 0.0,
    'rot_eul2z_deg': 0.0,
    'size': cube_size,
    'mass': 20,
    'collision_shape': 'BOX',
    'friction': 1,
    'use_margin': True,
    'collision_margin': 0,
    'linear_damping': 0.35,
    'angular_damping': 0.6,
    'color_x': 0.5,
    'color_y': 0.5,
    'color_z': 0.5
}


################################## FUNCTION AND CLASS DEFINITIONS ##################################

# No functions or classes are currently defined in this Boa file.

########################################## MAIN EXECUTION ##########################################

# Instantiate a boablend logger instance.
logger = boablend.util.Logger()

# Dump current environment info, just for illustrative purposes:
logger.dump_environment_info()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Select and then delete the default cube.
bpy.data.objects['Cube'].select_set(True)
bpy.ops.object.delete()  # This will delete all selected objects, so make sure of what is selected.

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Camera Setup for this project. Settings will provide the optimal framing of the tower animation.

# New instance of boablend.Camera with default boablend settings:
main_camera = boablend.camera.Camera()
# Optionally, we could apply desired settings at the time of instantiation:
#main_camera = boablend.camera.Camera(cam=rgb_cube_tower_camera_settings)
boablend_default_camera_settings = main_camera.get()
logger.log('Boablend camera class default camera settings:')
logger.dump(boablend_default_camera_settings)

# Note that the boablend default camera settings are not the same as Blender's.
# Right now we have boablend's stored in the instance but next we will retreive Blender's.
# Just above here we did look at boablend's default camera settings by using main_camera.get().
# But what we will do next is main_camera.read(), which retrieves and stores Blender's settings.

# First before changing any camera settings and for illustrative purposes, let's retrieve the
# current (default) camera settings from the blend file and dump them to the log.
# Read the active camera settings in the current blend file and store them in this instance.
# The camera.read() method also returns the settings/attributes dictionary.
blender_default_camera_settings = main_camera.read()
logger.log('Blender initial/default camera settings:')
logger.dump(blender_default_camera_settings)

# Next we store the settings we will need for rgb_cube_tower into this camera instance, but note
# that they will not be applied (written) to the blend file until we explicitly do so.
main_camera.store(rgb_cube_tower_camera_settings)
# Now 'write' them to the blend file, thus they are applied and take effect:
main_camera.write()
# Now, we can simply 'get' the settings back from the instance without causing anything to happen,
# such as if we used read() .. which would take the settings from the blend file first.
current_stored_camera_settings = main_camera.get()
logger.log('RGB cube tower camera settings:')
logger.dump(current_stored_camera_settings)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Instantiate a 'cube maker'.
# In the current design and for this Boa, it makes the most sense to just re-use a single instance
# of the primitive.cube.Cube class, but in other situations, we might want a separate instance of
# primitive.cube.Cube for each of many Cubes. These sorts of things are flexible and also the
# design of boablend itself is still very much in flux and such concepts are being explored as
# boablend evolves.

cube_maker = boablend.primitive.cube.Cube(cube=rgb_tower_cube_template)
# TODO: primitive.cube.Cube does not currently have accessors for individual cube attributes, so
# below you will see direct access to the cube dictionary in the instance. Currently I am
# considering various design patters to use in boablend where one of the challenges is having a
# high number of attributes for most Blender objects. Of course direct access is usually possible
# in Python, although not always desireable. One approach may be to provide accessors (or even
# just setters) for only the most commonly used attributes, such as position and color values as
# in the case of the current Boa.

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Tower Construction

current_z_position = 0

for a in range(0, cubes_z_height):
    current_z_position += cube_side_length
    current_y_position = 0
    #color_z = (a + 1) / cubes_z_height
    color_z = a / cubes_z_height
    for b in range(0, cubes_x_width):
        current_y_position += cube_side_length
        current_x_position = 0
        #color_x = (b + 1) / cubes_x_width
        color_x = b / cubes_x_width
        for c in range(0, cubes_y_depth):
            #cube = cube_defaults  # Now using class. Instance already created. Will be resused.
            #color_y = (c + 1) / cubes_y_depth
            color_y = c / cubes_y_depth
            location = (
                current_x_position + cube_side_length,
                current_y_position - cube_side_length,
                current_z_position - cube_side_length
            )
            cube_maker.set_location(location)
            rgb_tuple = (color_x, color_y, color_z)
            cube_maker.set_color(rgb_tuple)
            cube_maker.create()
            current_x_position += cube_side_length


####################################################################################################
# Remaining Manual Steps Requiring Automation
# The following steps are also required to build and render a complete animation as seen in the
# linked YouTube video.
#
# Most or all settings detailed below were the ones used for the demo YouTube video rendering:
# https://www.youtube.com/watch?v=1j7_nHfTeaw

# RGB Cube Tower is inspired by a tutorial video by 'Olav3D Tutorials':
# https://www.youtube.com/watch?v=KI0tjZUkb5A
# Watch this video to see the entirety of manual steps required to make a physics simulation and
# animation like this.

# - - - - - - - - - -

# - Instantiate floor plane.
# - Position/lower floor plane for desired fall height.
# - X,Y are 0,0. Z position is -38.88964.
# bpy.context.object.location[2] = -38.8896
# # - Plane scale XYZ are all 86.784.
# bpy.context.object.scale[0] = 86.7839
# bpy.context.object.scale[1] = 86.7839
# bpy.context.object.scale[2] = 86.7839

# - - - - - - - - - -

# - Go into Scene, Rigid Body World.
# bpy.context.space_data.context = 'SCENE'
# - Increase quality of animation by setting Steps Per Second.
# - 500 = good/high quality (Used for the example YouTube video.) Lower setting = faster render.

# - In Rigid Body Cache sub-section, set end point to 760 (frames).
# Before baking it is probably a good idea to trigger/click Free All Bakes, maybe also Free Bake
# which would be best to do first. Free Bake probably is not possible if there has never been bake
# and the same should be looked into for Free All Bakes.
# Free All Bakes: bpy.ops.ptcache.free_bake_all()
# Need the code for Free Bake.
# - Trigger (Click) Bake. This bake may take about 10 minutes.
# bpy.ops.ptcache.bake(bake=True)
# - Nearly all cubes have stopped moving after about 760 frames. Total duration about 9 seconds.

# - - - - - - - - - -

# - Set animation timeline end frame to 760 to match the physics bake.
# bpy.context.area.type = 'TIMELINE'
# bpy.context.scene.frame_end = 700

# - - - - - - - - - -

# Add a light of type Sun. ('layers' argument has been removed from below command for brevity.)
# bpy.ops.object.lamp_add(type='SUN', radius=1, view_align=False,
#     location=(-9.51748, 7.88541, -10.5362))
# The above values are not correct. Use the following:
# bpy.context.object.location[0] = 28.1261
# bpy.context.object.location[1] = -14.7615
# bpy.context.object.location[2] = 54.1666
# bpy.context.object.rotation_euler[0] = 0.265283
# bpy.context.object.rotation_euler[1] = -0.0242171
# bpy.context.object.rotation_euler[2] = 0.0888926
# The Sun's Strength needs to be set to 7 and this requires creating a Node.
# ** Node creation code not shown here, just the selection/setting of the Strength value.
# bpy.data.node_groups["Shader Nodetree"].nodes["Emission"].inputs[1].default_value = 7
# ** Attemted recreating Node and only the same setting code was generated.
# IMPORTANT: Above notes are from Blender 2.79, but things are different and actually more clear
# with Blender 2.80b. Nodes do not appear to be involved and things are straightforward:
# bpy.ops.object.light_add(type='SUN', radius=1, view_align=False, location=(0, 0, 0))
# bpy.context.space_data.context = 'DATA'
# bpy.context.object.data.energy = 7
# DECISION: Other differences between 2.79 and 2.80 have been noted elsewhere, but this difference
# is significant enough that the boablend project going forward will only support Blender 2.80.

# - - - - - - - - - -

# Set up render engine and render settings. See original Olav3D utorial video at 9:09.
# https://www.youtube.com/watch?v=KI0tjZUkb5A

# - - - - - - - - - -



# - - - - - - - - - -



# - - - - - - - - - -



# - - - - - - - - - -




##
#
