from os.path import basename
from os.path import dirname


class Image:
    """A class to represent an image file."""

    def __init__(self, filepath: str, filename: str = None) -> None:
        """Constructor for the Image class.

        Args:
            filepath (str): The path to the image file.
            filename (str, optional): The name of the image file.
        """
        self.filepath = filepath
        self.filename = filename or basename(filepath)
        self.filebase = dirname(filepath)

    def __repr__(self) -> str:
        """Return a string representation of the Image class.

        Returns:
            str: A string representation of the Image class.
        """
        return f"{self.filename}<{self.filepath}>"
