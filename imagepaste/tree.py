import bpy


def get_save_directory() -> str:
    """Get the path to the directory where the images are saved.

    Returns:
        str: The path to the directory where the images are saved.
    """
    from os import makedirs
    from os.path import exists
    from os.path import dirname
    from os.path import join
    from .metadata import get_addon_preferences

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


def is_valid_filename(filename: str) -> bool:
    """Check if the filename is valid.

    Args:
        filename (str): a string representing the filename.

    Returns:
        bool: True if the filename is valid, False otherwise.
    """

    def is_general_valid_filename(filename: str) -> bool:
        """Check if the filename is valid.

        Args:
            filename (str): a string representing the filename.

        Returns:
            bool: True if the filename is valid, False otherwise.
        """
        if not filename:
            return False
        if len(filename) > 255:
            return False
        if filename in (".", ".."):
            return False
        return True

    def is_windows_valid_filename(filename: str) -> bool:
        """Check if the filename is valid on Windows.

        Args:
            filename (str): a string representing a filename.

        Returns:
            bool: True if the filename is valid on Windows, False otherwise.
        """
        # Check if the filename does not end with a dot or a space
        if filename[-1] in (".", " "):
            return False
        # Check if the filename is a reserved name
        windows_reserved_filenames = (
            "CON",
            "PRN",
            "AUX",
            "NUL",
            "COM1",
            "COM2",
            "COM3",
            "COM4",
            "COM5",
            "COM6",
            "COM7",
            "COM8",
            "COM9",
            "LPT1",
            "LPT2",
            "LPT3",
            "LPT4",
            "LPT5",
            "LPT6",
            "LPT7",
            "LPT8",
            "LPT9",
        )
        if filename.upper() in windows_reserved_filenames:
            return False
        # Check if the filename contains any invalid characters
        windows_invalid_characters = ("/", "\\", ":", "*", "?", '"', "<", ">", "|")
        for character in windows_invalid_characters:
            if character in filename:
                return False
        # Check if the filename contains any unprintable characters
        for index in range(31):
            if chr(index) in filename:
                return False
        return True

    def is_linux_valid_filename(filename: str) -> bool:
        """Check if the filename is valid on Linux.

        Args:
            filename (str): a string representing a filename.

        Returns:
            bool: True if the filename is valid on Linux, False otherwise.
        """
        # The "\" character is valid in Linux but Blender does not support it
        invalid_characters = ["/", "\\"]
        for invalid_character in invalid_characters:
            if invalid_character in filename:
                return False
        return True

    def is_darwin_valid_filename(filename: str) -> bool:
        """Check if the filename is valid on macOS.

        Args:
            filename (str): a string representing a filename.

        Returns:
            bool: True if the filename is valid on macOS, False otherwise.
        """
        return is_linux_valid_filename(filename)

    import sys

    if not is_general_valid_filename(filename):
        return False
    if sys.platform == "win32":
        return is_windows_valid_filename(filename)
    elif sys.platform == "linux":
        return is_linux_valid_filename(filename)
    elif sys.platform == "darwin":
        return is_darwin_valid_filename(filename)
    return False


def populate_filename(filename_pattern: str) -> str:
    """Populate a filename with a pattern.

    Args:
        pattern (str): a string representing a pattern.

    Returns:
        str: a string representing a filename.
    """
    from re import sub
    from time import strftime
    from .image import Image
    from .metadata import ADDON_NAME

    image_index = str(Image.image_index + 1)
    # Replace normal variables
    VARIABLES_TABLE = [
        ("${addonName}", ADDON_NAME),
        ("${yearLong}", strftime("%Y")),
        ("${yearShort}", strftime("%y")),
        ("${monthNumber}", strftime("%m")),
        ("${monthNameLong}", strftime("%B")),
        ("${monthNameShort}", strftime("%b")),
        ("${day}", strftime("%d")),
        ("${weekdayNumber}", strftime("%w")),
        ("${weekdayNameLong}", strftime("%A")),
        ("${weekdayNameShort}", strftime("%a")),
        ("${hour24}", strftime("%H")),
        ("${hour12}", strftime("%I")),
        ("${minute}", strftime("%M")),
        ("${second}", strftime("%S")),
        ("${index}", image_index),
    ]
    for pattern_key, pattern_value in VARIABLES_TABLE:
        filename_pattern = filename_pattern.replace(pattern_key, pattern_value)
    # Replace dynamic variables ${index:N}
    # Produce an N-digits-with-zeros-padded number
    filename_pattern = sub(
        r"\${index\:(\d+)}",
        lambda match: image_index.zfill(int(match.group(1))),
        filename_pattern,
    )
    return filename_pattern


def remove_empty_subdirectory(subdirectory_name: str = None) -> None:
    """Remove empty subdirectories.

    Args:
        subdirectory_name (str, optional): a string representing a subdirectory name.
            Defaults to None.
    """
    from os import listdir
    from os import rmdir
    from os.path import (
        dirname,
        join,
        isdir,
    )
    from .report import Report
    from .metadata import get_addon_preferences

    if not subdirectory_name:
        preferences = get_addon_preferences()
        if not preferences.subdirectory_name:
            return
        subdirectory_name = preferences.subdirectory_name
    directory_path = dirname(bpy.data.filepath)
    subdirectory_path = join(directory_path, subdirectory_name)
    if not isdir(subdirectory_path):
        return
    if listdir(subdirectory_path):
        return
    rmdir(subdirectory_path)
    Report.console_log(f"Empty subdirectory '{subdirectory_path}' was removed")
