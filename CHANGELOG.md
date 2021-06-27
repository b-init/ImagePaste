# Changelog

## [1.5.0](https://github.com/Yeetus3141/ImagePaste/compare/v1.4.0...v1.5.0) (2021-06-22)
- Now Works on MacOS (by [@celestialmaze](https://twitter.com/cmzw_))
- Standardized Github Repository (by [@thanhph111](https://github.com/thanhph111))
- Excluded the use of Pillow module for Windows, now works natively (by [@thanhph111](https://github.com/thanhph111))
- Minor fixes and improvements

## [1.4.0](https://github.com/Yeetus3141/ImagePaste/compare/v1.3.2...v1.4.0) (2021-06-10)
- Now Supports X11 Clipboard on Linux platform, all thanks to [@thanhph111](https://github.com/thanhph111) 

## [1.3.2](https://github.com/Yeetus3141/ImagePaste/compare/v1.3.1...v1.3.2) (2021-04-16)
- Updated image naming scheme, now with timestamps, preventing overwriting of saved images.
- Merged separate build versions of ImagePaste for Blender version below 2.93a and above into one. 

## [1.3.1](https://github.com/Yeetus3141/ImagePaste/compare/v1.3.0...v1.3.1) (2021-03-14)
- Fixed issue with the copy to clipboard feature where it didn't work as intended for certain cases.

## [1.3.0](https://github.com/Yeetus3141/ImagePaste/compare/v1.1.0...v1.3.0) (2021-03-12)
- Image(s) can be pasted directly into the Node Editor as Image Texture Node(s), using `Node Editor > Context Menu (Right Click) > Paste Images From Clipboard` or `Ctrl + Shift + V`
- Images can now be copied to clipboard. In the `Image Editor > Image > Copy To Clipboard`, or `Ctrl + Shift + C`. These images are also saved along with other images in the set directory.

## 1.2.0 (2021-02-06)
- Paste image from clipboard directly as a plane onto the viewport `Ctrl + Shift + Alt + V`.
- Supports image(s) copied from file explorer in Windows.
- Multiple images can now be pasted at the same time if multiple images are copied from the file explorer (only for Windows).
- Fixed an issue where images where saved with the same name in the default directory even with different blender sessions and led to different images being loaded from what was pasted
- Added icons for the buttons

## [1.1.0](https://github.com/Yeetus3141/ImagePaste/compare/v1.0.0...v1.1.0) (2021-01-06) 
- Improved error management.
- The images are now saved in the same folder as the .blend file, in a newly created subfolder. If the blend file is not saved, it uses the directory set in preferences or the default temp directory, which might raise permission error. This feature can be toggled via addon preferences.
- Improved the UI in preferences.

## [1.0.0](https://github.com/Yeetus3141/ImagePaste/releases/tag/v1.0.0) (2021-01-04)
- Initial release.
