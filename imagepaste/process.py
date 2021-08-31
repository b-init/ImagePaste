from __future__ import annotations


class Process:
    """A helper class for executing a command line process."""

    def __init__(self) -> None:
        """Initialize a Process instance."""
        self.parameters = {
            "encoding": "utf-8",
            "text": True,
        }
        self.stdout = None
        self.stderr = None
        self.returncode = None

    @classmethod
    def execute(
        cls,
        args: list[str],
        shell: bool = False,
        capture_output: bool = True,
        split: bool = True,
        outpath: str = None,
    ) -> Process:
        """Execute a command line process.

        Args:
            args (list[str]): The command line arguments to execute.
            shell (bool, optional): If True, execute the command line using the shell.
                Defaults to False.
            capture_output (bool, optional): If True, capture the output of the command
                line. Defaults to True.
            outpath (str, optional): The path to write the output to. If not provided,
                the output will be returned as a string. Defaults to None.
            split (bool, optional): If True, split the output `stderr` into a list of
                lines. If False, it will be returned as a single string. The `stderr`
                is passed without any modifications. Defaults to True.

        Returns:
            Process: A Process instance with the output of the command line.
        """
        from subprocess import (
            DEVNULL,
            PIPE,
            Popen,
            STDOUT,
        )

        def comunicate(parameters):
            popen = Popen(**parameters)
            stdout, stderr = popen.communicate()
            return popen, stdout, stderr

        process = cls()
        process.parameters.update(
            {
                "args": args,
                "shell": shell,
                "stdout": PIPE if capture_output else DEVNULL,
                "stderr": PIPE if capture_output else STDOUT,
            }
        )
        if outpath:
            with open(outpath, "w") as file:
                process.parameters.update({"stdout": file})
                popen, stdout, stderr = comunicate(process.parameters)
        else:
            popen, stdout, stderr = comunicate(process.parameters)

        # Postprocess output
        if capture_output:
            if not outpath:
                process.stdout = stdout.strip().split("\n") if split else stdout.strip()
            process.stderr = stderr.strip()
        process.returncode = popen.returncode
        return process
