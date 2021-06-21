# ImagePaste

A simple Blender addon to grab images from your clipboard and paste as a reference image in viewport or onto the image editor, or even copy images from blender to clipboard.
Works with blender 2.80 and above.


## Installation

1. Download the latest release from [releases page](https://github.com/Yeetus3141/ImagePaste/releases/) (you can view the changelog [here](CHANGELOG.md)).
1. Go to `Edit > Preferences > Addons > Install` and select the downloaded zip file, then tick the box beside the add-on name.
1. Set the directory for saving images to avoid errors.


## Usage

- `Ctrl + Shift + V` or `Object Mode > Add > Image > Paste From Clipboard` in Object Mode to paste as a reference image.
- `Ctrl + Shift + Alt + V` or `Object Mode > Add > Image > Paste From Clipboard as Plane` in Object Mode to paste image as a plane.
- `Ctrl + Shift + V` or `Image Editor > Image > Paste From Clipboard` in the Image Editor to paste as image.
- `Ctrl + Shift + V` or `Node Editor > Context Menu (Right Click) > Paste Images From Clipboard` in the Node Editor to paste image(s) as Image Texture Node(s).
- `Ctrl + Shift + C` or `Image Editor > Image > Copy To Clipboard` in the Image Editor to copy active image to clipboard.
- It is recommended to save the blend file before using this add-on to prevent the misplacement of image files.

![demo](assets/demo.gif)


## Notes

- Running Blender as administrator might fix some errors.
- Works on Windows and Linux (X11 server) (by [@thanhph111](https://github.com/thanhph111)), does not work on MacOS (not yet, at least).
- A material must be created (if not exists already) before using **Paste Image As Node** feature.


## Setup environment for development

[Recommended style guide for Blender add-ons](https://wiki.blender.org/wiki/Style_Guide/Python) is followed by this repository with these tool:
- Linter: **Flake8** (latest, configured in [.flake8](.flake8)).
- Formatter: **Black** (latest, default settings).
- Environment manager: **pipenv** (configured in [Pipfile](Pipfile)).

These steps will show how to set up a python virtual environment that fits my workflow.
1. Open CLI in the project directory.
1. Run following command `pipenv install --dev --skip-lock` to install packages for development.
1. After that, a virtual environment has been setup. You can get in using `pipenv shell` and get out with `exit`. Once activated, you will have all packages you need.

Some editor configurations are also defined in [.editorconfig](.editorconfig).

I am personally using Visual Studio Code as editor. If you also use it, you should have these workspace settings:

```jsonc
{
    // Python language configuration
    "[python]": {
        "editor.rulers": [88],
        "editor.wordWrap": "wordWrapColumn",
        "editor.wordWrapColumn": 88
    },
    // Enable and overwrite flake8 user settings (if any) to be accepted in .flake8
    "python.linting.flake8Enabled": true,
    "python.linting.flake8Args": [],
    // Set default Python formatter and reset it to default settings
    "python.formatting.provider": "black",
    "python.formatting.blackArgs": []
}
```


## Additional Info

For any questions, suggestions or bug reports, join [my discord server](https://discord.gg/G8ajxwQuYT) contact me via twitter **@YeetusBlenditus** or e-mail me at **binitnew@gmail.com**.
