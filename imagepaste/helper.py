import bpy


ADDON_NAME = __package__.split(".")[0]


def get_addon_preferences() -> bpy.types.AddonPreferences:
    """Get the addon preferences.

    Returns:
        bpy.types.AddonPreferences: The addon preferences.
    """
    import bpy

    return bpy.context.preferences.addons[ADDON_NAME].preferences


def get_save_directory() -> str:
    """Get the path to the directory where the images are saved.

    Returns:
        str: The path to the directory where the images are saved.
    """
    from os import makedirs
    from os.path import exists
    from os.path import dirname
    from os.path import join

    preferences = get_addon_preferences()

    if bpy.data.filepath and not preferences.is_force_use_another_directory:
        directory_path = dirname(bpy.data.filepath)
        if preferences.is_use_subdirectory and preferences.subdirectory_name:
            subdirectory_path = join(directory_path, preferences.subdirectory_name)
            if not exists(subdirectory_path):
                makedirs(subdirectory_path)
            return subdirectory_path
        return directory_path
    if preferences.is_use_another_directory and preferences.another_directory:
        return preferences.another_directory
    return bpy.app.tempdir