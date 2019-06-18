#! /usr/bin/env bash
####################################################################################################

VIPER="background_job"
DESC="This is the background_job template example from within Blender 2.8. Located under the \
(Scripting/Text) Templates menu."

# Obtain absulte path to the current script, the vipers dir:
SCRIPT_DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

# The project directory or repository root which contains the vipers dir:
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

TEMP_DIR="$PROJECT_DIR/tmp"

####################################################################################################

echo
echo "EXECUTING VIPER: $VIPER"
echo $DESC
echo "Script 'vipers' directory: $SCRIPT_DIR"
echo "Project/repository root directory: $PROJECT_DIR"
echo "Temp/working directory: $TEMP_DIR"
echo "Making sure the temp dir exists."

mkdir -p $TEMP_DIR

####################################################################################################

# This viper is intended to use the --background Blender option but when used the rendered image
# is just solid black. If the --background option is removed, thus allowing the GUI to open, the
# the code still runs the same, but the image is rendered and output correctly. This could be a bug
# in Blender or a problem in the Belder template code from which this viper is derived.
# Unfortunately, using --background was one of the main points of this viper.
# So, here, --background has been removed.
/Applications/Blender/blender.app/Contents/MacOS/blender \
--factory-startup \
--python "$PROJECT_DIR/vipers/background_job_vp.py" -- \
--text="Boablend" \
--render="$TEMP_DIR/bg_job_test" \
--save="$TEMP_DIR/bg_job_test.blend"


# /Applications/Blender/blender.app/Contents/MacOS/blender \
# --background \
# --factory-startup \
# --python "$PROJECT_DIR/vipers/background_job_vp.py" -- \
# --text="Boablend" \
# --render="$TEMP_DIR/bg_job_test" \
# --save="$TEMP_DIR/bg_job_test.blend"


##
#
