
####################################################################################################
# BOA: cube_corkscrew
####################################################################################################

####################################################################################################
import bpy  # This import works when executing within Blender but will show an import error in IDEs.
# See: /docs/import_bpy_error_in_ide.txt
####################################################################################################

import sys
import os
import math
import colorsys  # To convert HSV color to RGB color.
# Our corkscrew most readily provides TWO dimensions of change to use to map RGB colors for coloring
# each cube, with those being angle and height. To simplify mapping ALL the colors in the RGB color
# space, a good solution is to convert an HSV color, in which value is held constant at FULL, into
# RGB. For this we use the standard library colorsys. Colorsys is available in the standard Python 3
# libraries and also within Blender's built-in Python 3 environment.
# See: https://en.wikipedia.org/wiki/HSL_and_HSV

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


########################################## CONFIGURATION ###########################################

# Camera Settings

cube_corkscrew_camera_settings = {
    'name': 'Cube Corkscrew Camera',
    'comment': 'boablend.Camera settings for the cube_corkscrew boa',
    'scene.camera.location.x': -42.9565,
    'scene.camera.location.y': -41.8034,
    'scene.camera.location.z': 39.6792,
    'rot_eul0x_deg': 74.7548,
    'rot_eul1y_deg': 0.622499,
    'rot_eul2z_deg': -45.31,
    'render_resolution_x': 854,
    'render_resolution_y': 480,
    'scene.camera.data.angle': 100.38885695056194,
    'scene.camera.data.clip_start': 0.1,
    'scene.camera.data.clip_end': 300
}

# Corkscrew Structure Settings
default_corkscrew = {
    'screw_radius': 14,
    'screw_pitch': 18,
    'screw_full_rotations': 22,
    'cube_interval': 15,
    'screw_height_offset': 50,
    'axis_align_cubes': True
}

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

current_corkscrew = default_corkscrew

# Radius of the corkscrew structure in Blender units
screw_radius = current_corkscrew['screw_radius']

# Height unit change per 360 degree revolution
screw_pitch = current_corkscrew['screw_pitch']

# Number of full rotations in the corkscrew structure.
# Later we could consider supporting partial rotations by allowing specification of the total
# number of degrees to rotate through. The current design is to drive all calculations based
# on the angle, in an iterative manner, so we could specify two full rotations by specifying
# a total angular rotation of 360*2 = 720 etc. We will start with the simplest design by
# specifying integer full rotations and then calculate a full multiple of 360 for our
# 'completion_angle'
screw_full_rotations = current_corkscrew['screw_full_rotations']

# Calculate completion angle. It is useful to track the total_angle because it increases linearly
# similar to cube_number and so it is also useful to calculate completion_angle to use as a
# stopping point.
completion_angle = screw_full_rotations * 360

# Degrees of rotation separation between each cube.
# IMPORTANT: This must divide equally into 360. e.g. 3, 15, 30, 45, 90, 180
# This requiremnt may be relaxed in future designs, but we are keeping the math simple at first.
cube_interval = current_corkscrew['cube_interval']  # Degrees

# Calculate the intervals per rotation.
intervals_per_rotation = 360 / cube_interval  # This needs to be an integer for now.

# Calculate the height change/delta between consecutive cubes, using the screw pitch and the
# intervals per rotation we just calculated.
inter_cube_height_delta = screw_pitch / intervals_per_rotation

# Rotate each cube appropriately to keep the centerline parallel to a radius line.
# i.e. keep the cube faces tangentially parallel to what would be the cylinder walls.
# If this is false, all the cubes will be aligned the same with the world space XYZ axis.
#axis_align_cubes = True  # Currently not supported.

# Height offset for the entire corkscrew, useful for setting the drop height for physics
# simulation and animation.
screw_height_offset = current_corkscrew['screw_height_offset']

# Cube dimensions
cube_size = 2

