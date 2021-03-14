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
    "version" : (1, 3, 0),
    "location" : "Object Mode > Toolbar > Add > Image, Image Editor > Toolbar > Image, Node Editor > Context Menu",
    "warning" : "",
    "category" : "Import"
}

import bpy
from bpy.types import Operator, AddonPreferences
from bpy.props import StringProperty, BoolProperty
import addon_utils

from io import BytesIO
from .win32 import win32clipboard
from .PIL import ImageGrab, Image
import os
import random

addon_utils.enable("io_import_images_as_planes") #enable the "Import Images as Planes" addon to be used here

times_executed = 0 #counter to count the number of times an image has been grabbed from clipboard during the current session to name the file accordingly
randstr = 'abcdefghijklmnopqrstuvwxyz' #string of alphabets to select from for the random part of the filename

# function to grab image(s) from clipboard, save them and return their names and paths
def GrabImage():
    global times_executed

    img = ImageGrab.grabclipboard()

    if img == None:
        return 0

    if type(img) == list:
        img_dir = img
        img_name = [os.path.basename(current) for current in img_dir]
        return img_dir, img_name

    #generate the name of the image with random characters to make sure it doesn't load images from different sessions if saved in the same directory
    img_name = 'PastedImage' + str(times_executed) + random.choice(randstr) + random.choice(randstr) + '.png' 

    if bpy.data.filepath and bpy.context.preferences.addons[__name__].preferences.force_default_dir == False: 
        # save image in the place where the blendfile is saved, in a newly created subfolder (if saved and force_default_directory is set to false)
        Directory = os.path.join(os.path.split(bpy.data.filepath)[0], 'ImagePaste')
        
        if os.path.isdir(Directory) == False:
            os.mkdir(Directory)

    else:  
        # just use the default location otherwise
        Directory = bpy.context.preferences.addons[__name__].preferences.default_img_dir

    img_dir = Directory + '\\' + img_name

    try:
        img.save(img_dir) 
    except:
        return 1

    times_executed += 1

    return [img_dir], [img_name]


# function to copy image from given path to clipboard 
def CopyImage(img_path):
    image = Image.open(img_path)

    img_out = BytesIO()
    image.convert('RGB').save(img_out, 'BMP')
    data = img_out.getvalue()[14:]
    img_out.close()

    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
    win32clipboard.CloseClipboard()


class ImagePastePreferences(AddonPreferences):
    bl_idname = __name__

    default_img_dir: StringProperty(
        name= "Default directory",
        subtype= 'DIR_PATH',
        default= bpy.context.preferences.filepaths.temporary_directory,
        )

    force_default_dir: BoolProperty(
        name= "Always use default directory",
        default=False,
        )

    def draw(self, context):
        layout = self.layout
        layout.label(text="Default directory for saving image files. This directory will be used if")
        layout.label(text="The blend file is not saved, or Always use default directory' is checked.")
        layout.prop(self, "default_img_dir")
        layout.prop(self, "force_default_dir")


class PasteImageToImageEditor(Operator):
    """Paste image from clipboard into the Image Editor"""
    bl_idname = "imgpaste.paste_ie"
    bl_label = "Paste From Clipboard"


    def execute(self, context):
        img_data = GrabImage()

        if img_data == 0:
            self.report({'ERROR'}, 'No image data on clipboard')
            return {'CANCELLED'}
        elif img_data == 1:
            self.report({'ERROR'}, 'Unable to save image')
            return {'CANCELLED'}
        else:
            img_dir, img_name = img_data

        for directory in img_dir:
            bpy.data.images.load(directory)

        current_img = bpy.data.images[img_name[-1]]

        #set current image as active in image editor
        for area in bpy.context.screen.areas :
            if area.type == 'IMAGE_EDITOR' :
                area.spaces.active.image = current_img

        return {'FINISHED'}


class PasteImageToReference(Operator):
    """Load reference image from clipboard"""
    bl_idname = "impaste.paste_ref"
    bl_label = "Paste From Clipboard"

    def execute(self, context):
        img_data = GrabImage()

        if img_data == 0:
            self.report({'ERROR'}, 'No image data on clipboard')
            return {'CANCELLED'}
        elif img_data == 1:
            self.report({'ERROR'}, 'Unable to save image')
            return {'CANCELLED'}
        else:
            img_dir, img_name = img_data

        for directory in img_dir:
            bpy.ops.object.load_reference_image(filepath=directory)

        return {'FINISHED'}


class PasteImageAsPlane(Operator):
    """Load image from clipboard as a plane"""
    bl_idname = "impaste.paste_as_plane"
    bl_label = "Paste From Clipboard as Plane"

    def execute(self, context):
        img_data = GrabImage()

        if img_data == 0:
            self.report({'ERROR'}, 'No image data on clipboard')
            return {'CANCELLED'}
        elif img_data == 1:
            self.report({'ERROR'}, 'Unable to save image')
            return {'CANCELLED'}
        else:
            img_dir, img_name = img_data


        for directory in img_dir:
            name = os.path.basename(directory)
            path = os.path.dirname(directory) + '\\'

            bpy.ops.import_image.to_plane(files=[{"name":name, "name":name}], directory=path, relative = False)

        return {'FINISHED'}


