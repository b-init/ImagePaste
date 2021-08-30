import bpy


class Report:
    """A class to hold information about a report."""

    REPORT_TABLE = {
        1: ["ERROR", "Process failed"],
        2: ["ERROR", "No image found on clipboard"],
        3: ["ERROR", "Unable to save image"],
        4: ["ERROR", "Unable to copy image"],
        5: ["INFO", "Copied image"],
        6: ["INFO", "Pasted image"],
        7: ["INFO", "Moved images"],
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

    def log(self, operator: bpy.types.Operator) -> None:
        """Log the report to the Blender UI and console.

        Args:
            operator (bpy.types.Operator): The operator calling the report. If the
                method is called from a Blender operator method, it is usually `self`.
        """
        operator.report({self.type}, self.message)
        Report.console_log(self.verbose)

    @staticmethod
    def console_log(message: str) -> None:
        """Log the message to the console.

        Args:
            message (str): The message to be printed to the console.
        """
        from .metadata import get_addon_preferences

        preferences = get_addon_preferences()
        if not preferences.is_disable_debug:
            print(f"ImagePaste: {message}")

    def __repr__(self) -> str:
        """Return the string representation of the report.

        Returns:
            str: The string representation of the report.
        """
        return f"({self.code}:{self.type})<{self.message}>"
