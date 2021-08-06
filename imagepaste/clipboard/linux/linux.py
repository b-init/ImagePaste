from __future__ import annotations
from enum import Enum

from ...image import Image
from ...process import Process
from ...report import Report
from ..clipboard import Clipboard


class XclipTarget(Enum):
    """Enum for xclip target types."""

    ALL = "TARGETS"
    IMAGE = "image/png"
    URI = "text/uri-list"


class LinuxClipboard(Clipboard):
    """A Clipboard implementation for Linux."""

    def __init__(self, report: Report, images: list[Image] = None) -> None:
        """Initialize LinuxClipboard instance.

        Args:
            report (Report): a Report object to show status of operation results.
            images (list[Image], optional): a list of Image objects. Defaults to None.
        """
        super().__init__(report, images)

    @classmethod
    def push(cls, save_directory: str) -> LinuxClipboard:
        """Clipboard pushes images information.

        Args:
            save_directory (str): a directory to save images.

        Returns:
            LinuxClipboard: a LinuxClipboard instance, which contains a Report object
                showing the status of the operation and a list of Image objects that
                holds information of images were copied in the clipboard.
        """
        from os.path import join
        from urllib.parse import urlparse
        from urllib.request import url2pathname

        # Get all available targets
        process = Process.execute(cls.get_xclip_args())
        if process.stderr:
            return cls(Report(1, f"Process failed ({process.stderr})"))

        # If there is an image in clipboard, save the image and send its path
        if XclipTarget.IMAGE.value in process.stdout:
            filename = cls.get_filename()
            filepath = join(save_directory, filename)
            process = Process.execute(
                cls.get_xclip_args(XclipTarget.IMAGE.value), outpath=filepath
            )
            if process.stderr:
                image = Image(filepath)
                return cls(Report(3, f"Cannot save image: {image} ({process.stderr})"))
            image = Image(filepath, pasted=True)
            return cls(Report(6, f"Saved and pasted 1 image: {image}"), [image])

        # If copying from files, just send their paths
        if XclipTarget.URI.value in process.stdout:
            uris = Process.execute(cls.get_xclip_args(XclipTarget.URI.value)).stdout
            filepaths = [url2pathname((urlparse(uri).path)) for uri in uris]
            # TODO: Check if files are images
            images = [Image(filepath, pasted=True) for filepath in filepaths]
            return cls(Report(6, f"Pasted {len(images)} image files: {images}"), images)
        return cls(Report(2))

    @classmethod
    def pull(cls, image_path: str) -> LinuxClipboard:
        """Clipboard pulls image information.

        Args:
            image_path (str): a path to image to be copied to clipboard.

        Returns:
            LinuxClipboard: a LinuxClipboard instance, which contains a Report object
                showing the status of the operation and a list of one Image object that
                holds information of the image we put its path to the input.
        """
        from mimetypes import guess_type

        mime_type = guess_type(image_path)[0]
        if not mime_type:
            return Report(4, f"Cannot guess MIME type from {image_path}")
        args = LinuxClipboard.get_xclip_args(mime_type, image_path, out=False)
        # If capture stdout/stderr, popen will hang as xclip runs in the background
        process = Process.execute(args, capture_output=False)
        if process.returncode != 0:
            return cls(Report(4, f"Popen failed with code {process.returncode}"))
        image = Image(image_path)
        return cls(Report(5, f"Copied 1 image: {image}"), [image])

    @staticmethod
    def get_xclip_args(
        target: XclipTarget = XclipTarget.ALL.value, *suffix: str, out=True
    ) -> list[str]:
        """Get arguments for xclip command.

        Args:
            target (XclipTarget, optional): a XclipTarget enum value, which specifies
                what to capture. Defaults to XclipTarget.ALL.value.
            suffix (str, optional): a list of suffixes to be added to the command.
                Defaults to empty list.
            out (bool, optional): a flag to request xclip to output to stdout.
                Defaults to True.

        Returns:
            list[str]: a list of arguments for xclip command.
        """
        from os import chmod
        from os.path import dirname
        from os.path import realpath
        from stat import S_IXUSR

        XCLIP_PATH = f"{dirname(realpath(__file__))}/bin/xclip"
        # TODO: Move to higher level
        chmod(XCLIP_PATH, S_IXUSR)
        args = [
            XCLIP_PATH,
            "-rmlastnl",
            "-selection",
            "clipboard",
            "-target",
            f"{target}",
        ]
        if out:
            args += ["-out"]
        args += suffix
        return args
