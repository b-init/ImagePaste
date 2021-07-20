class Report:
    """A class to hold information about a report."""

    REPORT_TABLE = {
        1: ["ERROR", "Process failed"],
        2: ["ERROR", "No image found on clipboard"],
        3: ["ERROR", "Unable to save image"],
        4: ["ERROR", "Unable to copy image"],
        5: ["INFO", "Copied image"],
        6: ["INFO", "Pasted image"],
    }

    def __init__(self, code: int, verbose: str = None) -> None:
        """Initialize the Report object.

        Args:
            code (int): The code of the report.
            verbose (str, optional): The verbose message for the debugging. Defaults to
                None.
        """
        self.code = code
        self.type = Report.REPORT_TABLE[self.code][0]
        self.message = Report.REPORT_TABLE[self.code][1]
        self.verbose = verbose or self.message

    def log(self) -> None:
        """Log the report to the console."""
        print(f"ImagePaste: {self.verbose}")

    def __repr__(self) -> str:
        """Return the string representation of the report

        Returns:
            str: The string representation of the report
        """
        return f"({self.code}:{self.type})<{self.message}>"
