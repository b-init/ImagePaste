<!-- @format -->

# ImagePaste

A simple _Blender_ add-on to paste your images from the clipboard to various places in the _Blender_ and vice versa, copy them to the clipboard so you can take them anywhere. It works with _Blender_ 2.80 and above.

## Installing

1. Download [the latest release](https://github.com/Yeetus3141/ImagePaste/releases/latest) (you can view the changelog on the [release page](https://github.com/Yeetus3141/ImagePaste/releases)).
2. Go to <kbd><kbd>Edit</kbd>|<kbd>Preferences</kbd></kbd>. On tab <kbd>Add-ons</kbd> choose <kbd>Install</kbd> and select the downloaded `.zip` file, then tick the box beside the add-on name.

## Using

![demo](assets/demo.gif)

| Operator                | Editor type     | Key shortcut                                                            | UI                                                                                                |
| ----------------------- | --------------- | ----------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| Copy Image              | Image Editor    | <kbd><kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>C</kbd></kbd>                | <kbd><kbd>Image</kbd>&vert;<kbd>Copy to Clipboard</kbd></kbd>                                     |
| Paste as Images         | Image Editor    | <kbd><kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>V</kbd></kbd>                | <kbd><kbd>Image</kbd>&vert;<kbd>Paste from Clipboard</kbd></kbd>                                  |
| Paste as Image Strips   | Sequence Editor | <kbd><kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>Alt</kbd>+<kbd>V</kbd></kbd> | <kbd><kbd>Context Menu</kbd>&vert;<kbd>Paste from Clipboard</kbd></kbd>                           |
| Paste as Image Textures | Shader Editor   | <kbd><kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>V</kbd></kbd>                | <kbd><kbd>Context Menu</kbd>&vert;<kbd>Paste from Clipboard</kbd></kbd>                           |
| Paste as Planes         | 3D Viewport     | <kbd><kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>Alt</kbd>+<kbd>V</kbd></kbd> | <kbd><kbd>Add</kbd>&vert;<kbd>Image</kbd>&vert;<kbd>Paste from Clipboard as Plane</kbd></kbd>     |
| Paste as References     | 3D Viewport     | <kbd><kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>V</kbd></kbd>                | <kbd><kbd>Add</kbd>&vert;<kbd>Image</kbd>&vert;<kbd>Paste from Clipboard as Reference</kbd></kbd> |

By default, the images pasted are stored in a temporary directory which is deleted when _Blender_ is closed, but after you save the `.blend` file, they will be saved in the same directory under the `ImagePaste` folder. You can change the directory name, the saving location and other configurations in the add-on preferences.

## Contributing and getting support

This is only a small project and we're happy to know it helped some of you. I just want to say that all this wouldn't have been possible without these [great contributors](https://github.com/Yeetus3141/ImagePaste/graphs/contributors) and everybody who comes with new ideas and feature requests! So thank you all!

It will be great if you have an idea and turn it into visible. Tell us how amazing they are by [suggesting a feature](https://github.com/Yeetus3141/ImagePaste/issues/new/choose), or you can make it yourself by creating [a pull request](https://github.com/Yeetus3141/ImagePaste/compare). And if you encounter a problem, let us know by [opening an issue](https://github.com/Yeetus3141/ImagePaste/issues/new/choose). But before doing anything, let's take a look at [our contributing guide](.github/CONTRIBUTING.md), it will show you how to start with all of that.
