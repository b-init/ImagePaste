bl_info = {
    "name": "ImagePaste",
    "author": "Binit",
    "blender": (2, 80, 0),
    "version": (1, 6, 0),
    "category": "Import-Export",
    "support": "COMMUNITY",
    "doc_url": "https://github.com/Yeetus3141/ImagePaste#readme",
    "tracker_url": "https://github.com/Yeetus3141/ImagePaste/issues",
    "description": (
        "Paste images from your clipboard to "
        "Image Editor, Shader Editor, 3D Viewport"
    ),
    "location": (
        "Image Editor: Image Menu, "
        "View3D: Add Menu > Image, "
        "Shader Editor: Context Menu"
    ),
}

from .imagepaste import preferences
from .imagepaste import operators


def register():
    preferences.register()
    operators.register()


def unregister():
    operators.unregister()
    preferences.unregister()
