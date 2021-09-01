<!-- @format -->

# Changelog

## [1.7.0](https://github.com/Yeetus3141/ImagePaste/compare/v1.6.1...v1.7.0) (2021-09-01)

- Now you can customize the filename of the pasted images ([#18](https://github.com/Yeetus3141/ImagePaste/pull/18) by [@thanhph111](https://github.com/thanhph111)).
- You can paste the images anytime you want, then save the file and all images you need will be in the target folder ([#17](https://github.com/Yeetus3141/ImagePaste/pull/17) by [@thanhph111](https://github.com/thanhph111)).
- The folder in your `.blend` file will be removed automatically when you quit _Blender_ if it's empty (by [@thanhph111](https://github.com/thanhph111)).
- Copying images in the **Image Editor** won't save it to your folder anymore.

## [1.6.1](https://github.com/Yeetus3141/ImagePaste/compare/v1.6.0...v1.6.1) (2021-08-01)

- Fix the logic of getting the save directory.

## [1.6.0](https://github.com/Yeetus3141/ImagePaste/compare/v1.5.1...v1.6.0) (2021-07-27)

- Now you can paste your image to the _Video Sequence Editor_ as an image strip with a button in the context menu, thanks to [@tin2tin](https://github.com/tin2tin) (read more at [#16](https://github.com/Yeetus3141/ImagePaste/pull/16)).
- The add-on now stores the pasted images in a temporary folder by default, they will be deleted after _Blender_ is closed, but from the time you save your session, they will be saved under the `ImagePaste` folder in the same directory as the `.blend` file ([#14](https://github.com/Yeetus3141/ImagePaste/pull/14) by [@thanhph111](https://github.com/thanhph111)).
- Redesigned preferences UI with an option to change the name of the default folder and another option to force the add-on to use a different folder for your temporary images ([#14](https://github.com/Yeetus3141/ImagePaste/pull/14) by [@thanhph111](https://github.com/thanhph111)).
- All operators now only run if they are in their context so you never have to worry about annoying errors (even they're now more friendly) ([#14](https://github.com/Yeetus3141/ImagePaste/pull/14) by [@thanhph111](https://github.com/thanhph111)).
- We also want to thank [@williamchange](https://github.com/williamchange) for helping us to implement new code architecture on _macOS_.

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
