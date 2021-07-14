import os
import platform

import addon_utils
import bpy
from bpy.props import BoolProperty
from bpy.props import StringProperty
from bpy.types import AddonPreferences
from bpy.types import Operator


bl_info = {
    "name": "ImagePaste",
    "author": "Binit",
    "blender": (2, 80, 0),
    "version": (1, 5, 1),
    "category": "Import-Export",
    "doc_url": "https://github.com/Yeetus3141/ImagePaste#readme",
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


class IMAGEPASTE_AddonPreferences(AddonPreferences):
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


class IMAGEPASTE_OT_imageeditor_copy(Operator):
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


class IMAGEPASTE_OT_imageeditor_paste(Operator):
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


class IMAGEPASTE_OT_shadereditor_paste(Operator):
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


class IMAGEPASTE_OT_view3d_paste_plane(Operator):
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


class IMAGEPASTE_OT_view3d_paste_reference(Operator):
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


# Menu functions
def imageeditor_copy_imagemenu_draw(self, context):
    self.layout.operator(
        IMAGEPASTE_OT_imageeditor_copy.bl_idname,
        icon="COPYDOWN",
    )


def imageeditor_paste_imagemenu_draw(self, context):
    self.layout.operator(
        IMAGEPASTE_OT_imageeditor_paste.bl_idname,
        icon="FILE_IMAGE",
    )


def shadereditor_paste_contextmenu_draw(self, context):
    self.layout.operator(
        IMAGEPASTE_OT_shadereditor_paste.bl_idname,
        icon="FILE_IMAGE",
    )


def view3d_paste_plane_imageaddmenu_draw(self, context):
    self.layout.operator(
        IMAGEPASTE_OT_view3d_paste_plane.bl_idname,
        icon="IMAGE_PLANE",
    )


def view3d_paste_reference_imageaddmenu_draw(self, context):
    self.layout.operator(
        IMAGEPASTE_OT_view3d_paste_reference.bl_idname,
        icon="FILE_IMAGE",
    )


# List of all classes to register/unregister
classes = (
    IMAGEPASTE_AddonPreferences,
    IMAGEPASTE_OT_imageeditor_copy,
    IMAGEPASTE_OT_imageeditor_paste,
    IMAGEPASTE_OT_shadereditor_paste,
    IMAGEPASTE_OT_view3d_paste_plane,
    IMAGEPASTE_OT_view3d_paste_reference,
)

# Store keymaps here to access after registration
addon_keymaps = []
kc = None


def register():

    # Register classes
    for current in classes:
        bpy.utils.register_class(current)

    # Register menus
    bpy.types.IMAGE_MT_image.append(imageeditor_copy_imagemenu_draw)
    bpy.types.IMAGE_MT_image.append(imageeditor_paste_imagemenu_draw)
    bpy.types.NODE_MT_context_menu.append(shadereditor_paste_contextmenu_draw)
    bpy.types.VIEW3D_MT_image_add.append(view3d_paste_plane_imageaddmenu_draw)
    bpy.types.VIEW3D_MT_image_add.append(view3d_paste_reference_imageaddmenu_draw)

    # Register keymaps
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name="Image Generic", space_type="IMAGE_EDITOR")
        kmi = km.keymap_items.new(
            IMAGEPASTE_OT_imageeditor_paste.bl_idname,
            type="V",
            value="PRESS",
            ctrl=True,
            shift=True,
        )
        addon_keymaps.append((km, kmi))

        km = kc.keymaps.new(name="3D View", space_type="VIEW_3D")
        kmi = km.keymap_items.new(
            IMAGEPASTE_OT_view3d_paste_reference.bl_idname,
            type="V",
            value="PRESS",
            ctrl=True,
            shift=True,
        )
        addon_keymaps.append((km, kmi))

        km = kc.keymaps.new(name="3D View", space_type="VIEW_3D")
        kmi = km.keymap_items.new(
            IMAGEPASTE_OT_view3d_paste_plane.bl_idname,
            type="V",
            value="PRESS",
            ctrl=True,
            shift=True,
            alt=True,
        )
        addon_keymaps.append((km, kmi))

        km = kc.keymaps.new(name="Node Editor", space_type="NODE_EDITOR")
        kmi = km.keymap_items.new(
            IMAGEPASTE_OT_shadereditor_paste.bl_idname,
            type="V",
            value="PRESS",
            ctrl=True,
            shift=True,
        )
        addon_keymaps.append((km, kmi))

        km = kc.keymaps.new(name="Image Generic", space_type="IMAGE_EDITOR")
        kmi = km.keymap_items.new(
            IMAGEPASTE_OT_imageeditor_copy.bl_idname,
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
    bpy.types.VIEW3D_MT_image_add.remove(view3d_paste_reference_imageaddmenu_draw)
    bpy.types.VIEW3D_MT_image_add.remove(view3d_paste_plane_imageaddmenu_draw)
    bpy.types.NODE_MT_context_menu.remove(shadereditor_paste_contextmenu_draw)
    bpy.types.IMAGE_MT_image.remove(imageeditor_paste_imagemenu_draw)
    bpy.types.IMAGE_MT_image.remove(imageeditor_copy_imagemenu_draw)

    # Unregister keymaps
    if kc:
        for km, kmi in addon_keymaps:
            km.keymap_items.remove(kmi)
        addon_keymaps.clear()
