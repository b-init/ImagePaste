from __future__ import annotations
import sys

if sys.platform == "win32":
    from .clipboard.windows.windows import WindowsClipboard as Clipboard
elif sys.platform == "linux":
    from .clipboard.linux.linux import LinuxClipboard as Clipboard
elif sys.platform == "darwin":
    from .clipboard.darwin.darwin import DarwinClipboard as Clipboard
else:
    raise RuntimeError(f"Unsupported platform '{sys.platform}'.")


import bpy


class IMAGEPASTE_OT_imageeditor_copy(bpy.types.Operator):
    """Copy image to the clipboard"""

    bl_idname = "imagepaste.imageeditor_copy"
    bl_label = "Copy to Clipboard"
    bl_options = {"UNDO_GROUPED"}

    def execute(self, context):
        from os.path import join
        from .metadata import get_addon_preferences

        active_image = context.area.spaces.active.image
        # If active image is render result, save it first
        if active_image.filepath != "":
            image_path = active_image.filepath
        else:
            image_extension = get_addon_preferences().image_extension
            image_path = join(bpy.app.tempdir, active_image.name + image_extension)
            bpy.ops.image.save_as(save_as_render=True, copy=True, filepath=image_path)
        # Report and log the result
        clipboard = Clipboard.pull(image_path)
        clipboard.report.log(self)
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

    bl_idname = "imagepaste.imageeditor_paste"
    bl_label = "Paste from Clipboard"
    bl_options = {"UNDO_GROUPED"}

    def execute(self, context):
        from .tree import get_save_directory

        clipboard = Clipboard.push(get_save_directory())
        clipboard.report.log(self)
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


class IMAGEPASTE_OT_sequenceeditor_paste(bpy.types.Operator):
    """Paste images from the clipboard"""

    bl_idname = "imagepaste.sequenceeditor_paste"
    bl_label = "Paste from Clipboard"
    bl_options = {"UNDO_GROUPED"}

    def execute(self, context):
        from .tree import get_save_directory

        clipboard = Clipboard.push(get_save_directory())
        clipboard.report.log(self)
        if clipboard.report.type != "INFO":
            return {"CANCELLED"}
        sequences = context.scene.sequence_editor.sequences
        current_frame = context.scene.frame_current
        for image in clipboard.images:
            image_strip = sequences.new_image(
                name=image.filename,
                filepath=image.filepath,
                channel=1,
                frame_start=current_frame,
            )
            image_strip.frame_final_end = current_frame + 50
        return {"FINISHED"}

    @classmethod
    def poll(_cls, context):
        return context.area.type == "SEQUENCE_EDITOR"


class IMAGEPASTE_OT_shadereditor_paste(bpy.types.Operator):
    """Paste images from the clipboard as image texture nodes"""

    bl_idname = "imagepaste.shadereditor_paste"
    bl_label = "Paste from Clipboard"
    bl_options = {"UNDO_GROUPED"}

    def execute(self, context):
        from .tree import get_save_directory

        clipboard = Clipboard.push(get_save_directory())
        clipboard.report.log(self)
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

    bl_idname = "imagepaste.view3d_paste_plane"
    bl_label = "Paste from Clipboard as Plane"
    bl_options = {"UNDO_GROUPED"}

    def execute(self, _context):
        from addon_utils import enable
        from .tree import get_save_directory

        # Enable the "Import Images as Planes" add-on to be used here
        enable("io_import_images_as_planes")

        clipboard = Clipboard.push(get_save_directory())
        clipboard.report.log(self)
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

    bl_idname = "imagepaste.view3d_paste_reference"
    bl_label = "Paste from Clipboard as Reference"
    bl_options = {"UNDO_GROUPED"}

    def execute(self, _context):
        from .tree import get_save_directory

        clipboard = Clipboard.push(get_save_directory())
        clipboard.report.log(self)
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


