#ImagePaste addon for Blender 2.80+ to paste image from your clipboard into your blender workflow
#Managed by: Binit (aka Yeetus)


# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "ImagePaste",
    "author" : "Binit",
    "description" : "Paste image from you clipboard as a Reference or into the Image Editor",
    "blender" : (2, 80, 0),
    "version" : (1, 0, 0),
    "location" : "Object Mode > Toolbar > Add > Image > Paste From Clipboard, Image Editor > Toolbar > Image > Paste From Clipboard",
    "warning" : "",
    "category" : "Import"
}

import bpy
from bpy.types import Operator, AddonPreferences
from bpy.props import StringProperty
from .PIL import ImageGrab

times_executed = 0

def grabImage():
    global times_executed

    img = ImageGrab.grabclipboard()
    img_name = 'PastedImage' + str(times_executed) + '.png'
    Directory = bpy.context.preferences.addons[__name__].preferences.Directory
    img_dir = Directory + '\\' + img_name
    img.save(img_dir)

    times_executed += 1

    return img_dir, img_name


def loadImage(reference=False):

    img_dir, img_name = grabImage()

    if reference:
        bpy.ops.object.load_reference_image(filepath=img_dir)
    else:
        bpy.data.images.load(img_dir)
        current_img = bpy.data.images[img_name]

        #set current image as active in image editor
        for area in bpy.context.screen.areas :
            if area.type == 'IMAGE_EDITOR' :
                area.spaces.active.image = current_img



class ImagePastePreferences(AddonPreferences):
    bl_idname = __name__

    Directory = bpy.props.StringProperty(default= bpy.context.preferences.filepaths.temporary_directory)

    def draw(self, context):
        layout = self.layout
        layout.label(text="Set Directory for saving the images. Set this to non-primary drive location to avoid permission errors (e.g. Local Disk (D:), D:\\Images)")
        layout.prop(self, "Directory")



class PasteImageToImageEditor(bpy.types.Operator):
    """Paste image from clipboard into the Image Editor"""
    bl_idname = "imgpaste.paste_ie"
    bl_label = "Paste From Clipboard"


    def execute(self, context):
        loadImage(reference=False)

        return {'FINISHED'}

class PasteImageToReference(bpy.types.Operator):
    """Load reference image from clipboard"""
    bl_idname = "impaste.paste_ref"
    bl_label = "Paste From Clipboard"

    def execute(self, context):
        loadImage(reference=True)

        return {'FINISHED'}


# menu functions
def menu_func_ie(self, context):
    self.layout.operator(PasteImageToImageEditor.bl_idname)
def menu_func_ref(self, context):
    self.layout.operator(PasteImageToReference.bl_idname)

# store keymaps here to access after registration
addon_keymaps = []


def register():

    # register classes
    bpy.utils.register_class(PasteImageToImageEditor)
    bpy.utils.register_class(PasteImageToReference)
    bpy.utils.register_class(ImagePastePreferences)

    # register menus
    bpy.types.IMAGE_MT_image.append(menu_func_ie)
    bpy.types.VIEW3D_MT_image_add.append(menu_func_ref)

    # register keymaps
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='Image Generic',space_type='IMAGE_EDITOR')
        kmi = km.keymap_items.new(PasteImageToImageEditor.bl_idname,type='V',value='PRESS',ctrl=True,shift=True)
        addon_keymaps.append((km,kmi))

        km = kc.keymaps.new(name='3D View',space_type='VIEW_3D')
        kmi = km.keymap_items.new(PasteImageToReference.bl_idname,type='V',value='PRESS',ctrl=True,shift=True)
        addon_keymaps.append((km,kmi))


def unregister():

    # unregister classes
    bpy.utils.unregister_class(PasteImageToImageEditor)
    bpy.utils.unregister_class(PasteImageToReference)
    bpy.utils.unregister_class(ImagePastePreferences)

    # unregister menus
    bpy.types.IMAGE_MT_image.remove(menu_func_ie)
    bpy.types.VIEW3D_MT_image_add.remove(menu_func_ref)

    # unregister keymaps
    for km,kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

if __name__ == "__main__":
    register()