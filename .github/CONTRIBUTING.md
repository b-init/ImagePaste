<!-- @format -->

# Contributing to ImagePaste

First of all, thank you for taking the time to support us. Every change however small helps us grow further, your contributions here are our starting point.

## How do I…

- [🐛 Report a bug](#-reporting-a-bug)
- [🚀 Request a feature](#-requesting-a-feature)
- [💬 Open a discussion](#-opening-a-discussion)
- [🎉 Create a pull request](#-creating-a-pull-request)

Or you can take a look at [our development guide](#-development-guide).

## Code of Conduct

This project and everyone participating in it is governed by [the Code of Conduct](CONTRIBUTING.md) which is adapted from the [Contributor Covenant](https://www.contributor-covenant.org), version 2.0. By participating, you are expected to uphold this code.

## 🐛 Reporting a bug

A great way to contribute to the add-on is to send a detailed report when you encounter an issue. We always appreciate a well-written, thorough bug report, and will thank you for it!

1. **Avoid walls of text**: It's very helpful to attach a log file to your report, which helps us quickly triage the bugs ([learn how to open a terminal](https://docs.blender.org/manual/en/latest/advanced/command_line/launch/index.html) to collect data). When sending lengthy log files, consider posting them as a [Github Gist](https://gist.github.com). Don't forget to remove sensitive data from your log files before posting (you can replace those parts with "REDACTED").

2. **Avoid duplication**: Make sure [the issue database](https://github.com/Yeetus3141/ImagePaste/issues) doesn't already include that problem or suggestion before submitting an issue. If you find a match, you can use the **Subscribe** button to get notified on updates. Do not leave random "+1" or "I have this too" comments, as they only clutter the discussion, and don't help resolving it. However, if you have ways to reproduce the issue or have additional information that may help resolving the issue, please leave a comment.

3. **Simplify**: First try to simplify the process that triggers the bug, so that it is reproducible in the least amount of steps. The less steps there are, the easier it is for us to spot the problem in the code. Typically if you have a complex .blend file, it is possible to keep removing objects, modifiers, nodes, and other data until the problem has been isolated to a simple setup.

Finally, you can [create a new issue](https://github.com/Yeetus3141/ImagePaste/issues/new/choose) by choosing the a **Bug report** template or creating a blank one.

## 🚀 Requesting a feature

If the add-on doesn't do something you need, [open an issue](https://github.com/Yeetus3141/ImagePaste/issues/new/choose) and provide as much context as you can about what you're running into. Please try to be clear about why existing features and alternatives would not work for you. This project is very small, and this makes it flexible, your idea is much more likely to come true. If it isn't accepted, don't have a cow. Sometimes, it's our job to keep the project on the right track.

## 💬 Opening a discussion

We’re using [Discussions](https://github.com/Yeetus3141/ImagePaste/discussions) as a place to connect with other members of our community. You can:

- Ask questions you’re wondering about.
- Share ideas.
- Engage with other community members.
- Welcome others and be open-minded. Remember that this is a community we build muscle together.

Feel free to open one [here](https://github.com/Yeetus3141/ImagePaste/discussions/new).

## 🎉 Creating a pull request

We like code commits a lot! They're super handy, and they keep the project going and doing the work it needs to do to be useful to others.

Code contributions of just about any size of any things in this repository (even the lines you're reading) are acceptable! However, before contributing large or high impact changes, make the effort to coordinate with the maintainers of the project before submitting a pull request. This prevents you from doing extra work that may or may not be merged.

To contribute code:

- Read the [development guide](#development-guide) and [set up the project](#setup-environment-for-development).
- Make any necessary changes to the source code.
- Include any additional documentation the changes might need.
- Test and verify that your contribution works as expected.
- Write clear, concise commit messages using [conventional format](#git-commit).
- [Open a new pull request](https://github.com/Yeetus3141/ImagePaste/compare) with your changes.

We are always thrilled to receive pull requests. We will do our best to process them quickly. If your pull request is not accepted on the first try, don't get discouraged! Keep trying, we're sure you will learn a lot from these.

## 📃 Development guide

### Design decision

#### Architecture and method

The `__init__.py` file includes all mandatory parts for an _Blender_ add-on (`__bl_info__` dictionary, `register` and `unregister` function) and all operators serving the main purposes (operator pasting images as planes, operator pasting images as nodes…). These operators depends on two important function: `GrabImage` (check clipboard and return a list of image files) and `CopyImage` (push given image file to clipboard), which is define in separated modules: `windows/windows.py`, `linux/linux.py` and `darwin/darwin.py` corresponding to _Windows_, _Linux_ and _macOS_ platform respectively. Each module has different approaches solving the problem:

- `windows/windows.py`: We used to rely on _Pillow_ library to handle the clipboard but because of some drawbacks, from the [version 1.5](https://github.com/Yeetus3141/ImagePaste/compare/v1.4.0...v1.5.0) we replace it with the _PowerShell_ 5.1 scripts which is pre-installed from _Windows_ version 1607 (see pull request [#8](https://github.com/Yeetus3141/ImagePaste/pull/8)).
- `linux/linux.py`: we currently support only _X11_ with `xclip`, _Wayland_ haven't been tested and done research yet (see pull request [#4](https://github.com/Yeetus3141/ImagePaste/pull/4)).
- `darwin/darwin.py`: [_Pasteboard_](https://pypi.org/project/pasteboard/) is shipped with add-on to be responsible with clipboard.

#### Naming

To be consistent, anything related to the code or the core system of the platform, we use `darwin` to refer to the _macOS_ platform. For _Windows_ and _Linux_ platform, they are `windows` and `linux` respectively.

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

We follow the [recommended style guide for Blender add-ons](https://wiki.blender.org/wiki/Style_Guide/Python) for all _Python_ files in this repository with these tool:

- Linter: [_Flake8_](https://flake8.pycqa.org/en/latest/) (latest version, which is configured in [`.flake8`](../.flake8)).
- Formatter: [_Black_](https://black.readthedocs.io/en/stable/) (latest version with default settings).

#### Other files

All other files (included _YAML_ and _Markdown_) are formatted by [Prettier](https://prettier.io/), which is configured in [`.prettierrc`](../.prettierrc).

### Set up development environment

If this is your first pull request, you just need to fork the repository and do whatever you need to do. If you have already forked it before, make sure you are on the latest commit before you make any changes, this will prevent some unnecessary conflicts when you request merging into the upstream.

We use _pipenv_ as an environment manager, which is configured in [Pipfile](../Pipfile). These steps will show how to set up a python virtual environment that fits our workflow.

1. Open CLI in the project directory.
1. Run `pipenv install --dev --skip-lock` to install packages for development.
1. After that, a virtual environment has been setup. You can get in using `pipenv shell` and get out with `exit`. Once activated, you will have all packages you need.

Some editor configurations are also defined in [.editorconfig](.editorconfig).

We recommend using Visual Studio Code as an editor. If you also use it, you should have these workspace settings:

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
