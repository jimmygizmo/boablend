
####################################################################################################

import bpy  # This import works when executing within Blender but will show an import error in IDEs.
# Regarding import errors showing in your IDE for 'import bpy':
# /docs/import_bpy_error_in_ide.txt

import boablend.constants as CONST
import math

# Cube dimensions
# NOTE: These may actually belong in client code and we can just pick a default value for the
# default cube dictionary and then override it. We moved these here from client code we are
# adapting to make this class and over there these values are used in tower dimension calculations
# which is why there are separate like this. Different structuring rules apply for this class.
default_cube_size = 2
cube_side_length = default_cube_size

# These default_cube settings are stored in a new Cube instance when no such settings are
# supplied to the Cube constructor.
default_cube = {
    'xloc': 0,
    'yloc': 0,
    'zloc': 0,
    'rot_eul0x_deg': 0.0,
    'rot_eul1y_deg': 0.0,
    'rot_eul2z_deg': 0.0,
    'size': default_cube_size,
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


class Cube:
    """The boablend.Cube class stores attributes of a cube primitive and can create a cube primitive
    with the stored attributes. Only the subset of attributes which Boablend deals with are
    handled."""
    def __init__(self, cube=default_cube):
        self.cube = cube

    def store(self, cube):
        """The store() method takes a cube attributes dictionary and stores those attributes in the
        current instance. Use the create() method to instantiate a cube primitive with the stored
        settings."""

        self.cube = cube
    
    def create(self):
        # Create the mesh object.
        bpy.ops.mesh.primitive_cube_add(
            size = self.cube['size'],
            location = (self.cube['xloc'], self.cube['yloc'], self.cube['zloc']),
            rotation = (
                math.radians(self.cube['rot_eul0x_deg']),
                math.radians(self.cube['rot_eul1y_deg']),
                math.radians(self.cube['rot_eul2z_deg'])
            )
        )

        # Add and adjust the physics.
        bpy.ops.rigidbody.object_add()
        obj = bpy.context.object  # For more concise code.
        obj.rigid_body.mass = self.cube['mass']
        obj.rigid_body.collision_shape = self.cube['collision_shape']
        obj.rigid_body.friction = self.cube['friction']
        obj.rigid_body.use_margin = self.cube['use_margin']
        obj.rigid_body.collision_margin = self.cube['collision_margin']
        obj.rigid_body.linear_damping = self.cube['linear_damping']
        obj.rigid_body.angular_damping = self.cube['angular_damping']

        mat_name = 'mat_' + str(self.cube['color_x']) + \
                    '_' + str(self.cube['color_y']) + \
                    '_' + str(self.cube['color_z'])
        mat = bpy.data.materials.new(name=mat_name)
        mat.diffuse_color = (self.cube['color_x'],
                             self.cube['color_y'],
                             self.cube['color_z'],
                             CONST.ALPHA_FULL_OPAQUE)

        # Can't assign materials in editmode. Enter object mode.
        bpy.ops.object.mode_set(mode='OBJECT')

        bpy.context.object.active_material = mat

    def set_color(self, rgb_color=(1,1,1)):
        (self.cube['color_x'], self.cube['color_y'], self.cube['color_z']) = rgb_color

    def get(self):
        """The get() method returns the cube attributes dictionary currently stored in the
        instance."""

        return self.cube


##
#
