import os
import subprocess
import time

import bpy

from .pasteboard import _native as pasteboard


# Check if clipboard doesn't contain any file paths
def no_furls():
    script = [
        "osascript",
        "-e",
        '((clipboard info) as string does not contain "«class furl»") as string',
    ]
    popen = subprocess.Popen(script, stdout=subprocess.PIPE)
    return popen.communicate()[0].decode("utf-8").strip() == "true"


# Save image data directly from clipboard
def save_clipboard(fullpath):
    commands = [
        f'set pastedImage to (open for access POSIX file "{fullpath}" with write permission)',
        "try",
        "    write (the clipboard as «class PNGf») to pastedImage",
        "end try",
        "close access pastedImage",
    ]
    script = ["osascript"]
    for command in commands:
        script += ["-e", command]
    subprocess.Popen(script).wait()


def GrabImage():

    timestamp = time.strftime("%y%m%d-%H%M%S")
    img_name = f"PastedImage{timestamp}.png"

    bpy_addon_prefs = bpy.context.preferences.addons[
        __package__.split(".")[0]
    ].preferences

    if bpy.data.filepath and bpy_addon_prefs.force_default_dir is False:
        Directory = os.path.join(os.path.split(bpy.data.filepath)[0], "ImagePaste")

        if os.path.isdir(Directory) is False:
            os.mkdir(Directory)

    else:
        Directory = bpy_addon_prefs.default_img_dir

    img_dir = os.path.join(Directory, img_name)

    pb = pasteboard.Pasteboard()
    urls = pb.get_file_urls()
    contents = pb.get_contents()

    if urls is not None:
        urls = list(urls)
        img_dir = urls
        img_name = [os.path.basename(current) for current in img_dir]
        return img_dir, img_name
    elif contents == "":
        return 0
    else:
        if no_furls():
            save_clipboard(img_dir)
            return [img_dir], [img_name]

    return 1


# Function to copy image from given path to clipboard
def CopyImage(img_path):
    script = [
        "osascript",
        "-e",
        f'set the clipboard to (read file POSIX file "{img_path}" as «class PNGf»)',
    ]
    subprocess.Popen(script).wait()
