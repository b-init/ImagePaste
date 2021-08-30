import bpy


ADDON_NAME = __package__.split(".")[0]


def get_addon_preferences() -> bpy.types.AddonPreferences:
    """Get the addon preferences.

    Returns:
        bpy.types.AddonPreferences: The addon preferences.
    """
    return bpy.context.preferences.addons[ADDON_NAME].preferences
