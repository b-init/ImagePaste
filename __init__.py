bl_info = {
    "name": "ImagePaste",
    "author": "Binit",
    "blender": (2, 80, 0),
    "version": (1, 8, 2),
    "category": "Import-Export",
    "support": "COMMUNITY",
    "doc_url": "https://github.com/b-init/ImagePaste#readme",
    "tracker_url": "https://github.com/b-init/ImagePaste/issues",
    "description": "Copy and paste your images with the clipboard in various places",
    "location": "Image Editor, Video Sequencer, Shader Editor, 3D Viewport",
}

from .imagepaste import preferences
from .imagepaste import operators


def register():
    preferences.register()
    operators.register()


def unregister():
    operators.unregister()
    preferences.unregister()
