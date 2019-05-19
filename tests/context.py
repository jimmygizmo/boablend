import os
import sys


####################################################################################################
# Tests need to import the boablend module and a good way to enable that is to prepend the correct
# path to Python's list of module import search paths. We need this to be an absolute path. This
# context file, being located in the /tests/ subdirectory accomplishes this for all test code
# contained herein. Each test file must perform the following import to leverage this context file.
# In each test file within /tests/ include this import:
# from .context import boablend

# Modifying the seach path all in one line looks like this:
#sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
#
# That one-line format is not a good way to learn anything, so let's break it down.
# Set verbose to 'True' to see the values at each step. 
# When you are done learning how this context.py file works, leave verbose = False.

verbose = True

# __file__ is the relative path to the current file.
current_filename = __file__
if verbose:
    print("__file__: {}".format(current_filename))

# And the directory name in this case just '.' which of course means the current directory
os_path_dirname = os.path.dirname(current_filename)
if verbose:
    print("os_path_dirname: {}".format(os_path_dirname))

# Using os.path.join() is the best practice way of assembling paths because it will always use the
# correct path separator for the current platform. i.e. '/' vs. '\' etc. And thus we keep things
# compatible with all platforms.
joined_with_parent_dir = os.path.join(os_path_dirname, '..')
if verbose:
    print("joined_with_parent_dir: {}".format(joined_with_parent_dir))

# It seems like a roundabout way to get there but in this case we determine the path we need is in
# fact just '..' which of course is the parent directory.

# If you are looking at the output from the verbose mode, you may see joined_with_parent_dir
# as './..'. At least in the default configuration with /tests/ within the project/repo root,
# on MacOS you may. Of course '.' equates to /path/to/project_repo_root/tests which is
# /path/to/boablend/tests. Hence this equates to /path/to/project_repo_root or 
# /path/to/boablend. And this is where the 'boablend' module directory is located which is what
# needs to be imported. Remember, we need to add the path to the dir to SEARCH for 'boablend'.

# We need this as an absolute path, hence:
absolute_path = os.path.abspath(joined_with_parent_dir)
if verbose:
    print("absolute_path: {}".format(absolute_path))

# This might seem excessive, but to do this in a reliable, cross-platform way which works for a
# tests directory located anywhere in the project, all of these steps are necessary.

# Prepend the calculated absolute path to Python's list of module import search paths.
# Prepending it means the boablend module will be located immediately, without unnecessarily
# searching the entire list of paths.
sys.path.insert(0, absolute_path)


# TODO: Add an explanation of how the 'import from .context boablen' works .. i.e. about
# Python relative imports.


# Hopefully this breakdown brings some clarity to how to portably and reliably enable the import
# of the module under test.


##
#
