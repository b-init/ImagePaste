class Image:
    """A class to represent an image file."""

    pasted_images = {}
    image_index = 0

    def __init__(self, filepath: str, pasted: bool = False) -> None:
        """Constructor for the Image class.

        Args:
            filepath (str): The path to the image file.
            filename (str, optional): The name of the image file.
            pasted (bool, optional): Whether the image is pasted.
        """
        self.filepath = filepath
        if pasted:
            Image.pasted_images[self.filepath] = self
            Image.image_index += 1

    @property
    def filepath(self) -> str:
        """Get the path to the image file."""
        return self._filepath

    @filepath.setter
    def filepath(self, filepath: str) -> None:
        """Set the path to the image file.

        Args:
            filepath (str): The path to the image file.
        """
        from os.path import basename
        from os.path import dirname

        self._filepath = filepath
        self.filename = basename(filepath)
        self.filebase = dirname(filepath)

    def __repr__(self) -> str:
        """Return a string representation of the Image class.

        Returns:
            str: A string representation of the Image class.
        """
        return f"{self.filename}<{self.filepath}>"
