import sys

# Platform-specific import
if sys.platform == "win32":
    from .clipboard.windows.windows import WindowsClipboard as Clipboard
elif sys.platform == "linux":
    from .clipboard.linux.linux import LinuxClipboard as Clipboard
elif sys.platform == "darwin":
    from .clipboard.darwin.darwin import DarwinClipboard as Clipboard
else:
    raise RuntimeError(f"Unsupported platform '{sys.platform}'.")


import bpy


def get_save_directory() -> str:
    """Get the path to the directory where the images are saved.

    Returns:
        str: The path to the directory where the images are saved.
    """
    return bpy.data.filepath or bpy.app.tempdir


class IMAGEPASTE_OT_imageeditor_copy(bpy.types.Operator):
    """Copy image to the clipboard"""

    bl_idname = "imagepaste.copy_imageeditor"
    bl_label = "Copy to Clipboard"
    bl_options = {"UNDO_GROUPED"}

    def execute(self, context):
        from os.path import join

        active_image = context.area.spaces.active.image
        # If active image is render result, save it first
        if active_image.filepath != "":
            image_path = active_image.filepath
        else:
            image_path = join(get_save_directory(), active_image.name + ".png")
            bpy.ops.image.save_as(save_as_render=True, copy=True, filepath=image_path)
        # Report and log the result
        clipboard = Clipboard.pull(image_path)
        clipboard.report.log()
        self.report({clipboard.report.type}, clipboard.report.message)
        if clipboard.report.type != "INFO":
            return {"CANCELLED"}
        return {"FINISHED"}

    @classmethod
    def poll(_cls, context):
        return (
            context.area.type == "IMAGE_EDITOR"
            and context.area.spaces.active.image is not None
            and context.area.spaces.active.image.has_data is True
        )


class IMAGEPASTE_OT_imageeditor_paste(bpy.types.Operator):
    """Paste images from the clipboard"""

    bl_idname = "imagepaste.paste_imageeditor"
    bl_label = "Paste from Clipboard"
    bl_options = {"UNDO_GROUPED"}

    def execute(self, context):
        clipboard = Clipboard.push(get_save_directory())
        clipboard.report.log()
        self.report({clipboard.report.type}, clipboard.report.message)
        if clipboard.report.type != "INFO":
            return {"CANCELLED"}
        for image in clipboard.images:
            bpy.data.images.load(image.filepath)
        last_image_name = clipboard.images[-1].filename
        context.area.spaces.active.image = bpy.data.images[last_image_name]
        return {"FINISHED"}

    @classmethod
    def poll(_cls, context):
        return context.area.type == "IMAGE_EDITOR"


class IMAGEPASTE_OT_shadereditor_paste(bpy.types.Operator):
    """Paste images from the clipboard as image texture nodes"""

    bl_idname = "imagepaste.paste_shadereditor"
    bl_label = "Paste from Clipboard"
    bl_options = {"UNDO_GROUPED"}

    def execute(self, context):
        clipboard = Clipboard.push(get_save_directory())
        clipboard.report.log()
        self.report({clipboard.report.type}, clipboard.report.message)
        if clipboard.report.type != "INFO":
            return {"CANCELLED"}
        tree = context.space_data.edit_tree
        location_X, location_Y = context.space_data.cursor_location
        for image in clipboard.images:
            node_image = tree.nodes.new("ShaderNodeTexImage")
            node_image.location = location_X, location_Y
            # Offset location for next node
            location_Y += 300
            image_data = bpy.data.images.load(filepath=image.filepath)
            node_image.image = image_data
        return {"FINISHED"}

    @classmethod
    def poll(_cls, context):
        return (
            context.area.type == "NODE_EDITOR"
            and context.area.ui_type == "ShaderNodeTree"
            and context.space_data.edit_tree is not None
        )


class IMAGEPASTE_OT_view3d_paste_plane(bpy.types.Operator):
    """Paste images from the clipboard as planes"""

    bl_idname = "imagepaste.paste_view3d_plane"
    bl_label = "Paste from Clipboard as Plane"
    bl_options = {"UNDO_GROUPED"}

    def execute(self, _context):
        from addon_utils import enable

        # Enable the "Import Images as Planes" add-on to be used here
        enable("io_import_images_as_planes")

        clipboard = Clipboard.push(get_save_directory())
        clipboard.report.log()
        self.report({clipboard.report.type}, clipboard.report.message)
        if clipboard.report.type != "INFO":
            return {"CANCELLED"}
        for image in clipboard.images:
            bpy.ops.import_image.to_plane(files=[{"name": image.filepath}])
        return {"FINISHED"}

    @classmethod
    def poll(_cls, context):
        return (
            context.area.type == "VIEW_3D"
            and context.area.ui_type == "VIEW_3D"
            and context.mode == "OBJECT"
        )


class IMAGEPASTE_OT_view3d_paste_reference(bpy.types.Operator):
    """Paste images from the clipboard as references"""

    bl_idname = "imagepaste.paste_view3d_reference"
    bl_label = "Paste from Clipboard as Reference"
    bl_options = {"UNDO_GROUPED"}

    def execute(self, _context):
        clipboard = Clipboard.push(get_save_directory())
        clipboard.report.log()
        self.report({clipboard.report.type}, clipboard.report.message)
        if clipboard.report.type != "INFO":
            return {"CANCELLED"}
        for image in clipboard.images:
            bpy.ops.object.load_reference_image(filepath=image.filepath)
        return {"FINISHED"}

    @classmethod
    def poll(_cls, context):
        return (
            context.area.type == "VIEW_3D"
            and context.area.ui_type == "VIEW_3D"
            and context.mode == "OBJECT"
        )


classes = (
    IMAGEPASTE_OT_imageeditor_copy,
    IMAGEPASTE_OT_imageeditor_paste,
    IMAGEPASTE_OT_shadereditor_paste,
    IMAGEPASTE_OT_view3d_paste_plane,
    IMAGEPASTE_OT_view3d_paste_reference,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
