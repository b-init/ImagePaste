import bpy


ADDON_NAME = __package__.split(".")[0]


def get_addon_preferences() -> bpy.types.AddonPreferences:
    """Get the addon preferences.

    Returns:
        bpy.types.AddonPreferences: The addon preferences.
    """
    return bpy.context.preferences.addons[ADDON_NAME].preferences


def get_addon_bl_info() -> dict:
    """Get add-on bl_info defined in __init__.py.

    Returns:
        dict: a dictionary containing add-on info.
    """
    from importlib import import_module

    return import_module(ADDON_NAME).bl_info
