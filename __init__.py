import os
import platform

import bpy
import addon_utils
from bpy.props import StringProperty, BoolProperty
from bpy.types import Operator, AddonPreferences


bl_info = {
    "name": "ImagePaste",
    "author": "Binit",
    "description": (
        "Paste image from you clipboard as a Reference or into the Image Editor"
    ),
    "blender": (2, 80, 0),
    "version": (1, 5, 0),
    "location": (
        "View3D > Add > Image, "
        "Image Editor > Toolbar > Image, "
        "Node Editor > Context Menu"
    ),
    "warning": "",
    "category": "Import-Export",
}


# Platform router
if platform.system() == "Windows":
    from .windows.windows import GrabImage, CopyImage
elif platform.system() == "Linux":
    from .linux.linux import GrabImage, CopyImage
elif platform.system() == "Darwin":
    from .darwin.darwin import GrabImage, CopyImage
else:
    raise Exception("Unsupported current platform")


# Enable the "Import Images as Planes" addon to be used here
addon_utils.enable("io_import_images_as_planes")


class ImagePastePreferences(AddonPreferences):
    bl_idname = __name__

    default_img_dir: StringProperty(
        name="Default directory",
        subtype="DIR_PATH",
        default=bpy.context.preferences.filepaths.temporary_directory,
    )

    force_default_dir: BoolProperty(
        name="Always use default directory",
        default=False,
    )

    def draw(self, context):
        layout = self.layout
        layout.label(text="Default directory for saving image files.")
        layout.label(
            text=(
                "This directory will be used if"
                "the blend file is not saved, "
                "or always use default directory if it is checked."
            )
        )
        layout.prop(self, "default_img_dir")
        layout.prop(self, "force_default_dir")


class PasteImageToImageEditor(Operator):
    """Paste image from clipboard into the Image Editor"""

    bl_idname = "impaste.paste_ie"
    bl_label = "Paste From Clipboard"
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


class PasteImageToReference(Operator):
    """Load reference image from clipboard"""

    bl_idname = "impaste.paste_ref"
    bl_label = "Paste From Clipboard"
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


class PasteImageAsPlane(Operator):
    """Load image from clipboard as a plane"""

    bl_idname = "impaste.paste_as_plane"
    bl_label = "Paste From Clipboard as Plane"
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


class PasteImageToNodeEditor(Operator):
    """Paste image(s) from clipboard as image texture node(s)"""

    bl_idname = "impaste.paste_as_node"
    bl_label = "Paste Images From Clipboard"
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


class CopyImageToClipboard(Operator):
    """Copy image to clipboard"""

    bl_idname = "impaste.copy_img"
    bl_label = "Copy To Clipboard"
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
                    __name__
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
                    __name__
                ].preferences.default_img_dir

            img_dir = os.path.join(Directory, active_img.name + ".png")
            bpy.ops.image.save_as(save_as_render=True, copy=True, filepath=img_dir)

            CopyImage(img_dir)

        return {"FINISHED"}


# Menu functions
def menu_func_ie(self, context):
    self.layout.operator(PasteImageToImageEditor.bl_idname, icon="FILE_IMAGE")


def menu_func_ref(self, context):
    self.layout.operator(PasteImageToReference.bl_idname, icon="FILE_IMAGE")


def menu_func_as_plane(self, context):
    self.layout.operator(PasteImageAsPlane.bl_idname, icon="IMAGE_PLANE")


def menu_func_as_node(self, context):
    self.layout.operator(PasteImageToNodeEditor.bl_idname, icon="FILE_IMAGE")


def menu_func_to_clipboard(self, context):
    self.layout.operator(CopyImageToClipboard.bl_idname, icon="COPYDOWN")


# List of all classes to register/unregister
classes = (
    PasteImageToReference,
    PasteImageAsPlane,
    PasteImageToImageEditor,
    ImagePastePreferences,
    PasteImageToNodeEditor,
    CopyImageToClipboard,
)

# Store keymaps here to access after registration
addon_keymaps = []
kc = None


def register():

    # Register classes
    for current in classes:
        bpy.utils.register_class(current)

    # Register menus
    bpy.types.IMAGE_MT_image.append(menu_func_ie)
    bpy.types.VIEW3D_MT_image_add.append(menu_func_ref)
    bpy.types.VIEW3D_MT_image_add.append(menu_func_as_plane)
    bpy.types.NODE_MT_context_menu.append(menu_func_as_node)
    bpy.types.IMAGE_MT_image.append(menu_func_to_clipboard)

    # Register keymaps
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name="Image Generic", space_type="IMAGE_EDITOR")
        kmi = km.keymap_items.new(
            PasteImageToImageEditor.bl_idname,
            type="V",
            value="PRESS",
            ctrl=True,
            shift=True,
        )
        addon_keymaps.append((km, kmi))

        km = kc.keymaps.new(name="3D View", space_type="VIEW_3D")
        kmi = km.keymap_items.new(
            PasteImageToReference.bl_idname,
            type="V",
            value="PRESS",
            ctrl=True,
            shift=True,
        )
        addon_keymaps.append((km, kmi))

        km = kc.keymaps.new(name="3D View", space_type="VIEW_3D")
        kmi = km.keymap_items.new(
            PasteImageAsPlane.bl_idname,
            type="V",
            value="PRESS",
            ctrl=True,
            shift=True,
            alt=True,
        )
        addon_keymaps.append((km, kmi))

        km = kc.keymaps.new(name="Node Editor", space_type="NODE_EDITOR")
        kmi = km.keymap_items.new(
            PasteImageToNodeEditor.bl_idname,
            type="V",
            value="PRESS",
            ctrl=True,
            shift=True,
        )
        addon_keymaps.append((km, kmi))

        km = kc.keymaps.new(name="Image Generic", space_type="IMAGE_EDITOR")
        kmi = km.keymap_items.new(
            CopyImageToClipboard.bl_idname,
            type="C",
            value="PRESS",
            ctrl=True,
            shift=True,
        )
        addon_keymaps.append((km, kmi))


def unregister():
    # Unregister classes
    for current in classes:
        bpy.utils.unregister_class(current)

    # Unregister menus
    bpy.types.IMAGE_MT_image.remove(menu_func_ie)
    bpy.types.VIEW3D_MT_image_add.remove(menu_func_ref)
    bpy.types.VIEW3D_MT_image_add.remove(menu_func_as_plane)
    bpy.types.NODE_MT_context_menu.remove(menu_func_as_node)
    bpy.types.IMAGE_MT_image.remove(menu_func_to_clipboard)

    # Unregister keymaps
    if kc:
        for km, kmi in addon_keymaps:
            km.keymap_items.remove(kmi)
        addon_keymaps.clear()


if __name__ == "__main__":
    register()
