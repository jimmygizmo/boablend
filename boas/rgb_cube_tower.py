
####################################################################################################
####################################### BOABLEND ENTRY POINT #######################################


# This 'import bpy' will show as broken in the IDE if bpy is not installed in the external
# environment, however since this script is invoked via exec() from within the Blender internal
# Python environment, it will be imported successfully there.
import bpy

import sys
import os

# TODO: IMPROVE THINGS WITH pip install -e.
# If we use setup.py correctly AND include a step to 'pip install -e .' into the .venv, then the
# idea is that any changes to the code WILL be immediately picked up within the .venv thus
# eliminating the need for the path hack, for testing anyhow.
# It is not yet clear if this will also eliminate the need for the below but it might lead to
# something along those lines. See, we should use the .venv for more than just the IDE and /tests/
# but it is not clear how Blender fits into that. Again, it may be that this is another thing we
# need to enable 'external execution and hence the import of bpy etc.' .. to be able to do.


####################################################################################################
# Add the current directory to the list of directories Python will search to find modules for
# importing. In the current format, this project is only executed from within Blender using the
# built-in Python environment. Importing of Boablend from the current project/repository directory
# is enabled in this manner so that the Boablend module does not need to be installed within
# Blender's python envirnoment. This configuration may change in the future as there are a few other
# execution/module-installation configurations under consideration.
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

# At a later date, camera scale values may also be supported, but currently are not:
    # 'scene.camera.scale.x': 1.0,
    # 'scene.camera.scale.y': 1.0,
    # 'scene.camera.scale.z': 1.0,


########################################## MAIN EXECUTION ##########################################


# New instance of boablend.Camera with the specified settings:
main_camera = boablend.camera.Camera(bpy, cam=rgb_cube_tower_camera_settings)

# New instance of boablend.Camera which will use the class default settings:
#main_camera = boablend.camera.Camera(bpy)

# Apply the camera settings currently stored in this instance to the current blend file:
main_camera.apply_camera()

# Read the camera settings in the current blend file and store them in this instance:
#main_camera.get_camera()

# Log the camera settings currently stored in this instance to the console:
main_camera.log_camera()


##
#
