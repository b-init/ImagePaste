from __future__ import annotations

from ..clipboard import Clipboard
from ...image import Image
from ...report import Report
from ...process import Process


class DarwinClipboard(Clipboard):
    """A Clipboard implementation for macOS."""

    def __init__(self, report: Report, images: list[Image] = None) -> None:
        """Initialize the Darwin Clipboard.

        Args:
            report (Report): A Report object to hold operation results.
            images (list[Image], optional): A list of Image objects. Default: None.
        """
        super().__init__(report, images)

    @classmethod
    def push(cls, save_directory: str) -> DarwinClipboard:
        """Push the current image information from the clipboard.

        Args:
            save_directory (str): A path to a directory to save the image.

        Returns:
            DarwinClipboard: A new instance of the DarwinClipboard, with a Report
                object containing the operation results and a list of Image objects
                holding the images information.
        """
        from os.path import join
        from os.path import isfile
        from .pasteboard._native import Pasteboard

        # Use Pasteboard to get file URLs from the clipboard
        pasteboard = Pasteboard()
        urls = pasteboard.get_file_urls()
        if urls is not None:
            filepaths = list(urls)
            images = [Image(filepath) for filepath in filepaths]
            return cls(Report(6, f"Pasted {len(images)} image files: {images}"), images)

        # If no images are found, return a report with no images
        contents = pasteboard.get_contents()
        if contents == "":
            return cls(Report(2))

        # Check if clipboard doesn't contain any filepaths
        # (e.g. if the clipboard contains just a single image)
        if urls is None:
            filename = cls.get_timestamp_filename()
            filepath = join(save_directory, filename)
            image = Image(filepath, filename)
            commands = [
                "set pastedImage to "
                f'(open for access POSIX file "{filepath}" with write permission)',
                "try",
                "    write (the clipboard as «class PNGf») to pastedImage",
                "end try",
                "close access pastedImage",
            ]
            process = Process.execute(cls.get_osascript_args(commands))

            if not isfile(filepath):
                return cls(Report(3, f"Cannot save image: {image} ({process.stderr})"))
            return cls(Report(6, f"Saved and pasted 1 image: {image}"), [image])
        return cls(Report(3))

    @classmethod
    def pull(cls, image_path: str) -> DarwinClipboard:
        """Pull the image to the clipboard from its path.

        Args:
            image_path (str): A path to an image to be pulled to the clipboard.

        Returns:
            DarwinClipboard: A new instance of the DarwinClipboard, with a Report
                object containing the operation results and a list of one Image object
                holding information of the pulled image we put its path to the input.
        """
        commands = [
            "set the clipboard to "
            f'(read file POSIX file "{image_path}" as «class PNGf»)'
        ]
        process = Process.execute(cls.get_osascript_args(commands))
        if process.stderr:
            return cls(Report(4, f"Process failed ({process.stderr})"))
        image = Image(image_path)
        return cls(Report(5, f"Copied 1 image: {image}"), [image])

    @staticmethod
    def get_osascript_args(commands: list[str]) -> list[str]:
        """Get the arguments for osascript command.

        Args:
            commands (list[str]): A list of commands to be executed.

        Returns:
            list[str]: A list of arguments for osascript command ready to be executed.
        """
        args = ["osascript"]
        for command in commands:
            args += ["-e", command]
        return args
