
####################################################################################################
# BOA: rgb_cube_tower

# This 'import bpy' will show as broken in the IDE if bpy is not installed in the external
# environment, however since this script is invoked via exec() from within the Blender internal
# Python environment, it will be imported successfully there.
import bpy

import sys
import os

# TODO: If and when we can execute things outside of Blender, we can improve things a lot and
# eliminate the need for any path hacks by using 'pip install -e .' The -e option of pip install
# in this local install context will perform the module install using symlinks and then we can
# develop the module in its repository location and the .venv will immediately reflect the changes.
# setup.py will need to be in the correct format.

# Since we are currently only executing from within Blender, we will still need to use the
# following path hack.

####################################################################################################
# Add the current directory of the current blend file to the list of directories Python will search
# to find modules for importing. In the current format, this project is only executed from within
# Blender using the built-in Python environment. Importing of Boablend from the current
# project/repository directory is enabled in this manner so that the Boablend module does not need
# to be installed within Blender's python envirnoment. This configuration may change in the future
# as there are a few other execution/module-installation configurations under consideration.
dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir)
import boablend
import boablend.camera
# Importlib's reload() is used to ensure that every time this project is executed, any Boablend code
# changes will be picked up. This is necessary in the case that the Blender file containing the
# Boablend hook has not been restarted because Blender's Python environment internally caches
# imported modules and this cache persists while the blend file is open.
import importlib
importlib.reload(boablend)
importlib.reload(boablend.camera)
####################################################################################################


# Camera Settings

# These camera settings are great for the animation of the tower falling and shattering and were
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
    'scene.camera.data.angle': 88.22523942116491
}
# 'rot_eul0x_deg' is the symbol for 'scene.camera.rotation_euler[0] in degrees'  # X
# 'rot_eul1y_deg' is the symbol for 'scene.camera.rotation_euler[1] in degrees'  # Y
# 'rot_eul2z_deg' is the symbol for 'scene.camera.rotation_euler[2] in degrees'  # Z


# Tower/Cube Settings

# This version now creates a custom material for each cube and maps the entire RGB color space into the
# XYZ space based on the position/index of each cube. Pure black to pure white is fully mapped across RGB/XYZ space.

# This code will be compiled and run inside Blender using the built in Python
# interpreter which is a version 2.x interpreter.

# This code is compatible with Blender 2.79b. Cube size set via 'radius='.
# This code is not compatible with Blender 2.80b. Cube size set via 'size='.
# When porting between the two version note that size = 2 * radius.

# The cube origin is in the volumetric center of the cube as instantiated by
# bpy.ops.mesh.primitive_cube_add(). Obviously this is necessary to know in order
# to perform location calculations in the main execution code.

# Dimensions of the tower of cubes as number of cubes:
cubes_x_width = 8
cubes_y_depth = 8
cubes_z_height = 24

# Cube dimensions
cube_radius = 1
cube_side_length = 2 * cube_radius
# Version 2.80b NOTE: Change the attribute name from 'radius' to 'size' and use cube_side_length
# as the radius. Make sure to change the corresponding variable names for consistency.

cube_defaults = {
    'xloc': 0,
    'yloc': 0,
    'zloc': 0,
    'radius': cube_radius,
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


def instantiate_cube(cube):
    # Create the mesh object.
    bpy.ops.mesh.primitive_cube_add(
        radius = cube['radius'],
        location = (cube['xloc'], cube['yloc'], cube['zloc'])
    )

    # Add and adjust the physics.
    bpy.ops.rigidbody.object_add()
    obj = bpy.context.object  # For more concise code.
    obj.rigid_body.mass = cube['mass']
    obj.rigid_body.collision_shape = cube['collision_shape']
    obj.rigid_body.friction = cube['friction']
    obj.rigid_body.use_margin = cube['use_margin']
    obj.rigid_body.collision_margin = cube['collision_margin']
    obj.rigid_body.linear_damping = cube['linear_damping']
    obj.rigid_body.angular_damping = cube['angular_damping']

    mat_name = 'mat_' + str(cube['color_x']) + \
                  '_' + str(cube['color_y']) + \
                  '_' + str(cube['color_z'])
    mat = bpy.data.materials.new(name=mat_name)
    mat.diffuse_color = (cube['color_x'], cube['color_y'], cube['color_z'])

    bpy.ops.object.mode_set(mode='OBJECT')  # Can't assign materials in editmode. Enter object mode.

    bpy.context.object.active_material = mat


########################################## MAIN EXECUTION ##########################################


# Camera Setup

# New instance of boablend.Camera with the specified settings:
main_camera = boablend.camera.Camera(bpy, cam=rgb_cube_tower_camera_settings)

# Apply the camera settings currently stored in this instance to the current blend file:
main_camera.apply_camera()

# Read the camera settings in the current blend file and store them in this instance:
#main_camera.get_camera()

# Log the camera settings currently stored in this instance to the console:
main_camera.log_camera()


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
            cube = cube_defaults
            #color_y = (c + 1) / cubes_y_depth
            color_y = c / cubes_y_depth
            cube['xloc'] = current_x_position + cube_side_length
            cube['yloc'] = current_y_position - cube_side_length
            cube['zloc'] = current_z_position - cube_side_length
            cube['color_x'] = color_x
            cube['color_y'] = color_y
            cube['color_z'] = color_z
            instantiate_cube(cube)
            current_x_position += cube_side_length


# World and Animation Setup

# - Go into World, Rigid Body Physics



##
#
