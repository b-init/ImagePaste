import bpy

from .helper import ADDON_NAME
from .operators import (
    IMAGEPASTE_OT_imageeditor_copy,
    IMAGEPASTE_OT_imageeditor_paste,
    IMAGEPASTE_OT_sequenceeditor_paste,
    IMAGEPASTE_OT_shadereditor_paste,
    IMAGEPASTE_OT_view3d_paste_plane,
    IMAGEPASTE_OT_view3d_paste_reference,
)


class IMAGEPASTE_AddonPreferences(bpy.types.AddonPreferences):
    """Add-on preferences for ImagePaste"""

    bl_idname = ADDON_NAME

    is_use_another_directory: bpy.props.BoolProperty(
        name="Use a directory",
        description=(
            "Save images to another directory instead of temporary directory"
            " when the file is not saved"
        ),
        default=False,
    )
    another_directory: bpy.props.StringProperty(
        name="Saving directory",
        description="A path to directory where images saved to",
        subtype="DIR_PATH",
    )
    is_force_use_another_directory: bpy.props.BoolProperty(
        name="Force use another directory",
        description="Save images to above directory even when the file is saved or not",
        default=False,
    )
    is_use_subdirectory: bpy.props.BoolProperty(
        name="Use subdirectory",
        description="Save images to a subdirectory where the file is saved",
        default=True,
    )
    subdirectory_name: bpy.props.StringProperty(
        name="Sub directory name",
        description="A name for subdirectory",
        default="ImagePaste",
    )
    image_filename_pattern: bpy.props.StringProperty(
        name="Image file name",
        description=(
            "A name for pasted images\n"
            "%y: Year, %m: Month, %d: Day\n"
            "%H: Hour, %M: Minute, %S: Second"
        ),
        default="ImagePaste-%y%m%d-%H%M%S",
    )
    image_type_to_move: bpy.props.EnumProperty(
        name="Image type to move",
        description="Which type of image will be moved",
        items=[
            ("pasted_images", "Pasted images", "Only pasted images will be moved"),
            ("all_images", "All images", "All images will be moved"),
            ("no_moving", "No moving", "Don't move anything when saving"),
        ],
        default="pasted_images",
    )
    is_disable_debug: bpy.props.BoolProperty(
        name="Disable debug message",
        description="Debug message will not printed in console",
        default=False,
    )

    def draw(self, _context):
        from .helper import is_valid_filename

        split_ratio = 0.3
        layout = self.layout

        # New box
        box = layout.box().column()
        box.label(
            text="Specify a different directory for images when the file is not saved"
        )

        # New property
        prop = box.row(align=True)
        split = prop.split(factor=split_ratio)
        # First column
        column_1 = split.column()
        column_1.alignment = "RIGHT"
        column_1.label(text="Use a directory")
        # Second column
        column_2 = split.column().row(align=True)
        column_2.prop(self, "is_use_another_directory", text="")
        column_2_sub = column_2.column()
        column_2_sub.active = self.is_use_another_directory
        column_2_sub.prop(self, "another_directory", text="")

        # New property
        prop = box.row(align=True)
        split = prop.split(factor=split_ratio)
        # First column
        split.column()
        # Second column
        column_2 = split.column().row(align=True)
        column_2.active = self.is_use_another_directory
        column_2.prop(self, "is_force_use_another_directory", text="Force use")

        # New box
        box = layout.box().column()
        box.label(text="Specify a subdirectory for images when the file is saved")

        # New property
        prop = box.row(align=True)
        prop.active = not (
            self.is_force_use_another_directory and self.is_use_another_directory
        )
        split = prop.split(factor=split_ratio)
        # First column
        column_1 = split.column()
        column_1.alignment = "RIGHT"
        column_1.label(text="Use subdirectory")
        # Second column
        column_2 = split.column().row(align=True)
        column_2.prop(self, "is_use_subdirectory", text="")
        column_2_sub = column_2.column()
        column_2_sub.active = self.is_use_subdirectory
        column_2_sub.prop(self, "subdirectory_name", text="")

        # New box
        box = layout.box().column()
        box.label(text="Custom image file name")

        # New property
        prop = box.row(align=True)
        split = prop.split(factor=split_ratio)
        # First column
        column_1 = split.column()
        column_1.alignment = "RIGHT"
        column_1.label(text="Image file name")
        # Second column
        column_2 = split.column().row(align=True)
        column_2.prop(self, "image_filename_pattern", text="")
        column_2.alert = is_valid_filename(self.image_filename_pattern)

        # New box
        box = layout.box().column()
        box.label(
            text=("Choose the type of images that will be moved when saving the file")
        )

        # New property
        prop = box.row(align=True)
        split = prop.split(factor=split_ratio)
        # First column
        column_1 = split.column()
        column_1.alignment = "RIGHT"
        column_1.label(text="Image type to move")
        # Second column
        column_2 = split.row()
        column_2.prop(self, "image_type_to_move", expand=True)

        # New box
        box = layout.box().column()
        box.label(text="Miscellaneous")

        # New property
        prop = box.row(align=True)
        split = prop.split(factor=split_ratio)
        # First column
        column_1 = split.column()
        column_1.alignment = "RIGHT"
        column_1.label(text="Disable debug message")
        # Second column
        column_2 = split.row()
        column_2.prop(self, "is_disable_debug", text="")


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


