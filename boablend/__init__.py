#! /usr/bin/env python3

# The import of bpy works within Blender. However, extra steps are needed in order to
# make it work for external execution as well as to make it recognized by the IDE
# as a valid import. To install bpy requires compilation it and this is currently
# failing. When the bpy build and python module install is working, then we
# can make 'import bpy' work for external execution and for the VSCode/IDE code
# inspection features. See the build error log in this repo and comments in init.sh
# for more information on the bpy build failure.
# This does not prevent the use of boablend within Blender, but it would be nice to fix
# for a more complete and full-featured project.

#import bpy  #Bpy install compile fails. This does not affect executing within Blender.
import sys


# For converting XYZ Degrees values to Euler Values for Rotation
PI = 3.14159265
DEG_TO_EUL_FACTOR = (PI/180.0)  # 0.0174532925

# For converting Euler Values for Rotation to XYZ Degrees values
EUL_TO_DEG_FACTOR = (180.0/PI) # 57.29577957855229


################################## FUNCTION AND CLASS DEFINITIONS ##################################


class Camera:
    def __init__(self, bpy, cam):
        if not cam:
            cam = {
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
        self.cam = cam
# Attribute/key names in the cam dictionary are identical to Blender internal
# references to the same data, except for the following which were given symbols
# for brevity and clarity.
# 'rot_eul0x_deg' is the symbol for 'scene.camera.rotation_euler[0] in degrees'  # X
# 'rot_eul1y_deg' is the symbol for 'scene.camera.rotation_euler[1] in degrees'  # Y
# 'rot_eul2z_deg' is the symbol for 'scene.camera.rotation_euler[2] in degrees'  # Z


    def setup_camera(self, bpy):
        scene = bpy.data.scenes["Scene"]

        # Camera Location
        scene.camera.location.x = self.cam['scene.camera.location.x']
        scene.camera.location.y = self.cam['scene.camera.location.y']
        scene.camera.location.z = self.cam['scene.camera.location.z']

        # Camera Rotation - Degrees - Rotation Mode: 'XYZ Euler'/'XYZ'
        scene.camera.rotation_mode = 'XYZ'
        scene.camera.rotation_euler[0] = self.cam['rot_eul0x_deg']*DEG_TO_EUL_FACTOR
        scene.camera.rotation_euler[1] = self.cam['rot_eul1y_deg']*DEG_TO_EUL_FACTOR
        scene.camera.rotation_euler[2] = self.cam['rot_eul2z_deg']*DEG_TO_EUL_FACTOR

        # Camera FOV - Degrees
        scene.camera.data.angle = self.cam['scene.camera.data.angle']*DEG_TO_EUL_FACTOR

        scene.render.resolution_x = self.cam['render_resolution_x']
        scene.render.resolution_y = self.cam['render_resolution_y']

        # Camera Scale [UNUSED/UNTESTED]
        # Try this out. We can read the data via: bpy.data.objects['Camera'].scale.x etc.
        # Noting that we are using scene.camera instead of bpy.data.objects['Camera']
        # in the below proposed method to set camera scale values.
        # And scene = bpy.data.scenes["Scene"] .. SO:
        # bpy.data.objects['Camera'] = bpy.data.scenes["Scene"].camera
        #
        # scene.camera.scale.x = self.cam['scene.camera.scale.x']
        # scene.camera.scale.y = self.cam['scene.camera.scale.y']
        # scene.camera.scale.z = self.dcam['scene.camera.scale.z']


########################################## MAIN EXECUTION ##########################################
# Direct execution is not supported in this module and it is only intended to be imported.

# if __name__ == '__main__':
#     sys.exit(f"This file [{__file__}] is meant to be imported, not executed directly.")

##
#
