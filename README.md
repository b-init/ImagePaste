ImagePaste
==

A simple Blender addon to grab images from your clipboard and paste as a reference image in viewport or onto the image editor. 
Works with blender 2.80 and above.

Installation
--
* Download the latest release from [releases](https://github.com/Yeetus3141/ImagePaste/releases/)
* Go to `Edit > Preferences > Addons > Install` and select the downloaded zip file.
* Set the directory for saving images to avoid errors.

Usage
--
* **Ctrl+Shift+V** or `Object Mode > Add > Image > Paste From Clipboard` in Object Mode to paste as a reference image.
* **Ctrl+Shift+V** or `Image Editor > Image > Paste From Clipboard` in the Image Editor to paste as image.

Changelog
--
**v1.0.0 (4th Jan, 20)** 
	* Initial release.

**v1.1.0 (6th Jan, 20)** 
	* Improved error management.
	* The images are now saved in the same folder as the .blend file, in a newly created subfolder. If the blend file is not saved, it uses the directory set in preferences or the default temp directory, which might raise permission error. This feature is toggleable via addon preferences.
	* Improved the UI in preferences.

Notes
--
* Running Blender as adminstrator might fix some errors.
* Not tested on linux/Mac. Seems to be not working on Mac (Please message me if it works on your Linux/Mac device)

Additional Info
--
For any questions, suggestions or bug reports, contact me via twitter **@YeetusBlenditus** or e-mail me at **binitnew@gmail.com**