class IMAGEPASTE_OT_move_to_save_directory(bpy.types.Operator):
    """Move images to a target directory"""

    bl_idname = "imagepaste.move_to_save_directory"
    bl_label = "Move to Target Directory"
    bl_options = {"UNDO_GROUPED"}

    def __init__(self) -> None:
        from .tree import get_save_directory

        super().__init__()
        self.save_directory = get_save_directory()
        self.orphaned_images = self.get_orphaned_images(self.save_directory)

    def execute(self, _context):
        from .image import Image
        from .report import Report

        pasted_images = Image.pasted_images
        orphaned_image_filepaths = []
        # Change the paths the images refers to with the new one
        for orphaned_image in self.orphaned_images:
            old_filepath = self.get_abspath(orphaned_image.filepath)
            self.change_image_directory(orphaned_image, self.save_directory)
            new_filepath = self.get_abspath(orphaned_image.filepath)
            # Also change in the dictionary
            if old_filepath in pasted_images:
                pasted_images[new_filepath] = pasted_images.pop(old_filepath)
                pasted_images[new_filepath].filepath = new_filepath
            orphaned_image_filepaths.append(old_filepath)
        # Remove pasted images which are not in `.blend` file (pasted but then undone)
        existing_images = [
            self.get_abspath(image.filepath)
            for image in bpy.data.images
            if image.filepath
        ]
        for filepath in list(pasted_images.keys()):
            if filepath not in existing_images:
                del pasted_images[filepath]
        Report(7, f"Pasted images after: {list(pasted_images.keys())}").log(self)
        Report.console_log(f"Blend images after: {existing_images}")
        return {"FINISHED"}

    def invoke(self, context, _event):
        if self.orphaned_images:
            self.execute(context)
        return {"CANCELLED"}

    @classmethod
    def poll(_cls, _context):
        return bool(bpy.data.filepath)

    def get_abspath(self, path: str) -> str:
        """Get the absolute path of a file or directory.

        Args:
            path (str): The path to get the absolute path of.

        Returns:
            str: The absolute path of the file or directory.
        """
        from os.path import abspath

        return abspath(bpy.path.abspath(path))

    def get_orphaned_images(self, save_directory: str) -> list[bpy.types.Image]:
        """Get images that are not in the target directory.

        Args:
            save_directory (str): The target directory.

        Returns:
            list[bpy.types.Image]: A list of orphaned images.
        """
        from os.path import dirname
        from .image import Image
        from .metadata import get_addon_preferences
        from .report import Report

        preferences = get_addon_preferences()
        if preferences.image_type_to_move == "no_moving":
            return []
        pasted_images = Image.pasted_images
        orphaned_images = []
        orphaned_image_paths = []
        existing_images = []
        for image in bpy.data.images:
            # Example: 'Render Result'
            if not image.filepath:
                continue
            filepath = self.get_abspath(image.filepath)
            existing_images.append(filepath)
            if dirname(filepath) == save_directory:
                continue
            if preferences.image_type_to_move == "all_images":
                orphaned_images.append(image)
                orphaned_image_paths.append(filepath)
                continue
            if filepath in pasted_images:
                orphaned_images.append(image)
                orphaned_image_paths.append(filepath)
        Report.console_log(f"Pasted images before: {list(pasted_images.keys())}")
        Report.console_log(f"Blend images before: {existing_images}")
        Report.console_log(f"Orphaned images: {orphaned_image_paths}")
        return orphaned_images

    def change_image_directory(
        self, orphaned_image: bpy.types.Image, save_directory: str
    ) -> None:
        """Change the directory of an orphaned image.

        Args:
            orphaned_image (bpy.types.Image): An orphaned image.
            save_directory (str): The target directory.
        """
        from os.path import join
        from shutil import copyfile

        new_filepath = join(save_directory, bpy.path.basename(orphaned_image.filepath))
        copyfile(bpy.path.abspath(orphaned_image.filepath), new_filepath)
        orphaned_image.filepath = new_filepath
        orphaned_image.reload()


classes = (
    IMAGEPASTE_OT_imageeditor_copy,
    IMAGEPASTE_OT_imageeditor_paste,
    IMAGEPASTE_OT_sequenceeditor_paste,
    IMAGEPASTE_OT_shadereditor_paste,
    IMAGEPASTE_OT_view3d_paste_plane,
    IMAGEPASTE_OT_view3d_paste_reference,
    IMAGEPASTE_OT_move_to_save_directory,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
