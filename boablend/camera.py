#! /usr/bin/env python3
####################################################################################################
# This module code is not meant to be executed, but the shebang is here to support issuing a warning
# through the __main__ block at the end of the file if direct execution is attempted.

####################################################################################################
#import bpy  # This import is not needed under the current execution model and it will not currently
# work because we do not yet have an external bpy build in the boablend environment.
#
# The import of bpy of course DOES work within Blender and when execution begins within the boablend
# Blender hook code. However, extra steps are needed in order to make it work for external execution
# as well as to make it recognized by the IDE as a valid import. To install bpy requires compilation
# and this is currently failing. When the bpy build and python module install is working, then we
# can make 'import bpy' work for external execution and for the VSCode/IDE code inspection features.
# See the build error log in this repo and comments in init.sh for more information on the bpy build
# failure. This does not prevent the use of boablend within Blender, but it would be nice to fix for
# a more complete and full-featured project.


import sys
import pprint


# For converting XYZ Degrees values to Euler Values for Rotation
PI = 3.14159265
DEG_TO_EUL_FACTOR = (PI/180.0)  # 0.0174532925

# For converting Euler Values for Rotation to XYZ Degrees values
EUL_TO_DEG_FACTOR = (180.0/PI) # 57.29577957855229

# These default_camera settings are stored in a new Camera instance when no such settings are
# supplied to the Camera constructor. These settings are not particularly useful since they
# represent a camera directly over the origin at a height of 10 units, pointing directly down, with
# Blender default FOV and resolution settings. These default settings are mostly useful during
# development as they are unique enough to be able to easily tell if the Blender defaults or the
# boablend.Camera defaults are the currently applied settings. Later, when development of
# boablend.Camera is not so active, perhaps these defaults should just be identical to Blender's.
default_camera = {
                'name': 'Camera',
                'comment': 'boablend.Camera default values',
                'scene.camera.location.x': 0.0,
                'scene.camera.location.y': 0.0,
                'scene.camera.location.z': 10.0,
                'rot_eul0x_deg': 0.0,
                'rot_eul1y_deg': 0.0,
                'rot_eul2z_deg': 0.0,
                'render_resolution_x': 1920,
                'render_resolution_y': 1080,
                'scene.camera.data.angle': 49.134342133748646
            }


################################## FUNCTION AND CLASS DEFINITIONS ##################################


class Camera:
    def __init__(self, bpy, cam=default_camera):
        self.bpy = bpy
        self.cam = cam
# Attribute/key names in the cam dictionary are identical to Blender internal references to the same
# data, except for the following which were given custom symbols for brevity and clarity.
# 'rot_eul0x_deg' is the symbol for 'scene.camera.rotation_euler[0] in degrees'  # X
# 'rot_eul1y_deg' is the symbol for 'scene.camera.rotation_euler[1] in degrees'  # Y
# 'rot_eul2z_deg' is the symbol for 'scene.camera.rotation_euler[2] in degrees'  # Z


    def apply_camera(self):
        scene = self.bpy.data.scenes["Scene"]

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

        # Render Resolution / Aspect Ratio
        scene.render.resolution_x = self.cam['render_resolution_x']
        scene.render.resolution_y = self.cam['render_resolution_y']


    def get_camera(self):
        obj = self.bpy.data.objects['Camera']  # bpy.types.Camera
        self.cam['name'] = 'Main Camera'
        self.cam['comment'] = 'from boablend.Camera.get_camera'

        # Camera Location
        # NOTE: We had to make these obj.location.* into str() to print them
        # but it is most likely that we do not need to do anything like that to
        # store or use them to set a camera. Just making a note on this.
        self.cam['scene.camera.location.x'] = obj.location.x
        self.cam['scene.camera.location.y'] = obj.location.y
        self.cam['scene.camera.location.z'] = obj.location.z

        # Camera Rotation - Degrees - Rotation Mode: 'XYZ Euler'/'XYZ'
        # Obtained as Euler values, Stored as Degrees.
        self.cam['rot_eul0x_deg'] = obj.rotation_euler[0]*EUL_TO_DEG_FACTOR
        self.cam['rot_eul1y_deg'] = obj.rotation_euler[1]*EUL_TO_DEG_FACTOR
        self.cam['rot_eul2z_deg'] = obj.rotation_euler[2]*EUL_TO_DEG_FACTOR

        scene = self.bpy.data.scenes["Scene"]

        # Render Resolution / Aspect Ratio
        self.cam['render_resolution_x'] = scene.render.resolution_x
        self.cam['render_resolution_y'] = scene.render.resolution_y

        # Camera FOV - Obtained as Euler values, Stored as Degrees.
        self.cam['scene.camera.data.angle'] = scene.camera.data.angle*EUL_TO_DEG_FACTOR

    
    def log_camera(self):
        pp = pprint.PrettyPrinter(indent=4)
        print("Currently stored boablend.Camera settings:")
        print("NOTE: These are the settings stored in the current boablend.Camera instance and "
              "may or may not have been applied to the current blend file.")
        pp.pprint(self.cam)


########################################## MAIN EXECUTION ##########################################
# This module and this file are only intended to be imported for use, not directly executed.


if __name__ == '__main__':
    sys.exit("This file [{}] is part of the boablend module which is meant to be imported, "
             "not executed directly.".format(__file__))


##
#
