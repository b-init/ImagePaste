class Image:
    """A class to represent an image file."""

    pasted_images = {}

    def __init__(
        self, filepath: str, filename: str = None, is_pasted: bool = False
    ) -> None:
        """Constructor for the Image class.

        Args:
            filepath (str): The path to the image file.
            filename (str, optional): The name of the image file.
            is_pasted (bool, optional): Whether the image is pasted.
        """
        from os.path import basename
        from os.path import dirname

        self.filepath = filepath
        self.filename = filename or basename(filepath)
        self.filebase = dirname(filepath)
        if is_pasted:
            Image.pasted_images[self.filepath] = self

    def __repr__(self) -> str:
        """Return a string representation of the Image class.

        Returns:
            str: A string representation of the Image class.
        """
        return f"{self.filename}<{self.filepath}>"