# Default cube attributes
corkscrew_cube_defaults = {
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

# Deselect all in case something unexpected is selected in the blend file.
bpy.ops.object.select_all(action='DESELECT')

# Select and then delete the default cube.
bpy.data.objects['Cube'].select_set(True)
bpy.ops.object.delete()  # This will delete all selected objects, so make sure of what is selected.

# Select and then delete the default light.
bpy.data.objects['Light'].select_set(True)
bpy.ops.object.delete()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Camera Setup

# New instance of boablend.Camera with default boablend settings:
main_camera = boablend.camera.Camera()

# After manually positioning and adjusting the main camera for the desired results, use the
# following camera.read() code to capture those camera settings from the blend file and dump them
# to the log. Then copy those settings into the camera settings dictionary near the top of this Boa
# file. Once this is done, disable this block of code and allow the Boa file to set the camera using
# the camera.write() code below here.
# In the future this process will be more streamlined and automated.
#camera_settings_read_from_blend_file = main_camera.read()
#logger.log('Camera settings obtained from Blender GUI:')
#logger.dump(camera_settings_read_from_blend_file)

# Next we store the settings we will need for rgb_cube_tower into this camera instance, but note
# that they will not be applied (written) to the blend file until we explicitly do so.
main_camera.store(cube_corkscrew_camera_settings)
# Now 'write' them to the blend file, thus they are applied and take effect:
main_camera.write()

# NOTE: Make sure to disable the above two lines of camera.write() code when performing the read()
# steps. Also, after the camera.read() steps, disable that code and re-enable the write code.

# TODO: Consider putting the camera.read() vs. camera.write() steps and their comments into
# distinct functions so that they can be more easily and clearly isolated from each other and
# executed correctly from a single point.
# BUT .. once the Boa is developed .. the read steps may never be needed again. Perhaps we need to
# make different kinds of Boas .. finished 'recipe' Boas vs. tutorial/template Boas for people to
# use to develop their own unique Boas.

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Lighting Setup

bpy.ops.object.light_add(type='SUN', radius=1, location=(0, 0, 0))


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Physics Setup - Scene, Rigid Body World Setup

bpy.ops.rigidbody.world_add()
bpy.data.scenes['Scene'].rigidbody_world.steps_per_second = 500
bpy.context.scene.frame_end = 680



# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Animation Setup


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

cube_maker = boablend.primitives.cube.Cube(cube=corkscrew_cube_defaults)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Create ground plane, scale it and assign physics attributes to it.
bpy.ops.mesh.primitive_plane_add(size=2, enter_editmode=False, location=(0, 0, 0))
# TODO: Certainly this scale can be simplified, probably to:
#bpy.ops.transform.resize(value=(90, 90, 90))
bpy.ops.transform.resize(value=(90, 90, 90),
                         orient_type='GLOBAL',
                         orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
                         orient_matrix_type='GLOBAL',
                         mirror=True,
                         use_proportional_edit=False,
                         proportional_edit_falloff='SMOOTH',
                         proportional_size=1,
                         use_proportional_connected=False,
                         use_proportional_projected=False)
bpy.ops.rigidbody.object_add()
bpy.context.object.rigid_body.type = 'PASSIVE'
bpy.context.object.rigid_body.collision_shape = 'MESH'
bpy.context.object.rigid_body.collision_margin = 0


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


# Corkscrew Construction

# Initialize the iteration variables
current_z_position = 0
current_x_position = 0
current_z_position = 0
angle = 0
total_angle = 0
rotation_number = 0  # This increments after every 360 degrees of rotation.
cube_number = 0  # This increments every time a cube is created.
angle_ratio = 0
total_angle_ratio = 0
red = 0
green = 0
blue = 0

# A refresher in basic geometry:
# Sine = Opposite / Hypotenuse = y / r
# Cosine = Adjacent / Hypotenuse = x / r
# Tangent = Opposite / Adjacent = y / x
# Hence:
# x = r * Cosine(degrees_angle)
# x = r * Sine(degrees_angle)
#
# x = r * math.cos(radian_angle)
# x = r * math.sin(radian_angle)

# To be used for inner-loop logging.
state = {}

# Iterate until angle exceeds completion_angle, meaning angle = completion_angle will be included.
while (not total_angle > completion_angle):
    angle_ratio = angle / 360
    total_angle_ratio = total_angle / completion_angle
    current_x_position = screw_radius * math.cos(angle*CONST.DEG_TO_EUL_FACTOR)
    current_y_position = screw_radius * math.sin(angle*CONST.DEG_TO_EUL_FACTOR)
    current_z_position = (cube_number * inter_cube_height_delta) + screw_height_offset
    cube_maker.cube['xloc'] = current_x_position
    cube_maker.cube['yloc'] = current_y_position
    cube_maker.cube['zloc'] = current_z_position

    # This color model is nice, but let's try using an HSV conversion so we can more easily get ALL
    # of the RGB colors.
    #
    # # Red will cycle from zero to full each 360 degree rotation
    # red = angle_ratio
    # # Green will increase from zero to full from bottom to top
    # green = total_angle_ratio
    # # Blue will increase from zero to full from top to bottom
    # blue = total_angle_ratio
    # rgb_tuple = (red, green, blue)

    fixed_hsv_saturation = 1

    hsv_hue = angle_ratio
    #hsv_saturation = total_angle_ratio
    hsv_saturation = fixed_hsv_saturation
    hsv_value = total_angle_ratio
    rgb_tuple = colorsys.hsv_to_rgb(hsv_hue, hsv_saturation, hsv_value)

    cube_maker.set_color(rgb_tuple)
    # For logging
    state = {
        'angle': angle,
        'total_angle': total_angle,
        'completion_angle': completion_angle,
        'angle_ratio': angle_ratio,
        'total_angle_ratio': total_angle_ratio,
        'cube_number': cube_number,
        'cube_interval': cube_interval,
        'rotation_number': rotation_number,
        'intervals_per_rotation': intervals_per_rotation,
        'inter_cube_height_delta': inter_cube_height_delta,
        'current_x_position': current_x_position,
        'current_y_position': current_y_position,
        'current_z_position': current_z_position
    }
    #logger.dump(state)
    cube_maker.create()
    # Calcualtions for next iteration:
    angle += cube_interval
    total_angle += cube_interval
    cube_number += 1
    if angle >= 360:
        rotation_number += 1
        angle = angle - 360
    # For debugging, would like to watch the cubes being created
    #bpy.context.view_layer.update()  # Does not appear to be causing the view to update as desired
    #time.sleep(1)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

#bpy.context.area.type = 'PROPERTIES'
# The above line appears to work, but we still are getting a context error when we try to bake:
# RuntimeError: Operator bpy.ops.ptcache.bake.poll() failed, context is incorrect

#bpy.ops.rigidbody.bake_to_keyframes(frame_start=1, frame_end=600, step=1)
# No I don't think we want to bake to keyframes .. just trying to trigger a standard bake.
# Having trouble finding a way to set the end_frame for the Simulation/Bake.
#bpy.ops.ptcache.bake(bake=True)



##
#
