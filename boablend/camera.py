
####################################################################################################
import bpy  # This import works when executing within Blender but will show an import error in IDEs.
# Regarding import errors showing in your IDE for 'import bpy':
# /docs/import_bpy_error_in_ide.txt
####################################################################################################

import boablend.constants as CONST

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
    """The boablend.Camera class stores, obtains, applies and generally manipulates camera settings.
    Only the subset of Blender camera attributes which Boablend deals with are handled."""
    def __init__(self, cam=default_camera):
        self.cam = cam
    # Attribute/key names in the cam dictionary are identical to Blender internal references to the
    # same data, except for the following which were given custom symbols for brevity and clarity.
    # 'rot_eul0x_deg' is the symbol for 'scene.camera.rotation_euler[0] in degrees'  # X
    # 'rot_eul1y_deg' is the symbol for 'scene.camera.rotation_euler[1] in degrees'  # Y
    # 'rot_eul2z_deg' is the symbol for 'scene.camera.rotation_euler[2] in degrees'  # Z

    # TODO: Consider using @property and more standardized accessors. We might also make a parent
    # class perhaps called Entity and define generic accessors in a pythonic way and always use a
    # single 'props' dictionary to hold whatever properties a specific kind of object needs.
    # If every object/entity boablend deals with will have a generic getter and setter for a generic
    # props dictionary then this would makes sense. Still carefully considering the design patterns
    # in this area.
    

    def store(self, cam):
        """The store() method takes a camera settings dictionary and stores those settings in the
        current instance. Settings are not applied to an actual camera. Use the apply() method to
        cause the settings to take effect on the Blender main camera."""

        self.cam = cam


    def write(self):
        """The write() method applies the camera settings currently stored in the instance to the
        Blender main camera at which point they take effect."""

        scene = bpy.data.scenes["Scene"]

        # Camera Location
        scene.camera.location.x = self.cam['scene.camera.location.x']
        scene.camera.location.y = self.cam['scene.camera.location.y']
        scene.camera.location.z = self.cam['scene.camera.location.z']

        # Camera Rotation - Degrees - Rotation Mode: 'XYZ Euler'/'XYZ'
        scene.camera.rotation_mode = 'XYZ'
        scene.camera.rotation_euler[0] = self.cam['rot_eul0x_deg']*CONST.DEG_TO_EUL_FACTOR
        scene.camera.rotation_euler[1] = self.cam['rot_eul1y_deg']*CONST.DEG_TO_EUL_FACTOR
        scene.camera.rotation_euler[2] = self.cam['rot_eul2z_deg']*CONST.DEG_TO_EUL_FACTOR

        # Camera FOV - Degrees
        scene.camera.data.angle = self.cam['scene.camera.data.angle']*CONST.DEG_TO_EUL_FACTOR

        # Render Resolution / Aspect Ratio
        scene.render.resolution_x = self.cam['render_resolution_x']
        scene.render.resolution_y = self.cam['render_resolution_y']


    def read(self):
        """The read() method obtains the current main camera settings from the active blend file,
        stores those settings in the boablend camera instance and returns a camera settings
        dictionary."""

        obj = bpy.data.objects['Camera']  # bpy.types.Camera
        self.cam['name'] = 'Main Camera'
        self.cam['comment'] = 'from boablend.Camera.get_camera'

        # Camera Location
        # NOTE: We had to make these obj.location.* into str() to print them
        # but it is most likely that we do not need to do anything like that to
        # store or use them to set a camera. Just making a note on this.
        # TODO: Clarify this situation by showing the TYPEOF these and document it:
        self.cam['scene.camera.location.x'] = obj.location.x
        self.cam['scene.camera.location.y'] = obj.location.y
        self.cam['scene.camera.location.z'] = obj.location.z

        # Camera Rotation - Degrees - Rotation Mode: 'XYZ Euler'/'XYZ'
        # Obtained as Euler values, Stored as Degrees.
        self.cam['rot_eul0x_deg'] = obj.rotation_euler[0]*CONST.EUL_TO_DEG_FACTOR
        self.cam['rot_eul1y_deg'] = obj.rotation_euler[1]*CONST.EUL_TO_DEG_FACTOR
        self.cam['rot_eul2z_deg'] = obj.rotation_euler[2]*CONST.EUL_TO_DEG_FACTOR

        scene = bpy.data.scenes["Scene"]

        # Render Resolution / Aspect Ratio
        self.cam['render_resolution_x'] = scene.render.resolution_x
        self.cam['render_resolution_y'] = scene.render.resolution_y

        # Camera FOV - Obtained as Euler values, Stored as Degrees.
        self.cam['scene.camera.data.angle'] = scene.camera.data.angle*CONST.EUL_TO_DEG_FACTOR

        return self.cam


    def get(self):
        """The get() method returns the camera settings dictionary currently stored in the
        instance."""

        return self.cam


##
#
