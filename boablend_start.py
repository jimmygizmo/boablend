# No shebang. This file is currently only supported for direct execution from withing the Python
# environment of a currently-running Blender instance and open blend file with a Text object
# containing the boablend hook code. You cannot currently run this from a standard Python env.
####################################################################################################
####################################### BOABLEND ENTRY POINT #######################################

####################################################################################################
import bpy  # This import works when executing within Blender but will show an import error in IDEs.
# Regarding import errors showing in your IDE for 'import bpy':
# /docs/import_bpy_error_in_ide.txt
####################################################################################################

import os

verbose = True

boadir = 'boas'

# What is a 'boa'?
# A 'blender omnipotent automator' of course!
# BOA = Blender Omnipotent Automator

# Frankly, it is most likely true that 'boas' can't automate Blender in EVERY possible way, but the
# goal of the 'boablend' project is to potentially enable ANY kind of Blender automation or
# development with maximum flexibility and following both python and Blender best-practices.
# .. and I needed words that started with b, o and a .. hence 'omnipotent' .. i.e. more accurately;
# 'very flexible, powerful and relatively simple to use, with cool bundled functionality.' .. mkay?
# 'Automator' is a nice, flexible concept too. Automation is the genesis and most-likely the most
# common useful application of boablend, but the project goal is to enable and empower development
# with and of Blender in multiple contexts, including gaming and more .. so 'automator' is meant in
# a very general and poetic sense here.
# It is going to be fun to call boablend projects, modules, sub-modules, mini-applications, add-ons
# simulations, plug-ins or whatever (get the idea?) .. 'boas'.
# This is all Python, right? Well names derived from 'python/py' were sort of all taken up .. so
# here we are playing with boas .. and Blender .. and boablend!

default_boa = 'rgb_cube_tower.py'

if verbose:
    print()
    print("~ ~ ~ ~ ~ Boablend dispatching boa: {}".format(default_boa))

boa_sub_path = os.path.join(boadir, default_boa)

boapath = bpy.path.abspath("//{}".format(boa_sub_path))

if verbose:
    print("Executing boa at: ")
    print(boapath)

exec(compile(open(boapath).read(), boapath, 'exec'))


##
#
