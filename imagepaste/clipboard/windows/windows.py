from __future__ import annotations
from posixpath import abspath

from ..clipboard import Clipboard
from ...report import Report
from ...image import Image
from ...process import Process


class WindowsClipboard(Clipboard):
    """A concrete implementation of Clipboard for Windows."""

    def __init__(self, report: Report, images: list[Image] = None) -> None:
        """A concreate implementation of Clipboard for Windows.

        Args:
            report (Report): A Report instance to which results should be reported.
            images (list[Image], optional): A list of Images objects. Defaults to None.
        """
        super().__init__(report, images)

    @classmethod
    def push(cls, save_directory: str) -> WindowsClipboard:
        """A class method for pushing images from the Windows Clipboard.

        Args:
            save_directory (str): A path to a directory to save the pushed images.

        Returns:
            WindowsClipboard: A WindowsClipboard instance, which contains status of
                operations under Report object and a list of Image objects holding
                pushed images information.
        """
        from os.path import join, splitext
        from . import clipette

        filename = cls.get_filename()
        filepath = join(save_directory, filename)

        clipette.open_clipboard()

        # load multiple images first if filepaths are available (as CF_HDROP, id 15)
        if clipette.is_format_available(15):
            filepaths = clipette.get_FILEPATHS()
            clipette.close_clipboard()

            images = [Image(filepath) for filepath in filepaths]
            return cls(Report(6, f"Pasted {len(images)} image files: {images}"), images)

        # get image if available as 'PNG' or 'image/png' which covers pretty much all software.
        # Ditched BITMAP support because blender doesn't completely support all Bitmap sub-formats
        # and I couldn't find any software that copies only as a bitmap.
        output = clipette.get_PNG(save_directory, splitext(filename)[0])
        clipette.close_clipboard()
        if output != 1:
            image = Image(filepath)
            return cls(Report(3, f"Cannot save image: {image} ({process.stderr})"))
        else:
            image = Image(filepath, pasted=True)
            return cls(Report(6, f"Saved and pasted 1 image: {image}"), [image])

        return cls(Report(2))

    @classmethod
    def pull(cls, image_path: str) -> WindowsClipboard:
        """A class method for pulling images to the Windows Clipboard.

        Args:
            image_path (str): A path to an image to be pulled to the clipboard.

        Returns:
            WindowsClipboard: A WindowsClipboard instance, which contains status of
                operations under Report object and a list of one Image object that holds
                information of the pulled image we put its path to the input.
        """
        from . import clipette 
        from bpy.path import abspath

        clipette.open_clipboard()
        clipette.empty_cliboard()
        
        image_path = abspath(image_path)
        image_format = image_path[-3:].lower()
        # bmp (as DIB, DIBV5, BITMAP) and png (as PNG) should be enough formats to work with most applications
        if image_format != 'bmp':
            clipette.set_DIB(cls.convert_image(image_path, 'BMP'))
        else:
            clipette.set_DIB(image_path)

        if image_format != 'png':
            clipette.set_PNG(cls.convert_image(image_path, 'PNG'))
        else:
            clipette.set_PNG(image_path)
            
        clipette.close_clipboard()

        image = Image(image_path)
        return cls(Report(5, f"Copied 1 image: {image}"), [image])


    @staticmethod
    def convert_image(image_path: str, format: str) -> str:
        """A static method to convert image format and get new image filepath. 
        Saves converted image in ImagePaste's working directory.

        Args:
            image_path (str): Filepath of source image.
            format (str): Format to convert image to as in the image extension ('png', 'bmp', etc)

        Returns:
            str: Filepath of converted image.
        """
        # should probably incorpoate this function into the Image class or something
        from ...tree import get_save_directory
        from os.path import join, basename, splitext
        from bpy_extras.image_utils import load_image
        import bpy
        
        RGBA_unsupported = ['BMP', 'JPEG']
        format_ext = {
            'BMP': '.bmp',
            'IRIS': '.rgb',
            'PNG': '.png',
            'JPEG': '.jpg',
            'JPEG2000': '.jp2',
            'TARGA': '.tga',
            'TARGA_RAW': '.tga',
            'CINEON': '.cin',
            'DPX': '.dpx',
            'OPEN_EXR_MULTILAYER': '.exr',
            'OPEN_EXR': '.exr',
            'HDR': '.hdr',
            'TIFF': '.tif',
            'WEBP': '.webp'
        }

        img_settings = bpy.context.scene.render.image_settings
        prev_file_format = img_settings.file_format
        prev_color_mode = img_settings.color_mode
        prev_quality = img_settings.quality

        img_settings.file_format = format
        img_settings.quality = 100
        img_settings.color_mode = 'RGB' if format in RGBA_unsupported else 'RGBA'

        image = load_image(image_path)
        image_path_c = join(get_save_directory(), splitext(basename(image_path))[0] + format_ext[format])
        image.save_render(image_path_c)

        img_settings.file_format = prev_file_format
        img_settings.color_mode = prev_color_mode
        img_settings.quality = prev_quality

        return image_path_c
