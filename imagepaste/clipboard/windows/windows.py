from __future__ import annotations

from ..clipboard import Clipboard
from ...report import Report
from ...image import Image
from ...process import Process


class WindowsClipboard(Clipboard):
    """A concrete implementation of Clipboard for Windows."""

    def __init__(self, report: Report, images: list[Image] = None) -> None:
        """A concreate implementation of Clipboard for Windows.

        Args:
            report (Report): A Report instance to which results should be reported.
            images (list[Image], optional): A list of Images objects. Defaults to None.
        """
        super().__init__(report, images)

    @classmethod
    def push(cls, save_directory: str) -> WindowsClipboard:
        """A class method for pushing images from the Windows Clipboard.

        Args:
            save_directory (str): A path to a directory to save the pushed images.

        Returns:
            WindowsClipboard: A WindowsClipboard instance, which contains status of
                operations under Report object and a list of Image objects holding
                pushed images information.
        """
        from os.path import join

        filename = cls.get_filename()
        filepath = join(save_directory, filename)

        image_script = (
            "Add-Type -AssemblyName System.Windows.Forms; "
            "Add-Type -AssemblyName System.Drawing; "
            "$clipboard = [System.Windows.Forms.Clipboard]::GetDataObject(); "
            "$imageStream = $clipboard.GetData('PNG'); "
            "if ($null -eq $imageStream) { $imageStream = $clipboard.GetData('image/png') }; "
            "if ($null -eq $imageStream) { $imageStream = $clipboard.GetData('System.Drawing.Bitmap') }; "
            "if ($imageStream) {"
            "$bitmap = New-Object System.Drawing.Bitmap($imageStream); "
            f"$bitmap.Save('{filepath}', [System.Drawing.Imaging.ImageFormat]::Png); "
            "Write-Output 0"
            "}"
        )
        process = Process.execute(cls.get_powershell_args(image_script), split=False)
        if process.stderr:
            image = Image(filepath)
            return cls(Report(3, f"Cannot save image: {image} ({process.stderr})"))
        if process.stdout == "0":
            image = Image(filepath, pasted=True)
            return cls(Report(6, f"Saved and pasted 1 image: {image}"), [image])

        file_script = (
            "$files = Get-Clipboard -Format FileDropList; "
            "if ($files) { $files.fullname }"
        )
        process = Process.execute(cls.get_powershell_args(file_script))
        if process.stdout[0] != "":
            images = [Image(filepath) for filepath in process.stdout]
            return cls(Report(6, f"Pasted {len(images)} image files: {images}"), images)
        return cls(Report(2))

    @classmethod
    def pull(cls, image_path: str) -> WindowsClipboard:
        """A class method for pulling images to the Windows Clipboard.

        Args:
            image_path (str): A path to an image to be pulled to the clipboard.

        Returns:
            WindowsClipboard: A WindowsClipboard instance, which contains status of
                operations under Report object and a list of one Image object that holds
                information of the pulled image we put its path to the input.
        """
        # Script that supports transparency. Save images to clipboard as PNG and Bitmap.
        # Populating the clipboard with Bitmap data which is equivalent to using the
        # `Clipboard.SetImage` method.
        script = (
            "Add-Type -Assembly System.Windows.Forms; "
            "Add-Type -Assembly System.Drawing; "
            f"$image = [Drawing.Image]::FromFile('{image_path}'); "
            "$imageStream = New-Object System.IO.MemoryStream; "
            "$image.Save($imageStream, [System.Drawing.Imaging.ImageFormat]::Png); "
            "$dataObj = New-Object System.Windows.Forms.DataObject('Bitmap', $image); "
            "$dataObj.SetData('PNG', $imageStream); "
            "[System.Windows.Forms.Clipboard]::SetDataObject($dataObj, $true); "
        )

        process = Process.execute(cls.get_powershell_args(script))
        if process.stderr:
            return cls(Report(4, f"Cannot load image: {image_path} ({process.stderr})"))
        image = Image(image_path)
        return cls(Report(5, f"Copied 1 image: {image}"), [image])

    @staticmethod
    def get_powershell_args(script: str) -> list[str]:
        """A static method to get PowerShell arguments from a script for a process.

        Args:
            script (str): A script to be executed.

        Returns:
            list[str]: A list of PowerShell arguments for operating a process.
        """
        from os import getenv
        from os.path import join

        powershell_args = [
            join(
                getenv("SystemRoot"),
                "System32",
                "WindowsPowerShell",
                "v1.0",
                "powershell.exe",
            ),
            "-NoProfile",
            "-NoLogo",
            "-NonInteractive",
            "-WindowStyle",
            "Hidden",
        ]
        script = (
            "$OutputEncoding = "
            "[System.Console]::OutputEncoding = "
            "[System.Console]::InputEncoding = "
            "[System.Text.Encoding]::UTF8; "
            + "$PSDefaultParameterValues['*:Encoding'] = 'utf8'; "
            + script
        )
        args = powershell_args + ["& { " + script + " }"]
        return args