class PasteImageToNodeEditor(Operator):
    """Paste image(s) from clipboard as image texture node(s)"""
    bl_idname = "impaste.paste_as_node"
    bl_label = "Paste Images From Clipboard"

    def execute(self, context):
        img_data = GrabImage()

        if img_data == 0:
            self.report({'ERROR'}, 'No image data on clipboard')
            return {'CANCELLED'}
        elif img_data == 1:
            self.report({'ERROR'}, 'Unable to save image')
            return {'CANCELLED'}
        else:
            img_dir, img_name = img_data


        tree = context.space_data.edit_tree
        locX, locY = context.space_data.cursor_location

        for directory in img_dir:
            node = tree.nodes.new("ShaderNodeTexImage")
            node.location = locX, locY
            locY += 200 # offset location for next node

            node_img = bpy.data.images.load(filepath = directory)
            node.image = node_img

        return {'FINISHED'}


class CopyImageToClipboard(Operator):
    """Copy image to clipboard"""
    bl_idname = "impaste.copy_img"
    bl_label = "Copy To Clipboard"

    def execute(self, context):
        for area in context.screen.areas:
            if area.type == 'IMAGE_EDITOR':
                active_img = area.spaces.active.image

        if active_img.filepath:
            CopyImage(active_img.filepath)

        else:
            if bpy.data.filepath and bpy.context.preferences.addons[__name__].preferences.force_default_dir == False: 
                # save image in the place where the blendfile is saved, in a newly created subfolder (if saved and force_default_directory is set to false)
                Directory = os.path.join(os.path.split(bpy.data.filepath)[0], 'ImagePaste')
        
                if os.path.isdir(Directory) == False:
                    os.mkdir(Directory)

            else:  
                # just use the default location otherwise
                Directory = bpy.context.preferences.addons[__name__].preferences.default_img_dir

            img_dir = Directory + '\\' + active_img.name + '.png'
            bpy.ops.image.save_as(save_as_render=True, copy=True, filepath = img_dir)

            CopyImage(img_dir)

        return {'FINISHED'}
        

# menu functions
def menu_func_ie(self, context):
    self.layout.operator(PasteImageToImageEditor.bl_idname, icon="FILE_IMAGE")
def menu_func_ref(self, context):
    self.layout.operator(PasteImageToReference.bl_idname, icon="FILE_IMAGE")
def menu_func_asplane(self, context):
    self.layout.operator(PasteImageAsPlane.bl_idname, icon="IMAGE_PLANE")
def menu_func_asnode(self, context):
    self.layout.operator(PasteImageToNodeEditor.bl_idname, icon="FILE_IMAGE")
def menu_func_toclipboard(self, context):
    self.layout.operator(CopyImageToClipboard.bl_idname, icon="COPYDOWN")


# list of all classes for registeration/unregistration
classes = (PasteImageToReference, PasteImageAsPlane, PasteImageToImageEditor, ImagePastePreferences, PasteImageToNodeEditor, CopyImageToClipboard)

# store keymaps here to access after registration
addon_keymaps = []


def register():

    # register classes
    for current in classes:
        bpy.utils.register_class(current)

    # register menus
    bpy.types.IMAGE_MT_image.append(menu_func_ie)
    bpy.types.VIEW3D_MT_image_add.append(menu_func_ref)
    bpy.types.VIEW3D_MT_image_add.append(menu_func_asplane)
    bpy.types.NODE_MT_context_menu.append(menu_func_asnode)
    bpy.types.IMAGE_MT_image.append(menu_func_toclipboard)

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

        km = kc.keymaps.new(name='3D View',space_type='VIEW_3D')
        kmi = km.keymap_items.new(PasteImageAsPlane.bl_idname, type='V',value='PRESS',ctrl=True,shift=True,alt=True)
        addon_keymaps.append((km,kmi))

        km = kc.keymaps.new(name='Node Editor',space_type='NODE_EDITOR')
        kmi = km.keymap_items.new(PasteImageToNodeEditor.bl_idname, type='V',value='PRESS',ctrl=True,shift=True)
        addon_keymaps.append((km,kmi))

        km = kc.keymaps.new(name='Image Generic',space_type='IMAGE_EDITOR')
        kmi = km.keymap_items.new(CopyImageToClipboard.bl_idname, type='C',value='PRESS',ctrl=True,shift=True)
        addon_keymaps.append((km,kmi))


def unregister():

    # unregister classes
    for current in classes:
        bpy.utils.unregister_class(current)

    # unregister menus
    bpy.types.IMAGE_MT_image.remove(menu_func_ie)
    bpy.types.VIEW3D_MT_image_add.remove(menu_func_ref)
    bpy.types.VIEW3D_MT_image_add.remove(menu_func_asplane)
    bpy.types.NODE_MT_context_menu.remove(menu_func_asnode)
    bpy.types.IMAGE_MT_image.remvoe(menu_func_toclipboard)

    # unregister keymaps
    for km,kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

if __name__ == "__main__":
    register()
