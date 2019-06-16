
####################################### BOABLEND ENTRY POINT #######################################

import bpy  # This import works when executing within Blender but will show an import error in IDEs.
# /docs/import_bpy_error_in_ide.txt

import os

verbose = True

boadir = 'boas'

default_boa = 'rgb_cube_tower_small.py'
#default_boa = 'rgb_cube_tower.py'
#default_boa = 'cube_corkscrew.py'
#default_boa = 'cube_corkscrew_deluxe.py'

boa_sub_path = os.path.join(boadir, default_boa)
boapath = bpy.path.abspath("//{}".format(boa_sub_path))

if verbose:
    print()
    print("~ ~ ~ ~ ~ ~ ~ ~ Boablend dispatching boa: {}".format(default_boa))
    print("Executing boa at: ")
    print(boapath)

exec(compile(open(boapath).read(), boapath, 'exec'))


##
#
