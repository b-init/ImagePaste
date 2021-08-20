<!-- @format -->

# ImagePaste

A simple _Blender_ add-on to paste your images from the clipboard to various places in the _Blender_ and vice versa, copy them to the clipboard so you can take them anywhere. It works with _Blender_ 2.80 and above.

## Installing

1. Download [the latest release](https://github.com/Yeetus3141/ImagePaste/releases/latest) (you can view the changelog on the [release page](https://github.com/Yeetus3141/ImagePaste/releases)).
2. Go to <kbd><kbd>Edit</kbd>|<kbd>Preferences</kbd></kbd>. On the <kbd>Add-ons</kbd> tab, choose <kbd>Install</kbd> and select the downloaded `.zip` file, then tick the box beside the add-on name.

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

## Configuring

![preferences](assets/preferences.png)

### Customizing the save folder

By default, pasted images will be stored in a temporary folder, this one will be deleted when you close _Blender_. If you want, you can redirect these images to a different directory.

On the other hand, after you save the `.blend` file, these pasted images will be saved where the `.blend` file is located - in the `ImagePaste` folder. This folder can also be customized in the preferences.

### Customizing the image filename

You can customize the filename of the pasted image with the help of some predefined variables:

| Variable              | Description                                          | Example                        |
| --------------------- | ---------------------------------------------------- | ------------------------------ |
| `${addonName}`        | Name of the add-on                                   | _ImagePaste_                   |
| `${yearLong}`         | Year with the century                                | 2021, 2022, …                  |
| `${yearShort}`        | Year without the century                             | 21, 22, …                      |
| `${monthNumber}`      | Month as a zero-padded decimal number                | 01, 02, …, 12                  |
| `${monthNameLong}`    | Full month name                                      | January, February, …, December |
| `${monthNameShort}`   | Abbreviated month name                               | Jan, Feb, …, Dec               |
| `${day}`              | Day of the month as a zero-padded decimal number     | 01, 02, …, 31                  |
| `${weekdayNumber}`    | Weekday as a decimal number                          | 0, 1, …, 6                     |
| `${weekdayNameLong}`  | Full weekday name                                    | Sunday, Monday, …, Saturday    |
| `${weekdayNameShort}` | Abbreviated weekday name                             | Sun, Mon, …, Sat               |
| `${hour24}`           | Hour (24-hour clock) as a zero-padded decimal number | 00, 01, …, 23                  |
| `${hour12}`           | Hour (12-hour clock) as a zero-padded decimal number | 01, 02, …, 12                  |
| `${minute}`           | Minute as a zero-padded decimal number               | 00, 01, …, 59                  |
| `${second}`           | Second as a zero-padded decimal number               | 00, 01, …, 59                  |
| `${index}`            | Order of the image                                   | 1, 2, …                        |
| `${index:N}`          | N-digits image order number with zero padding        | `${index:2}` gives 01, 02, …   |

The default filename is `${addonName}-${yearShort}${monthNumber}${day}-${hour24}${minute}${second}`.

### Choosing the image type to move when saving the file

This feature will move (actually copy) pasted images (or all images) you have imported into the save directory after you save the file, so you don't have to worry about missing images anymore. There's also an option in the add-on preferences you can choose the type of images to move:

- **Pasted images**: Only images that were pasted using the add-on would be moved to the save directory.
- **All images**: Images existing in the `.blend` file will be moved.
- **No moving**: Don't do anything when saving the file.

## Contributing and getting support

This is only a small project and we're happy to know it helped some of you. I just want to say that all this wouldn't have been possible without these [great contributors](https://github.com/Yeetus3141/ImagePaste/graphs/congittributors) and everybody who comes with new ideas and bug reports! So thank you all!

It will be great if you have an idea and turn it into visible. Tell us how amazing they are by [suggesting a feature](https://github.com/Yeetus3141/ImagePaste/issues/new/choose), or you can make it yourself by creating [a pull request](https://github.com/Yeetus3141/ImagePaste/compare). And if you encounter a problem, let us know by [opening an issue](https://github.com/Yeetus3141/ImagePaste/issues/new/choose). But before doing anything, let's take a look at [our contributing guide](.github/CONTRIBUTING.md), it will show you how to start with all of that.
