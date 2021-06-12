ImagePaste
==

A simple Blender addon to grab images from your clipboard and paste as a reference image in viewport or onto the image editor, or even copy images from blender to clipboard.
Works with blender 2.80 and above.

Installation
--
* Download the latest release from [releases page on github](https://github.com/Yeetus3141/ImagePaste/releases/)
* Go to `Edit > Preferences > Addons > Install` and select the downloaded zip file.
* Set the directory for saving images to avoid errors.

Usage
--
* **Ctrl+Shift+V** or `Object Mode > Add > Image > Paste From Clipboard` in Object Mode to paste as a reference image.
* **Ctrl+Shift+Alt+V** or `Object Mode > Add > Image > Paste From Clipboard as Plane` in Object Mode to paste image as a plane
* **Ctrl+Shift+V** or `Image Editor > Image > Paste From Clipboard` in the Image Editor to paste as image.
* **Ctrl+Shift+V** or `Node Editor > Context Menu (Right Click) > Paste Images From Clipboard` in the Node Editor to paste image(s) as Image Texture Node(s).
* **Ctrl+Shift+C** or `Image Editor > Image > Copy To Clipboard` in the Image Editor to copy active image to clipboard.
* It is recommended to save the blend file before using this add-on to prevent the misplacement of image files.

Notes
--
* Running Blender as adminstrator might fix some errors.
* Works on Windows and Linux (X11 Clipboard) (by [@thanhph111](https://github.com/thanhph111)) , does not work on MacOS (not yet, atleast) 
* A material must be created (if not exists already) before using 'Paste Image As Node' feature.

Additional Info
--
For any questions, suggestions or bug reports, join [my discord server](https://discord.gg/G8ajxwQuYT) contact me via twitter **@YeetusBlenditus** or e-mail me at **binitnew@gmail.com**

## Setup environment for development

I am using:

- Editor: **Visual Studio Code**
- Linter: **Flake8**
- Formatter: **Black**
- Environment manager: **pipenv**

These steps will show how to set up a python virtual environment that fits my workflow.

1. Open CLI in the project directory.
1. Run following command `python -m venv .venv`. A **.venv** folder will appear in the project folder.
1. Then run this `pipenv install --dev` to install packages for development.
1. After that, a virtual environment has been setup. You can get in using `pipenv shell` and get out with `exit`. Once activated, you will have all packages you need.