def sequenceeditor_paste_contextmenu_draw(self, _context):
    self.layout.separator()
    self.layout.operator(
        IMAGEPASTE_OT_sequenceeditor_paste.bl_idname,
        icon="IMAGE_PLANE",
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


@bpy.app.handlers.persistent
def move_to_saved_directory_handler(self, _context):
    bpy.ops.imagepaste.move_to_saved_directory("INVOKE_DEFAULT")


addon_keymaps = []


def register():
    bpy.utils.register_class(IMAGEPASTE_AddonPreferences)

    bpy.types.IMAGE_MT_image.append(imageeditor_copy_imagemenu_draw)
    bpy.types.IMAGE_MT_image.append(imageeditor_paste_imagemenu_draw)
    bpy.types.SEQUENCER_MT_context_menu.append(sequenceeditor_paste_contextmenu_draw)
    bpy.types.NODE_MT_context_menu.append(shadereditor_paste_contextmenu_draw)
    bpy.types.VIEW3D_MT_image_add.append(view3d_paste_plane_imageaddmenu_draw)
    bpy.types.VIEW3D_MT_image_add.append(view3d_paste_reference_imageaddmenu_draw)
    bpy.app.handlers.save_post.append(move_to_saved_directory_handler)

    kc = bpy.context.window_manager.keyconfigs.addon

    km = kc.keymaps.new(name="Image Generic", space_type="IMAGE_EDITOR")
    kmi = km.keymap_items.new(
        IMAGEPASTE_OT_imageeditor_copy.bl_idname,
        type="C",
        value="PRESS",
        ctrl=True,
        shift=True,
    )
    addon_keymaps.append((km, kmi))

    km = kc.keymaps.new(name="Image Generic", space_type="IMAGE_EDITOR")
    kmi = km.keymap_items.new(
        IMAGEPASTE_OT_imageeditor_paste.bl_idname,
        type="V",
        value="PRESS",
        ctrl=True,
        shift=True,
    )
    addon_keymaps.append((km, kmi))

    km = kc.keymaps.new(name="Sequencer", space_type="SEQUENCE_EDITOR")
    kmi = km.keymap_items.new(
        IMAGEPASTE_OT_sequenceeditor_paste.bl_idname,
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

    km = kc.keymaps.new(name="3D View", space_type="VIEW_3D")
    kmi = km.keymap_items.new(
        IMAGEPASTE_OT_view3d_paste_reference.bl_idname,
        type="V",
        value="PRESS",
        ctrl=True,
        shift=True,
    )
    addon_keymaps.append((km, kmi))


def unregister():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

    bpy.app.handlers.save_post.remove(move_to_saved_directory_handler)
    bpy.types.VIEW3D_MT_image_add.remove(view3d_paste_reference_imageaddmenu_draw)
    bpy.types.VIEW3D_MT_image_add.remove(view3d_paste_plane_imageaddmenu_draw)
    bpy.types.NODE_MT_context_menu.remove(shadereditor_paste_contextmenu_draw)
    bpy.types.SEQUENCER_MT_context_menu.remove(sequenceeditor_paste_contextmenu_draw)
    bpy.types.IMAGE_MT_image.remove(imageeditor_paste_imagemenu_draw)
    bpy.types.IMAGE_MT_image.remove(imageeditor_copy_imagemenu_draw)

    bpy.utils.unregister_class(IMAGEPASTE_AddonPreferences)
