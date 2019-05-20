
####################################################################################################
####################################### BOABLEND ENTRY POINT #######################################

# This is the new DISPATCHING implementation of the boablend entry point.
# Just introduced the concept of 'boas'.

# This 'import bpy' will show as broken in the IDE if bpy is not installed in the external
# environment, however since this script is invoked via exec() from within the Blender internal
# Python environment, it will be imported successfully there.
#import bpy

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
