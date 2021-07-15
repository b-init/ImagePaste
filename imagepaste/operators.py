import os
import platform

import addon_utils
import bpy


# Platform router
if platform.system() == "Windows":
    from .clipboard.windows.windows import GrabImage, CopyImage
elif platform.system() == "Linux":
    from .clipboard.linux.linux import GrabImage, CopyImage
elif platform.system() == "Darwin":
    from .clipboard.darwin.darwin import GrabImage, CopyImage
else:
    raise Exception("Unsupported current platform")


# Enable the "Import Images as Planes" addon to be used here
addon_utils.enable("io_import_images_as_planes")


class IMAGEPASTE_OT_imageeditor_copy(bpy.types.Operator):
    """Copy image to clipboard"""

    bl_idname = "imagepaste.copy_imageeditor"
    bl_label = "Copy to Clipboard"
    bl_options = {"UNDO_GROUPED"}

    def execute(self, context):
        for area in context.screen.areas:
            if area.type == "IMAGE_EDITOR":
                active_img = area.spaces.active.image

        if active_img.filepath:
            CopyImage(active_img.filepath)

        else:
            if (
                bpy.data.filepath
                and not bpy.context.preferences.addons[
                    __package__.split(".")[0]
                ].preferences.force_default_dir
            ):
                # If saved and force_default_directory is set to false
                # save image in the place where the .blend file is saved
                # in a newly created subfolder
                Directory = os.path.join(
                    os.path.split(bpy.data.filepath)[0], "ImagePaste"
                )

                if not os.path.isdir(Directory):
                    os.mkdir(Directory)

            else:
                # Just use the default location otherwise
                Directory = bpy.context.preferences.addons[
                    __package__.split(".")[0]
                ].preferences.default_img_dir

            img_dir = os.path.join(Directory, active_img.name + ".png")
            bpy.ops.image.save_as(save_as_render=True, copy=True, filepath=img_dir)

            CopyImage(img_dir)

        return {"FINISHED"}


class IMAGEPASTE_OT_imageeditor_paste(bpy.types.Operator):
    """Paste image from clipboard into the Image Editor"""

    bl_idname = "imagepaste.paste_imageeditor"
    bl_label = "Paste from Clipboard"
    bl_options = {"UNDO_GROUPED"}

    def execute(self, context):
        img_data = GrabImage()

        if img_data == 0:
            self.report({"ERROR"}, "No image data on clipboard")
            return {"CANCELLED"}
        elif img_data == 1:
            self.report({"ERROR"}, "Unable to save image")
            return {"CANCELLED"}
        else:
            img_dir, img_name = img_data

        for directory in img_dir:
            bpy.data.images.load(directory)

        current_img = bpy.data.images[img_name[-1]]

        # Set current image as active in image editor
        for area in bpy.context.screen.areas:
            if area.type == "IMAGE_EDITOR":
                area.spaces.active.image = current_img

        return {"FINISHED"}


class IMAGEPASTE_OT_shadereditor_paste(bpy.types.Operator):
    """Paste image(s) from clipboard as image texture node(s)"""

    bl_idname = "imagepaste.paste_shadereditor"
    bl_label = "Paste from Clipboard"
    bl_options = {"UNDO_GROUPED"}

    def execute(self, context):
        img_data = GrabImage()

        if img_data == 0:
            self.report({"ERROR"}, "No image data on clipboard")
            return {"CANCELLED"}
        elif img_data == 1:
            self.report({"ERROR"}, "Unable to save image")
            return {"CANCELLED"}
        else:
            img_dir, _ = img_data

        tree = context.space_data.edit_tree
        locX, locY = context.space_data.cursor_location

        for directory in img_dir:
            node = tree.nodes.new("ShaderNodeTexImage")
            node.location = locX, locY
            # Offset location for next node
            locY += 300

            node_img = bpy.data.images.load(filepath=directory)
            node.image = node_img

        return {"FINISHED"}


class IMAGEPASTE_OT_view3d_paste_plane(bpy.types.Operator):
    """Load image from clipboard as a plane"""

    bl_idname = "imagepaste.paste_view3d_plane"
    bl_label = "Paste from Clipboard as Plane"
    bl_options = {"UNDO_GROUPED"}

    def execute(self, context):
        img_data = GrabImage()

        if img_data == 0:
            self.report({"ERROR"}, "No image data on clipboard")
            return {"CANCELLED"}
        elif img_data == 1:
            self.report({"ERROR"}, "Unable to save image")
            return {"CANCELLED"}
        else:
            img_dir, img_name = img_data

        for directory in img_dir:
            name = os.path.basename(directory)
            path = os.path.dirname(directory)

            bpy.ops.import_image.to_plane(
                files=[{"name": name, "name": name}], directory=path, relative=False
            )

        return {"FINISHED"}


class IMAGEPASTE_OT_view3d_paste_reference(bpy.types.Operator):
    """Load reference image from clipboard"""

    bl_idname = "imagepaste.paste_view3d_reference"
    bl_label = "Paste from Clipboard as Reference"
    bl_options = {"UNDO_GROUPED"}

    def execute(self, context):
        img_data = GrabImage()

        if img_data == 0:
            self.report({"ERROR"}, "No image data on clipboard")
            return {"CANCELLED"}
        elif img_data == 1:
            self.report({"ERROR"}, "Unable to save image")
            return {"CANCELLED"}
        else:
            img_dir, img_name = img_data

        for directory in img_dir:
            bpy.ops.object.load_reference_image(filepath=directory)

        return {"FINISHED"}


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
