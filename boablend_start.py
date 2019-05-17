
# This 'import bpy' will show as broken in the IDE if bpy is not installed in the
# external environment, however since this script is invoked via exec() from within
# the Blender internal Python environment, it will be imported successfully there.
import bpy

import sys
import os

dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir)

import boablend

import importlib
importlib.reload(boablend)


main_camera_settings = {
    'scene.camera.location.x': 67.37174224853516,
    'scene.camera.location.y': 62.108951568603516,
    'scene.camera.location.z': -22.072437286376953,
    'rot_eul0x_deg': 98.04878632691747,
    'rot_eul1y_deg': 0.00013285419354253954,
    'rot_eul2z_deg': -585.7637994372828,
    'scene.camera.scale.x': 1.0,
    'scene.camera.scale.y': 1.0,
    'scene.camera.scale.z': 1.0,
    'render_resolution_x': 854,
    'render_resolution_y': 480,
    'scene.camera.data.angle': 88.22523942116491
}

# New instance of boablend.Camera with the specified settings
main_camera = boablend.Camera(bpy, main_camera_settings)

main_camera.setup_camera(bpy)  # Apply the settings to the current Blend file

##
#
