
####################################################################################################

# For converting XYZ Degrees values to Euler Values for Rotation
# TODO: Only used this PI for the below. Should use math.pi anyhow.
#PI = 3.14159265


# TODO: Now using math.radians(angle_in_degrees) instead of
# angle_in_degrees * DEG_TO_EUL_FACTOR -- It is the same thing and more clear
# and better to use a standard lib. TODO: We can probably deprecate/remove this everywhere.
#DEG_TO_EUL_FACTOR = (PI/180.0)  # 0.0174532925

# For converting Euler Values for Rotation to XYZ Degrees values
# TODO: Now using math.degrees(angle_in_radians) instead of
# angle_in_radians * EUL_TO_DEG_FACTOR -- It is the same thing and more clear
# and better to use a standard lib. TODO: We can probably deprecate/remove this everywhere.
#EUL_TO_DEG_FACTOR = (180.0/PI) # 57.29577957855229

ALPHA_FULL_OPAQUE = 1


##
#
