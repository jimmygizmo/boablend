#! /usr/bin/env bash
####################################################################################################
# This virtual environment setup is not needed if you will always be using Blender's built-in
# Python distribution. However, this venv setup can enhance the operation of IDEs such as VSCode
# and others even if this venv is only used by the IDE and you only run your code with Blender's
# Python environment.

# IMPORTANT: YOUR PYTHON 3 INTERPRETER IS EXPECTED TO BE 'python3'
# This is the usual case when Homebrew was used for installation. Homebrew is by far the best way
# to install and maintain Python on MacOS, including using Python 2 and Python 3 side by side on
# the same host.

# Create the python virtual environment.
python3 -m venv .venv

# Activate the new python virtual environment.
source .venv/bin/activate

# Upgrade the virtual environments setuptools and pip.
# New virtual environments created with the 'venv' module always seem to come with a setuptools and
# a pip that are many versions back. In most cases it is a good idea to upgrade these tools to the
# latest versions.
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade setuptools

# Install packages to support and enhance IDE operation, particularly VSCode.
python3 -m pip install pylint  # Static code analysis for Python
python3 -m pip install autopep8  # Automatic PEP8 code reformatting
python3 -m pip install rope  # Python code refactoring library


####################################################################################################
############################## CURRENTLY DEBUGGING BPY BUILD/INSTALL ###############################
#### In order to support the IDE for the 'import bpy' statement or for future project phases which
#### might need bpy external to Blender itself for execution, we attempted to install bpy, but this
#### currently failing:
####################################################################################################
#### Blender-specific setup - The bpy python module
#### Bpy must be compiled during the pip install and this adds some extra requirements
#### Cmake
###python3 -m pip install cmake
#### Future-fstrings
###python3 -m pip install future-fstrings
#### Bpy, forcing a compile install with the --no-binary option
#### CMAKE CURRENT BUILD FAILURE WITH:
#### CMake Error at build_files/cmake/platform/platform_apple.cmake:38 (message):
####       Mac OSX requires pre-compiled libs at:
####       '/Users/bilbo/.blenderpy/blender/../lib/darwin'
####################################################################################################


# Install project-specific python depdendencies
python3 -m pip install -r requirements.txt


####################################################################################################
#
# Before you first run the app in any shell you will always need to activate the python virtual
# environment unless you plan to install all requirements globally or unless your IDE provides some
# other library loading/access mechanism etc. Most IDEs, when running this program for you, usually
# in a new, visible terminal window, will do the same thing as this command.
#### source .venv/bin/activate
#
# For development in an IDE, you will may need to configure the IDE to recognize and automatically
# activate the new python virtual environment, however many popular IDEs can automatically see and
# activate this environment in the .venv directory in which we create it, at the base of the
# project dir.
#
####################################################################################################


# Modules installed to support pylint (versions may differ slightly):
# astroid==2.2.5
# isort==4.3.20
# lazy-object-proxy==1.4.1
# mccabe==0.6.1
# pylint==2.3.1
# six==1.12.0
# typed-ast==1.4.0
# wrapt==1.11.1

# Modules installed to support autopep8 (versions may differ slightly):
# autopep8==1.4.4
# pycodestyle==2.5.0

# Modules installed to support rope
# rope==0.14.0


