import bpy
from bpy.props import BoolProperty
from bpy.props import StringProperty
from bpy.types import AddonPreferences

from .operators import (
    IMAGEPASTE_OT_imageeditor_copy,
    IMAGEPASTE_OT_imageeditor_paste,
    IMAGEPASTE_OT_shadereditor_paste,
    IMAGEPASTE_OT_view3d_paste_plane,
    IMAGEPASTE_OT_view3d_paste_reference,
)


class IMAGEPASTE_AddonPreferences(AddonPreferences):
    bl_idname = __package__.split(".")[0]
    default_img_dir: StringProperty(
        name="Default directory",
        subtype="DIR_PATH",
        default=bpy.context.preferences.filepaths.temporary_directory,
    )
    force_default_dir: BoolProperty(
        name="Always use default directory",
        default=False,
    )

    def draw(self, _context):
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


def imageeditor_copy_imagemenu_draw(self, _context):
    self.layout.operator(
        IMAGEPASTE_OT_imageeditor_copy.bl_idname,
        icon="COPYDOWN",
    )


def imageeditor_paste_imagemenu_draw(self, _context):
    self.layout.operator(
        IMAGEPASTE_OT_imageeditor_paste.bl_idname,
        icon="FILE_IMAGE",
    )


def shadereditor_paste_contextmenu_draw(self, _context):
    self.layout.operator(
        IMAGEPASTE_OT_shadereditor_paste.bl_idname,
        icon="FILE_IMAGE",
    )


def view3d_paste_plane_imageaddmenu_draw(self, _context):
    self.layout.operator(
        IMAGEPASTE_OT_view3d_paste_plane.bl_idname,
        icon="IMAGE_PLANE",
    )


def view3d_paste_reference_imageaddmenu_draw(self, _context):
    self.layout.operator(
        IMAGEPASTE_OT_view3d_paste_reference.bl_idname,
        icon="FILE_IMAGE",
    )


addon_keymaps = []


def register():
    bpy.utils.register_class(IMAGEPASTE_AddonPreferences)

    bpy.types.IMAGE_MT_image.append(imageeditor_copy_imagemenu_draw)
    bpy.types.IMAGE_MT_image.append(imageeditor_paste_imagemenu_draw)
    bpy.types.NODE_MT_context_menu.append(shadereditor_paste_contextmenu_draw)
    bpy.types.VIEW3D_MT_image_add.append(view3d_paste_plane_imageaddmenu_draw)
    bpy.types.VIEW3D_MT_image_add.append(view3d_paste_reference_imageaddmenu_draw)

    kc = bpy.context.window_manager.keyconfigs.addon
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
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

    bpy.types.VIEW3D_MT_image_add.remove(view3d_paste_reference_imageaddmenu_draw)
    bpy.types.VIEW3D_MT_image_add.remove(view3d_paste_plane_imageaddmenu_draw)
    bpy.types.NODE_MT_context_menu.remove(shadereditor_paste_contextmenu_draw)
    bpy.types.IMAGE_MT_image.remove(imageeditor_paste_imagemenu_draw)
    bpy.types.IMAGE_MT_image.remove(imageeditor_copy_imagemenu_draw)

    bpy.utils.unregister_class(IMAGEPASTE_AddonPreferences)
