<!-- @format -->

# Changelog

## [1.5.1](https://github.com/Yeetus3141/ImagePaste/compare/v1.5.0...v1.5.1) (2021-06-30)

- Fix the crash that occurred when undoing after inserting an image ([#13](https://github.com/Yeetus3141/ImagePaste/issues/13) by [@thanhph111](https://github.com/thanhph111)).

## [1.5.0](https://github.com/Yeetus3141/ImagePaste/compare/v1.4.0...v1.5.0) (2021-06-22)

- Now works on _macOS_ (by [@celestialmaze](https://twitter.com/cmzw_)).
- Standardized _Github_ repository (by [@thanhph111](https://github.com/thanhph111)).
- Excluded the use of _Pillow_ module for _Windows_, now works natively (by [@thanhph111](https://github.com/thanhph111)).
- Minor fixes and improvements.

## [1.4.0](https://github.com/Yeetus3141/ImagePaste/compare/v1.3.2...v1.4.0) (2021-06-10)

- Now supports _X11_ clipboard on _Linux_ platform, (by [@thanhph111](https://github.com/thanhph111)).

## [1.3.2](https://github.com/Yeetus3141/ImagePaste/compare/v1.3.1...v1.3.2) (2021-04-16)

- Updated image naming scheme, now with timestamps, preventing overwriting of saved images.
- Merged separate build versions of _ImagePaste_ for _Blender_ version below 2.93a and above into one.

## [1.3.1](https://github.com/Yeetus3141/ImagePaste/compare/v1.3.0...v1.3.1) (2021-03-14)

- Fixed issue with the **Copy to clipboard** feature where it didn't work as intended for certain cases.

## [1.3.0](https://github.com/Yeetus3141/ImagePaste/compare/v1.1.0...v1.3.0) (2021-03-12)

- Images can be pasted directly into the **Node Editor** as **Image Texture Nodes**, using <kbd><kbd>Context Menu</kbd>|<kbd>Paste Images from Clipboard</kbd></kbd> or <kbd><kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>V</kbd></kbd>.
- Images can now be copied to the clipboard in the **Image Editor**: <kbd><kbd>Image</kbd>|<kbd>Copy To Clipboard</kbd></kbd> or <kbd><kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>C</kbd></kbd>. These images are also saved along with other images in the set directory.


## 1.2.0 (2021-02-06)

- Paste images from clipboard directly as a plane onto the viewport: <kbd><kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>Alt</kbd>+<kbd>V</kbd></kbd>.
- Support images copied from file explorer in _Windows_.
- Multiple images can now be pasted at the same time if multiple images are copied from the file explorer (only for _Windows_).
- Fixed an issue where images were saved with the same name in the default directory even with different _Blender_ sessions and led to different images being loaded from what was pasted.
- Added icons for the buttons.

## [1.1.0](https://github.com/Yeetus3141/ImagePaste/compare/v1.0.0...v1.1.0) (2021-01-06)

- Improved error management.
- The images are now saved in the same folder as the `.blend` file, in a newly created subfolder. If the blend file is not saved, it uses the directory set in preferences or the default temp directory, which might raise permission errors. This feature can be toggled via add-on preferences.
- Improved the UI in preferences.

## [1.0.0](https://github.com/Yeetus3141/ImagePaste/releases/tag/v1.0.0) (2021-01-04)

- Initial release.
