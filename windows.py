import bpy
import os

from io import BytesIO
from .PIL import ImageGrab, Image
import time

try:
    from .win32_py37 import win32clipboard
except Exception:
    from .win32_py39 import win32clipboard


# Function to grab image(s) from clipboard, save them and return their names and paths
def GrabImage():

    img = ImageGrab.grabclipboard()

    if img is None:
        return 0

    if type(img) == list:
        img_dir = img
        img_name = [os.path.basename(current) for current in img_dir]
        return img_dir, img_name

    # Generate the name of the image with timestamp to prevent overwriting
    timestamp = time.strftime("%y%m%d-%H%M%S")
    img_name = "PastedImage" + timestamp + ".png"

    if (
        bpy.data.filepath
        and not bpy.context.preferences.addons[
            __package__
        ].preferences.force_default_dir
    ):
        # If saved and force_default_directory is set to false
        # save image in the place where the .blend file is saved
        # in a newly created subfolder
        Directory = os.path.join(os.path.split(bpy.data.filepath)[0], "ImagePaste")

        if not os.path.isdir(Directory):
            os.mkdir(Directory)

    else:
        # Just use the default location otherwise
        Directory = bpy.context.preferences.addons[
            __package__
        ].preferences.default_img_dir

    img_dir = Directory + "\\" + img_name

    try:
        img.save(img_dir)
    except Exception:
        return 1

    return [img_dir], [img_name]


# Function to copy image from given path to clipboard
def CopyImage(img_path):
    image = Image.open(img_path)

    img_out = BytesIO()
    image.convert("RGB").save(img_out, "BMP")
    data = img_out.getvalue()[14:]
    img_out.close()

    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
    win32clipboard.CloseClipboard()
