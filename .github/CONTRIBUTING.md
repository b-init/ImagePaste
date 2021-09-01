<!-- @format -->

# Contributing to ImagePaste

First of all, thank you for taking the time to support us. Every change, no matter how small, helps us grow further. Your contributions here are our starting point.

## How do I…

- 🐛 [Report a bug](#-reporting-a-bug)
- 🚀 [Request a feature](#-requesting-a-feature)
- 💬 [Open a discussion](#-opening-a-discussion)
- 🎉 [Create a pull request](#-creating-a-pull-request)

Or you can take a look at [our development guide](#-development-guide).

## Code of Conduct

This project and everyone participating in it are governed by [the Code of Conduct](CODE_OF_CONDUCT.md) which is adapted from the [_Contributor Covenant_](https://www.contributor-covenant.org), version 2.0. By participating, you are expected to uphold this code.

## 🐛 Reporting a bug

A great way to contribute to the add-on is to send a detailed report when you encounter an issue. We always appreciate a well-written, thorough bug report, and will thank you for it!

1. **Avoid walls of text**: It's very helpful to attach a log file to your report, which helps us quickly triage the bugs ([learn how to open a terminal](https://docs.blender.org/manual/en/latest/advanced/command_line/launch/index.html) to collect logs). When sending lengthy log files, consider posting them as a [_GitHub Gist_](https://gist.github.com). Don't forget to remove sensitive data from your log files before posting (you can replace those parts with "REDACTED").

2. **Avoid duplication**: Make sure [the issue database](https://github.com/Yeetus3141/ImagePaste/issues) doesn't already include that problem or suggestion before submitting an issue. If you find a match, you can use the **Subscribe** button to get notified of updates. Do not leave random "+1" or "I have this too" comments, as they only clutter the discussion. However, if you have ways to reproduce the issue or have additional information that may help to resolve the issue, please leave a comment.

3. **Simplify**: First try to simplify the process that triggers the bug, so that it is reproducible in the least amount of steps. The fewer steps there are, the easier it is for us to spot the problem in the code. Typically if you have a complex .blend file, it is possible to keep removing objects, modifiers, nodes, and other data until the problem has been isolated to a simple setup.

Finally, you can [create a new issue](https://github.com/Yeetus3141/ImagePaste/issues/new/choose) by choosing the **Bug report** template or creating a blank one.

## 🚀 Requesting a feature

If the add-on doesn't do something you need, [open an issue](https://github.com/Yeetus3141/ImagePaste/issues/new/choose) and provide as much context as you can about what you're running into. Please try to be clear about why existing features and alternatives would not work for you. This project is very small, and this makes it flexible, your idea is much more likely to come true. If it isn't accepted, don't have a cow. Sometimes, it's our job to keep the project on the right track.

## 💬 Opening a discussion

We’re using [_Discussions_](https://github.com/Yeetus3141/ImagePaste/discussions) as a place to connect with other members of our community. You can:

- Ask questions you’re wondering about.
- Share ideas.
- Engage with other community members.
- Welcome others and be open-minded. Remember that this is a community we build muscle together.

## 🎉 Creating a pull request

We like code commits a lot! They're super handy, and they keep the project going and doing the work it needs to do to be useful to others.

Code contributions of just about any size of any things in this repository (even the lines you're reading) are acceptable! However, before contributing large or high-impact changes, make the effort to coordinate with the maintainers of the project before submitting a pull request. This prevents you from doing extra work that may or may not be merged.

To contribute code:

- Read the [development guide](#development-guide) and [set up the project](#setup-environment-for-development).
- Make any necessary changes to the source code.
- Include any additional documentation the changes might need.
- Test and verify that your contribution works as expected.
- Write clear, concise commit messages using [the conventional format](#git-commit).
- [Open a new pull request](https://github.com/Yeetus3141/ImagePaste/compare) with your changes.

We are always thrilled to receive pull requests. We will do our best to process them quickly. If your pull request is not accepted on the first try, don't get discouraged! Keep trying, we're sure you will learn a lot from these.

## 📃 Development guide

### Design decision

#### Architecture and method

The add-on code is divided into several modules to make it easier to maintain and extend. In [`__init__.py`](../__init__.py), we only keep the `bl_info` metadata and the `register`, `unregister` functions to register and unregister other modules. The main processing code of the add-on is located in [`imagepaste/`](../imagepaste/), which includes:

- [`process.py`](../imagepaste/process.py): The module holds the `Process` class, which is the utility class that handles the communication with commands or shells.
- [`image.py`](../imagepaste/image.py): The module contains the `Image` class, whose instances hold image information.
- [`report.py`](../imagepaste/report.py): The module for the `Report` class that creates objects containing operations status.
- [`clipboard/`](../imagepaste/clipboard/): The folder that contains all processes related to clipboard, which includes these modules:
  - [`clipboard.py`](../imagepaste/clipboard/clipboard.py): The module with the abstract `Clipboard` class, which all platform-specific clipboard classes inherit from must perform two important class methods - `push` and `pull` - with different appropriate approaches described below.
  - [`windows/windows.py`](../imagepaste/clipboard/windows/windows.py): The module contains the concrete `WindowsClipboard` class of the `Clipboard` for the _Windows_ platform. Used to rely on _Pillow_ library to handle the clipboard but because of some drawbacks, from [version 1.5](https://github.com/Yeetus3141/ImagePaste/compare/v1.4.0...v1.5.0) we replace it with the _PowerShell_ 5.1 scripts which is pre-installed from _Windows_ version 1607 (see pull request [#8](https://github.com/Yeetus3141/ImagePaste/pull/8)).
  - [`linux/linux.py`](../imagepaste/clipboard/linux/linux.py): The module contains the concrete `LinuxClipboard` class of the `Clipboard` for the _Linux_ platform. We currently use _xclip_ to manipulate clipboard on _X11_. _Wayland_ hasn't been tested and done the research yet (see pull request [#4](https://github.com/Yeetus3141/ImagePaste/pull/4)).
  - [`darwin/darwin.py`](../imagepaste/clipboard/darwin/darwin.py): The module contains the concrete `DarwinClipboard` class of the `Clipboard` for the _macOS_ platform. [_Pasteboard_](https://pypi.org/project/pasteboard/) is shipped with the add-on to be responsible for the clipboard (see pull request [#6](https://github.com/Yeetus3141/ImagePaste/pull/6)).
- [`operators.py`](../imagepaste/operators.py): The module with the core operators for main functionalities (copy/paste images from/to the _Blender_ editors), which depend mostly on clipboard instances created from `WindowsClipboard`, `LinuxClipboard` and `DarwinClipboard` classes.
- [`preferences.py`](../imagepaste/preferences.py): The module contains the add-on preferences class, all keymaps and UI-related functions.
- [`tree.py`](../imagepaste/tree.py): The module contains the utilities to work with files, folders, and paths.
- [`metadata.py`](../imagepaste/metadata.py): The module will cover the add-on metadata related operations.

The docstring in each module is also very helpful to understand what the module does and how to use it. Open the module you need and check them.

#### Naming

To be consistent, anything related to the code or the core system of the platform, we use `darwin` to refer to the _macOS_ platform. For _Windows_ and _Linux_ platforms, they are `windows` and `linux` respectively.

#### Branches

We currently use the _Centralized Workflow_ as the official _Git_ workflow, which `main` is the central branch where you can merge from and create pull requests to.

### Style guides

#### Git commit

Example of good commit:

```text
Summarize changes in around 50 characters or less

More detailed explanatory text. Wrap it to 72 characters. The blank
line separating the summary from the body is critical (unless you omit
the body entirely).

Write your commit message in the imperative: "Fix bug" and not "Fixed
bug" or "Fixes bug." But if your commit solves an issue, use "Fixes #1"
as described below.

Explain the problem that this commit is solving. Focus on why you
are making this change as opposed to how (the code explains that).
Are there side effects or other unintuitive consequences of this
change? Here's the place to explain them.

Further paragraphs come after blank lines. A list would be like this:
- Bullet points are okay, too, end with a period.
- Typically a hyphen or asterisk is used for the bullet, followed by a
  single space. Use a hanging indent.

If the commit is related to an issue or pull request, put references to
them at the bottom. Links can be inserted if it's necessary, like this:
https://github.blog/2013-01-22-closing-issues-via-commit-messages/.

See more at #123.
Fixes #456.
```

#### Python

We follow the [recommended _Blender_ add-ons style guide](https://wiki.blender.org/wiki/Style_Guide/Python) for all _Python_ files in this repository with these tools:

- Linter: [_Flake8_](https://flake8.pycqa.org/en/latest/) (latest version, which is configured in [`.flake8`](../.flake8)).
- Formatter: [_Black_](https://black.readthedocs.io/en/stable/) (latest version with default settings).

#### Other files

All other files (including _YAML_ and _Markdown_) will be formatted with [_Prettier_](https://prettier.io/), which is configured in [`.prettierrc`](../.prettierrc).

### Set up a development environment

If this is your first pull request, you just need to fork the repository and do whatever you need to do. If you have already forked it before, make sure you are on the latest commit before you make any changes, this will prevent some unnecessary conflicts when you request merging into the upstream.

We use [_Pipenv_](https://pipenv.pypa.io/en/latest/) as an environment manager, which is configured in [`Pipfile`](../Pipfile). To set up your development environment, simply run [`script\setup.cmd`](script\setup.cmd) (on _Windows_) or [`script\setup.sh`](script\setup.sh) (on _Linux_) and the script will do the rest for you. When it's done, you can get in the virtual environment using `pipenv shell` and get out with `exit`. Once activated, you will have all packages you need.

Some editor configurations are also defined in [`.editorconfig`](.editorconfig). You can read more on the [EditorConfig website](https://editorconfig.org/) about how to set up your IDE/editor to read the file.

We recommend using [_Visual Studio Code_](https://code.visualstudio.com/) as an official editor for this project, although we decided to ignore its `.vscode` folder as it may contain some personal configuration that you would not want to commit. If you also use it, you should have these configurations in your workspace settings:

```jsonc
{
    // Python language configuration
    "[python]": {
        "editor.rulers": [88],
        "editor.wordWrap": "wordWrapColumn",
        "editor.wordWrapColumn": 88
    },
    // Enable and overwrite Flake8 user settings (if any) to be accepted in `.flake8`
    "python.linting.flake8Enabled": true,
    "python.linting.flake8Args": [],
    // Set default Python formatter and reset it to default settings
    "python.formatting.provider": "black",
    "python.formatting.blackArgs": []
}
```
