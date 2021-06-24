<!-- @format -->

# ImagePaste

A simple _Blender_ addon to grab images from your clipboard and paste as a reference image in viewport or onto the image editor, or even copy images from _Blender_ to clipboard.
Works with _Blender_ 2.80 and above.

## Installation

1. Download [the latest release](https://github.com/Yeetus3141/ImagePaste/releases/latest) (you can view the changelog in the [release page](https://github.com/Yeetus3141/ImagePaste/releases)).
2. Go to `Edit > Preferences`, on tab **Addons** choose **Install** and select the downloaded `.zip` file, then tick the box beside the add-on name.
3. Set the directory for saving images to avoid errors.

## Usage

![demo](assets/demo.gif)

| Operator                     | Editor type               | Key shortcut             | UI                                                         |
| ---------------------------- | ------------------------- | ------------------------ | ---------------------------------------------------------- |
| Paste as reference images    | 3D Viewport (Object Mode) | `Ctrl + Shift + V`       | `Add > Image > Paste From Clipboard`                       |
| Paste as planes              | 3D Viewport (Object Mode) | `Ctrl + Shift + Alt + V` | `Add > Image > Paste From Clipboard as Plane`              |
| Paste as image texture nodes | Shader Editor             | `Ctrl + Shift + V`       | `Context Menu (right click) > Paste Images From Clipboard` |
| Paste as images              | Image Editor              | `Ctrl + Shift + V`       | `Image > Paste From Clipboard`                             |
| Copy image to clipboard      | Image Editor              | `Ctrl + Shift + C`       | `Image > Copy To Clipboard`                                |

**Note**:

- It is recommended to save the `.blend` file before using this add-on to prevent the misplacement of image files.
- Running _Blender_ as administrator might fix some errors.
- A material must be created (if not exists already) before using **Paste Image As Node** feature.

## Contributing and getting support

This is only a small project and we're happy to know it helped some of you. I just want to say that all this wouldn't have been possible without these [great contributors](https://github.com/Yeetus3141/ImagePaste/graphs/contributors) and everybody who comes with new ideas and feature requests! So thank you all!

It will be great if you have an idea and turn it into visible. Tell us how amazing they are by [suggest a feature](https://github.com/Yeetus3141/ImagePaste/issues/new/choose), or you can make it yourself by creating [a pull request](https://github.com/Yeetus3141/ImagePaste/compare). And if you encounter an problem, let us know by [opening an issue](https://github.com/Yeetus3141/ImagePaste/issues/new/choose). But before doing anything, let's take a look at [our contributing guide](.github/CONTRIBUTING.md), it will shows you how to start with all of that.
