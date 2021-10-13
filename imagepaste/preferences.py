import bpy

from .metadata import ADDON_NAME
from .operators import (
    IMAGEPASTE_OT_imageeditor_copy,
    IMAGEPASTE_OT_imageeditor_paste,
    IMAGEPASTE_OT_sequenceeditor_paste,
    IMAGEPASTE_OT_shadereditor_paste,
    IMAGEPASTE_OT_view3d_paste_plane,
    IMAGEPASTE_OT_view3d_paste_reference,
)
from .tree import remove_empty_subdirectory


def get_subdirectory_name(self):
    """Get the subdirectory name."""
    return self.get("subdirectory_name", ADDON_NAME)


def set_subdirectory_name(self, value):
    """Set the subdirectory name."""
    from .tree import remove_empty_subdirectory

    # Remove the old subdirectory before setting the new one
    remove_empty_subdirectory(self.subdirectory_name)
    self["subdirectory_name"] = value


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
        default=ADDON_NAME,
        get=get_subdirectory_name,
        set=set_subdirectory_name,
    )
    image_filename_pattern: bpy.props.StringProperty(
        name="Image filename",
        description=(
            "A name for pasted images\n"
            "Go to the Documentation to read more about the variables\n"
            "Warning: Images can be overwritten if they have the same name"
        ),
        default=(
            "${addonName}"
            "-${yearShort}${monthNumber}${day}"
            "-${hour24}${minute}${second}"
        ),
        subtype="FILE_NAME",
    )
    image_extension: bpy.props.StringProperty(
        name="Image extension",
        description="A file extension for pasted images",
        get=lambda _: ".png",
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
        from .tree import populate_filename
        from .tree import is_valid_filename

        split_ratio = 0.3
        layout = self.layout.column(align=True)

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
        box.label(text="Customize image filename")

        # New property
        prop = box.row(align=True)
        split = prop.split(factor=split_ratio)
        # First column
        column_1 = split.column()
        column_1.alignment = "RIGHT"
        column_1.label(text="Image filename")
        # Second column
        column_2 = split.column().row(align=True)
        filename = populate_filename(self.image_filename_pattern) + self.image_extension
        column_2.alert = not is_valid_filename(filename)
        column_2.prop(self, "image_filename_pattern", text="")
        column_2_sub = column_2.column(align=True)
        column_2_sub.alignment = "RIGHT"
        column_2_sub.prop(self, "image_extension", text="")

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
    """Draw the Copy operator in the Image Editor toolbar."""
    self.layout.operator(
        IMAGEPASTE_OT_imageeditor_copy.bl_idname,
        icon="COPYDOWN",
    )


def imageeditor_paste_imagemenu_draw(self, _context):
    """Draw the Paste operator in the Image Editor toolbar."""
    self.layout.operator(
        IMAGEPASTE_OT_imageeditor_paste.bl_idname,
        icon="FILE_IMAGE",
    )


def sequenceeditor_paste_contextmenu_draw(self, _context):
    """Draw the Paste operator in the Sequence Editor context menu."""
    self.layout.separator()
    self.layout.operator(
        IMAGEPASTE_OT_sequenceeditor_paste.bl_idname,
        icon="IMAGE_PLANE",
    )


def shadereditor_paste_contextmenu_draw(self, _context):
    """Draw the Paste operator in the Shader Editor context menu."""
    self.layout.operator(
        IMAGEPASTE_OT_shadereditor_paste.bl_idname,
        icon="FILE_IMAGE",
    )


def view3d_paste_plane_imageaddmenu_draw(self, _context):
    """Draw the Paste as Plane operator in the 3D View Add Image menu."""
    self.layout.operator(
        IMAGEPASTE_OT_view3d_paste_plane.bl_idname,
        icon="IMAGE_PLANE",
    )


def view3d_paste_reference_imageaddmenu_draw(self, _context):
    """Draw the Paste as Reference operator in the 3D View Add Image menu."""
    self.layout.operator(
        IMAGEPASTE_OT_view3d_paste_reference.bl_idname,
        icon="FILE_IMAGE",
    )


@bpy.app.handlers.persistent
def move_to_save_directory_handler(_self, _context):
    """Handler to move the images to the save directory after the file is saved."""
    bpy.ops.imagepaste.move_to_save_directory("INVOKE_DEFAULT")


addon_keymaps = []


def register_keymaps():
    """Register the keymaps."""
    kc = bpy.context.window_manager.keyconfigs.addon
    if not kc:
        return

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


def unregister_keymaps():
    """Unregister the keymaps."""
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()


def register():
    bpy.utils.register_class(IMAGEPASTE_AddonPreferences)
    bpy.types.IMAGE_MT_image.append(imageeditor_copy_imagemenu_draw)
    bpy.types.IMAGE_MT_image.append(imageeditor_paste_imagemenu_draw)
    bpy.types.SEQUENCER_MT_context_menu.append(sequenceeditor_paste_contextmenu_draw)
    bpy.types.NODE_MT_context_menu.append(shadereditor_paste_contextmenu_draw)
    bpy.types.VIEW3D_MT_image_add.append(view3d_paste_plane_imageaddmenu_draw)
    bpy.types.VIEW3D_MT_image_add.append(view3d_paste_reference_imageaddmenu_draw)
    bpy.app.handlers.save_post.append(move_to_save_directory_handler)
    register_keymaps()


def unregister():
    unregister_keymaps()
    remove_empty_subdirectory()
    bpy.app.handlers.save_post.remove(move_to_save_directory_handler)
    bpy.types.VIEW3D_MT_image_add.remove(view3d_paste_reference_imageaddmenu_draw)
    bpy.types.VIEW3D_MT_image_add.remove(view3d_paste_plane_imageaddmenu_draw)
    bpy.types.NODE_MT_context_menu.remove(shadereditor_paste_contextmenu_draw)
    bpy.types.SEQUENCER_MT_context_menu.remove(sequenceeditor_paste_contextmenu_draw)
    bpy.types.IMAGE_MT_image.remove(imageeditor_paste_imagemenu_draw)
    bpy.types.IMAGE_MT_image.remove(imageeditor_copy_imagemenu_draw)
    bpy.utils.unregister_class(IMAGEPASTE_AddonPreferences)
