import os
import subprocess
from enum import Enum

import bpy


class ClipBoardTarget(Enum):
    ALL = "TARGETS"
    IMAGE = "image/png"
    URI = "text/uri-list"


def xclip_out(target: ClipBoardTarget = ClipBoardTarget.ALL.value, path=None):
    script_file = os.path.realpath(__file__)
    directory = os.path.dirname(script_file)
    args = (
        f"{directory}/bin/xclip",
        "-selection",
        "clipboard",
        "-target",
        f"{target}",
        "-out",
    )
    if not path:
        popen = subprocess.Popen(args, stdout=subprocess.PIPE)
        result = popen.communicate()[0].decode("utf-8").strip()
        if "\r\n" in result:
            return result.split("\r\n")
        return result.split("\n")
    with open(path, "w") as file:
        popen = subprocess.Popen(args, stdout=file).wait()


def GrabImage():
    if ClipBoardTarget.IMAGE.value in xclip_out(target=ClipBoardTarget.ALL.value):
        file_name = "ImagePaste.png"
        file_path = (
            bpy.context.preferences.addons[__package__].preferences.default_img_dir
            + file_name
        )
        xclip_out(target=ClipBoardTarget.IMAGE.value, path=file_path)
        return [file_path], [file_name]
    if ClipBoardTarget.URI.value in xclip_out(target=ClipBoardTarget.ALL.value):
        uris = xclip_out(target=ClipBoardTarget.URI.value)
        import urllib
        import urllib.request

        paths = [
            urllib.request.url2pathname((urllib.parse.urlparse(uri).path))
            for uri in uris
        ]
        return paths, [os.path.basename(path) for path in paths]


# Function to copy image from given path to clipboard
def CopyImage(img_path):
    script_file = os.path.realpath(__file__)
    directory = os.path.dirname(script_file)
    args = (
        f"{directory}/bin/xclip",
        "-selection",
        "clipboard",
        "-target",
        "image/png",
        "-in",
        f"{img_path}",
    )
    subprocess.Popen(args).wait()
