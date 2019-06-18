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

/Applications/Blender/blender.app/Contents/MacOS/blender \
--background \
--factory-startup \
--python "$PROJECT_DIR/vipers/background_job_vp.py" -- \
--text="Background Job Test" \
--render="$TEMP_DIR/bg_job_test" \
--save="$TEMP_DIR/bg_job_test.blend"


##
#
