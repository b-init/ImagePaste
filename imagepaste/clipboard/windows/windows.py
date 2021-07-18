from __future__ import annotations

from os.path import join

from ..clipboard import Clipboard
from ...report import Report
from ...image import Image
from ...process import Process


class WindowsClipboard(Clipboard):
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
        filename = cls.get_timestamp_filename()
        filepath = join(save_directory, filename)
        image = Image(filepath, filename)

        image_script = (
            "$image = Get-Clipboard -Format Image\n"
            f'if ($image) {{ $image.Save("{filepath}"); Write-Output 0 }}'
        )
        process = Process.execute(cls.get_powershell_args(image_script), split=False)
        if process.stderr:
            return cls(Report(3, f"Cannot save image: {image} ({process.stderr})"))
        if process.stdout == "0":
            return cls(Report(6, f"Saved and pasted 1 image: {image}"), [image])

        file_script = (
            "$files = Get-Clipboard -Format FileDropList\n"
            "if ($files) { $files.fullname }"
        )
        process = Process.execute(cls.get_powershell_args(file_script))
        if process.stdout != "":
            images = [Image(filepath) for filepath in process.stdout]
            return cls(Report(6, f"Pasted {len(images)} image files: {images}"), images)
        return cls(Report(2))

    @classmethod
    def pull(cls, image_path: str) -> WindowsClipboard:
        """A class method for pulling images to the Windows Clipboard.

        Args:
            image_path (str): A path to an image to be pulled to the Windows Clipboard.

        Returns:
            WindowsClipboard: A WindowsClipboard instance, which contains status of
                operations under Report object and a list of one Image object that holds
                information of the pulled image we put its path to the input.
        """
        script = (
            "Add-Type -Assembly System.Windows.Forms\n"
            "Add-Type -Assembly System.Drawing\n"
            f'$image = [Drawing.Image]::FromFile("{image_path}")\n'
            "[Windows.Forms.Clipboard]::SetImage($image)"
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
        POWERSHELL = [
            "powershell",
            "-NoProfile",
            "-NoLogo",
            "-NonInteractive",
            "-WindowStyle",
            "Hidden",
        ]
        args = POWERSHELL + ["& { " + script + " }"]
        return args
