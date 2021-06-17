import os
import subprocess
import time

import bpy


POWERSHELL = [
    "powershell",
    "-NoProfile",
    "-NoLogo",
    "-NonInteractive",
    "-WindowStyle",
    "Hidden",
]


def request(command):
    popen = subprocess.Popen(
        [*POWERSHELL, "& {" + command + "}"],
        stdout=subprocess.PIPE,
        universal_newlines=True,
    )
    return popen.communicate()[0].strip()


def GrabImage():
    timestamp = time.strftime("%y%m%d-%H%M%S")
    img_name = "PastedImage" + timestamp + ".png"
    file_path = (
        bpy.context.preferences.addons["ImagePaste"].preferences.default_img_dir
        + img_name
    )

    image_command = (
        "$image = Get-Clipboard -Format Image\n"
        f'if ($image) {{ $image.Save("{file_path}") ; Write-Output "1"}}'
    )
    file_command = (
        "$files = Get-Clipboard -Format FileDropList\n"
        "if ($files) { "
        '($files | Where-Object { @(".png", ".jpg").Contains($_.Extension) }).fullName'
        "}"
    )
    if not request(image_command):
        file_path = request(file_command)

    if file_path == "":
        return 0
    file_path = file_path.split("\n")
    return file_path, [os.path.basename(path) for path in file_path]


def CopyImage(img_path):
    command = (
        "Add-Type -Assembly System.Windows.Forms\n"
        "Add-Type -Assembly System.Drawing\n"
        f'$image = [Drawing.Image]::FromFile("{img_path}")\n'
        "[Windows.Forms.Clipboard]::SetImage($image)"
    )
    request(command)
