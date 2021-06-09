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

Changelog
--
**v1.0.0 (4th Jan, 21)** 

	* Initial release.

**v1.1.0 (6th Jan, 21)** 

	* Improved error management.
	
	* The images are now saved in the same folder as the .blend file, in a newly created subfolder. If the blend file is not saved, it uses the directory set in preferences or the default temp directory, which might raise permission error. This feature is toggleable via addon preferences.
	
	* Improved the UI in preferences.

**v1.2.0 (6th Feb, 21)**

	* Paste image from clipboard directly as a plane onto the viewport `Ctrl+Shift+Alt+V`.
	
	* Supports image(s) copied from file explorer in Windows.
	
	* Multiple images can now be pasted at the same time if multiple images are copied from the file explorer (only for Windows).
	
	* Fixed an issue where images where saved with the same name in the default direcotry even with different blender sessions and led to different images being loaded from what was pasted
	
	* Added icons for the buttons

**v1.3.0 (12th Mar, 21)**

	* Image(s) can be pasted directly into the Node Editor as Image Texture Node(s), using `Node Editor > Context Menu (Right Click) > Paste Images From Clipboard` or `Ctrl+Shift+V`
	
	* Images can now be copied to clipboard. In the `Image Editor > Image > Copy To Clipboard`, or `Ctrl+Shift+C`. These images are also saved along with other images in the set directory.

**v1.3.1 (14th Mar, 21)**

	* Fixed issue with the copy to clipboard feature where it didn't work as intended for certain cases.

**v1.3.2 (16th Apr, 21)**

	* Updated image naming scheme, now with timestamps, preventing overwriting of saved images.
	
	* Merged seperate build versions of ImagePaste for Blender version below 2.93a and above into one. 
	
**v1.4.0 (10th May, 21)**

	* Now Supports X11 Clipboard on Linux platform, all thanks to [@thanhph111](https://github.com/thanhph111) 
	

Additional Info
--
For any questions, suggestions or bug reports, join [my discord server](https://discord.gg/G8ajxwQuYT) contact me via twitter **@YeetusBlenditus** or e-mail me at **binitnew@gmail.com**
