
####################################################################################################

import bpy  # This import works when executing within Blender but will show an import error in IDEs.
# /docs/import_bpy_error_in_ide.txt

#import boablend.constants as CONST
import math

default_sun = {
                'name': 'Sun',
                'comment': 'boablend.light.sun default values',
                'radius': 1,
                'energy': 7,
                'location.x': -5.0,
                'location.y': 5.0,
                'location.z': 40.0,
                'rot_eul0x_deg': -30.0,
                'rot_eul1y_deg': -20.0,
                'rot_eul2z_deg': 15.0
            }


################################## FUNCTION AND CLASS DEFINITIONS ##################################


class Sun:
    """class boablend.light.sun.Sun"""
    def __init__(self, sun=default_sun):
        self.sun = sun
    
    def store(self, sun):
        """Instance method boablend.light.sun.store()"""
        self.sun = sun

    def create(self):
        """The boablend.light.sun.create() method creates a new light of type sun in the blend
        file and applies the setings stored in this instance."""

        bpy.ops.object.light_add(type='SUN',
                                 radius=self.sun['radius'],
                                 location=(0, 0, 0))
        # We could set the location here in add_light but for now we will do that in a
        # separate step.

        #bpy.data.objects['Sun'].select_set(True)  # Turns out not necessary to select it in this
        # case
        
        # Energy/Strength
        bpy.context.object.data.energy = self.sun['energy']

        # Location
        bpy.context.object.location[0] = self.sun['location.x']
        bpy.context.object.location[1] = self.sun['location.y']
        bpy.context.object.location[2] = self.sun['location.z']

        # Rotation - Stored in degrees, assigned in radians
        bpy.context.object.rotation_euler[0] = math.radians(self.sun['rot_eul0x_deg'])
        bpy.context.object.rotation_euler[1] = math.radians(self.sun['rot_eul1y_deg'])
        bpy.context.object.rotation_euler[2] = math.radians(self.sun['rot_eul2z_deg'])

    def read(self):
        """The boablend.light.sun.read() method is not yet implemented."""

        sun = bpy.data.objects['Sun']  # Not tested

        # Read the attributes here

        return self.sun

    def get(self):
        """The boablend.light.sun.read() method returns the light/sun settings currently stored
        in this instance."""

        return self.sun


##
#
