import bpy


ADDON_NAME = __package__.split(".")[0]


def get_addon_preferences() -> bpy.types.AddonPreferences:
    """Get the addon preferences.

    Returns:
        bpy.types.AddonPreferences: The addon preferences.
    """
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

    if not bpy.data.filepath:
        if preferences.is_use_another_directory and preferences.another_directory:
            return preferences.another_directory
        return bpy.app.tempdir

    if (
        preferences.is_use_another_directory
        and preferences.is_force_use_another_directory
        and preferences.another_directory
    ):
        return preferences.another_directory

    directory_path = dirname(bpy.data.filepath)
    if not preferences.is_use_subdirectory or not preferences.subdirectory_name:
        return directory_path
    subdirectory_path = join(directory_path, preferences.subdirectory_name)
    if not exists(subdirectory_path):
        makedirs(subdirectory_path)
    return subdirectory_path
