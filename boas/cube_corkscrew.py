
####################################################################################################
# BOA: cube_corkscrew
####################################################################################################

####################################################################################################
import bpy  # This import works when executing within Blender but will show an import error in IDEs.
# Regarding import errors showing in your IDE for 'import bpy':
# See: /docs/import_bpy_error_in_ide.txt
####################################################################################################

import sys
import os
import math
import time

# See: /docs/sys_path_hack_in_boa_files.txt
dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir)

import boablend.camera
import boablend.util
import boablend.constants as CONST
import boablend.primitives.cube

# See: /docs/use_of_importlib_reload.txt
import importlib
importlib.reload(boablend)
importlib.reload(boablend.camera)
importlib.reload(boablend.util)
importlib.reload(boablend.constants)  # reload(CONST) works equally well. Use either.
importlib.reload(boablend.primitives.cube)


####################################################################################################


# Camera Settings

cube_corkscrew_camera_settings = {
    'name': 'Cube Corkscrew Camera - INCORRECT SETTINGS',
    'comment': 'boablend.Camera settings for the RGB Cube Tower project',
    'scene.camera.location.x': 67.37174224853516,
    'scene.camera.location.y': 62.108951568603516,
    'scene.camera.location.z': -22.072437286376953,
    'rot_eul0x_deg': 98.04878632691747,
    'rot_eul1y_deg': 0.00013285419354253954,
    'rot_eul2z_deg': -585.7637994372828,
    'render_resolution_x': 854,
    'render_resolution_y': 480,
    'scene.camera.data.angle': 88.22523942116491
}


# Corkscrew Structure Settings

# Radius of the corkscrew structure in Blender units
screw_radius = 16

# Height change per 360 degree revolution
screw_pitch = 6

# Number of full rotations in the corkscrew structure.
# Later we could consider supporting partial rotations by allowing specification of the total
# number of degrees to rotate through. The current design is to drive all calculations based
# on the angle, in an iterative manner, so we could specify two full rotations by specifying
# a total angular rotation of 360*2 = 720 etc. We will start with the simplest design by
# specifying integer full rotations.
screw_full_rotations = 4

completion_angle = 360 * screw_full_rotations

# Degrees of rotation separation between each cube
# IMPORTANT: This must divide equally into 360. e.g. 3, 15, 30, 45, 90, 180
# This requiremnt may be relaxed in future designs, but we are keeping the math simple at first.
cube_interval = 15  # degrees

intervals_per_rotation = 360 / cube_interval  # This needs to be an integer for now.

inter_cube_height_delta = screw_pitch / intervals_per_rotation

# Rotate each cube appropriately to keep the centerline parallel to a radius line.
# i.e. keep the cube faces tangentially parallel to what would be the cylinder walls.
# If this is false, all the cubes will be aligned the same with the world space XYZ axis.
#axis_align_cubes = True  # Currently not supported.

# Cube dimensions
cube_size = 2
cube_side_length = cube_size

corkscrew_cube_template = {
    'xloc': 0,
    'yloc': 0,
    'zloc': 0,
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
#main_camera = boablend.camera.Camera(cam=cube_corkscrew_camera_settings)
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
main_camera.store(cube_corkscrew_camera_settings)
# Now 'write' them to the blend file, thus applied and take effect:
main_camera.write()
# Now, we can simply 'get' the settings back from the instance without causing anything to happen,
# such as if we used read() .. which would take the settings from the blend file first.
current_stored_camera_settings = main_camera.get()
logger.log('RGB cube tower camera settings:')
logger.dump(current_stored_camera_settings)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

cube_maker = boablend.primitives.cube.Cube(cube=corkscrew_cube_template)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Corkscrew Construction

completion_angle = screw_full_rotations * 360

z_position = 0
angle = 0
total_angle = 0
rotation_number = 0  # This increments after every 360 degrees of rotation.
cube_number = 0  # This increments every time a cube is created.

# A refresher in basic geometry.
# Sine = Opposite / Hypotenuse = y / r
# Cosine = Adjacent / Hypotenuse = x / r
# Tangent = Opposite / Adjacent = y / x
# Hence:
# x = r * cos(angle)
# x = r * sin(angle)

state = {}

# Iterate until angle exceeds completion_angle, meaning angle = completion_angle will be included.
while (not total_angle > completion_angle):
    current_x_position = screw_radius * math.cos(angle*CONST.DEG_TO_EUL_FACTOR)
    current_y_position = screw_radius * math.sin(angle*CONST.DEG_TO_EUL_FACTOR)
    current_z_position = cube_number * inter_cube_height_delta
    cube_maker.cube['xloc'] = current_x_position
    cube_maker.cube['yloc'] = current_y_position
    cube_maker.cube['zloc'] = current_z_position
    state = {
        'angle': angle,
        'total_angle': total_angle,
        'completion_angle': completion_angle,
        'cube_number': cube_number,
        'cube_interval': cube_interval,
        'rotation_number': rotation_number,
        'inter_cube_height_delta': inter_cube_height_delta,
        'current_x_position': current_x_position,
        'current_y_position': current_y_position,
        'current_z_position': current_z_position
    }
    logger.dump(state)
    cube_maker.create()
    # Calcualtions for next iteration:
    angle += cube_interval
    total_angle += cube_interval
    cube_number += 1
    if angle > 360:
        rotation_number += 1
        angle = angle - 360
    # For debugging, would like to watch the cubes being created
    #bpy.context.view_layer.update()  # Does not appear to be causing the view to update as desired
    #time.sleep(1)


# for a in range(0, cubes_z_height):
#     current_z_position += cube_side_length
#     current_y_position = 0
#     #color_z = (a + 1) / cubes_z_height
#     color_z = a / cubes_z_height
#     for b in range(0, cubes_x_width):
#         current_y_position += cube_side_length
#         current_x_position = 0
#         #color_x = (b + 1) / cubes_x_width
#         color_x = b / cubes_x_width
#         for c in range(0, cubes_y_depth):
#             #cube = cube_defaults  # Now using class. Instance already created. Will be resused.
#             #color_y = (c + 1) / cubes_y_depth
#             color_y = c / cubes_y_depth
#             cube_maker.cube['xloc'] = current_x_position + cube_side_length
#             cube_maker.cube['yloc'] = current_y_position - cube_side_length
#             cube_maker.cube['zloc'] = current_z_position - cube_side_length
#             # cube_maker.cube['color_x'] = color_x
#             # cube_maker.cube['color_y'] = color_y
#             # cube_maker.cube['color_z'] = color_z
#             rgb_tuple = (color_x, color_y, color_z)
#             cube_maker.set_color(rgb_tuple)
#             cube_maker.create()
#             current_x_position += cube_side_length


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
