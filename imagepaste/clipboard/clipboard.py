from __future__ import annotations
from abc import ABC
from abc import abstractmethod
from abc import abstractclassmethod

from ..image import Image
from ..report import Report


class Clipboard(ABC):
    """An abstract class for clipboard operations."""

    @abstractmethod
    def __init__(self, report: Report, images: list[Image] = None) -> None:
        """Require subclasses to provide implementation for this method.

        Args:
            report (Report): Mandatory parameter, to be used to report status of result.
            images (list[Image], optional): List of returned images. Defaults to None.
        """
        self.report = report
        self.images = images

    @abstractclassmethod
    def push(cls, save_directory: str) -> Clipboard:
        """Push images information from the clipboard.

        Subclasses must implement this method to return a new instance of the class.
        'Push' keyword mean that the clipboard is giving (pushing) the images to us.

        Args:
            save_directory (str): a path of the directory where images should be saved.

        Returns:
            Clipboard: an instance of the class, which contains a Report object showing
                the status of the operation and a list of Image objects that holds
                information of images were copied in the clipboard.
        """
        pass

    @abstractclassmethod
    def pull(cls, image_path: str) -> Clipboard:
        """Pull images information to the clipboard.

        Subclasses must implement this method to return a new instance of the class.
        'Pull' keyword mean that the clipboard is getting (pulling) data from us.

        Args:
            image_path (str): a path of an image to be copied to the clipboard.

        Returns:
            Clipboard: an instance of the class, which contains a Report object showing
                the status of the operation and a list of one Image object that hold
                information of the image we put its path to the input.
        """
        pass

    @staticmethod
    def get_filename() -> str:
        """Get a string representation of the current time in the filename format.

        Returns:
            str: a string representing the current time in the filename format.
        """
        from time import strftime
        from ..metadata import get_addon_preferences
        from ..tree import populate_filename
        from ..tree import is_valid_filename

        preferences = get_addon_preferences()
        filename = (
            populate_filename(preferences.image_filename_pattern)
            + preferences.image_extension
        )
        if is_valid_filename(filename):
            return filename
        return strftime(f"ImagePaste-%y%m%d-%H%M%S{preferences.image_extension}")

    def __repr__(self) -> str:
        """Representation of the object.

        Returns:
            str: a string showing a brief information about the report and images.
        """
        return "{}({!r})".format(self.__class__.__name__, self.__dict__)
