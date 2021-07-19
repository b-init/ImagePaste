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

    if bpy.data.filepath and bpy.context.preferences.addons[
            __package__.split(".")[0]
        ].preferences.force_default_dir == False: 
        # save image in the place where the blendfile is saved, in a newly created 
        # subfolder (if saved and force_default_directory is set to false)
        file_path = os.path.join(os.path.split(bpy.data.filepath)[0], 'ImagePaste')
        
        if not os.path.isdir(file_path):
            os.mkdir(file_path)

    else:  
        # just use the default location otherwise
        file_path = (
        bpy.context.preferences.addons[
            __package__.split(".")[0]
        ].preferences.default_img_dir
        )

    file_path = os.path.join(file_path, img_name)

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
