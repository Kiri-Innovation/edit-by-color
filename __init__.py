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
    "name" : "Edit By Color by KIRI Engine",
    "author" : "Blue Nile 3D", 
    "description" : "Select and edit meshes by colour",
    "blender" : (4, 2, 0),
    "version" : (2, 1, 1),
    "location" : "N-Panel",
    "warning" : "",
    "doc_url": "", 
    "tracker_url": "", 
    "category" : "Mesh" 
}


import bpy
from ._gn_compat import *
import bpy.utils.previews
import os
import bmesh
import webbrowser




def string_to_type(value, to_type, default):
    try:
        value = to_type(value)
    except:
        value = default
    return value


addon_keymaps = {}
_icons = None
ebcfunctionedit_effects = {'sna_tempsubdividemesh': 0, 'sna_templiveeffects': 0, 'sna_tempuvmap': '', 'sna_tempbasetexture': None, 'sna_tempcolourselectionr': 0.0, 'sna_tempcolourselectiong': 0.0, 'sna_tempcolourselectionb': 0.0, 'sna_tempselectiontype': 0, 'sna_tempcolourthreshold': 0.0, 'sna_tempsaturationthreshold': 0.0, 'sna_tempvaluethreshold': 0.0, 'sna_tempgrowshrink': 0, 'sna_tempmasking': 0, 'sna_tempmaskobject': None, 'sna_tempfilterislands': False, 'sna_tempislandthreshold': 0.0, 'sna_tempsetmaterial': None, 'sna_tempsmoothfaces': 0, 'sna_evaluatedfacecount': 0, }
ebcfunctionretopo_loops = {'sna_ebc_temp_store_active_object': None, 'sna_ebc_temp_store_retopo_object': None, }
ebcinterfacefunctions = {'sna_kiri_temp_active_object': None, }
ebctexture = {'sna_ebc_temp_store_active_object': None, 'sna_ebc_temp_store_set_material': None, 'sna_ebc_active_bake_node': None, 'sna_ebc_bake_count': 0, 'sna_ebc_bake_type_list': [], }
ebctexturebake_combined = {'sna_ebc_temp_store_active_object': None, 'sna_ebc_temp_store_base_texture': None, 'sna_ebc_temp_store_set_material': None, 'sna_ebc_active_bake_node': None, 'sna_ebc_bake_count': 0, 'sna_ebc_bake_type_list': [], }
ebctexturebake_patch = {'sna_ebc_temp_store_active_object': None, 'sna_ebc_temp_store_set_material': None, 'sna_ebc_active_bake_node': None, 'sna_ebc_bake_count': 0, 'sna_ebc_bake_type_list': [], }


def sna_update_live_effects_proxy_switch_52B23(self, context):
    sna_updated_prop = self.live_effects_proxy_switch
    kiri_gn_set(bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], 'Socket_48', ((((5 if (sna_updated_prop != 'Smooth and Set Material') else 4) if (sna_updated_prop != 'Set Material') else 3) if (sna_updated_prop != 'Smooth') else 2) if (sna_updated_prop != 'Delete Faces') else 1) if (sna_updated_prop != 'None') else 0)
    bpy.context.active_object.update_tag(refresh={'DATA'}, )
    if bpy.context and bpy.context.screen:
        for a in bpy.context.screen.areas:
            a.tag_redraw()
    if ((sna_updated_prop == 'None') or (sna_updated_prop == 'Delete Faces')):
        bpy.context.scene.sna_ebc_scene_properties.active_menu_full = 'Colour Selection'
        bpy.context.scene.sna_ebc_scene_properties.active_menu_retopo_loops = 'Colour Selection'


def property_exists(prop_path, glob, loc):
    return kiri_gn_property_exists(prop_path, glob, loc)


def load_preview_icon(path):
    global _icons
    if not path in _icons:
        if os.path.exists(path):
            _icons.load(path, path, "IMAGE")
        else:
            return 0
    return _icons[path].icon_id


def sna_active_object_properties_function_interface_3951A(layout_function, ):
    layout_function.label(text='Active Object', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'color-palette.svg')))
    box_E7F59 = layout_function.box()
    box_E7F59.alert = False
    box_E7F59.enabled = True
    box_E7F59.active = True
    box_E7F59.use_property_split = False
    box_E7F59.use_property_decorate = False
    box_E7F59.alignment = 'Expand'.upper()
    box_E7F59.scale_x = 1.0
    box_E7F59.scale_y = 1.0
    if not True: box_E7F59.operator_context = "EXEC_DEFAULT"
    kiri_gn_layout_prop_search(box_E7F59, bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], '["Socket_2"]', bpy.context.view_layer.objects.active.data, 'uv_layers', text='UV Map', icon='NONE')
    kiri_gn_layout_prop_search(box_E7F59, bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], '["Socket_4"]', bpy.data, 'images', text='Base Texture', icon='NONE')
    attr_A311B = '["' + str('Socket_50' + '"]') 
    kiri_gn_layout_prop(box_E7F59, bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], attr_A311B, text='Subdivide Mesh', icon_value=0, emboss=True)
    if (kiri_gn_get(bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], 'Socket_2') == ''):
        box_6329F = layout_function.box()
        box_6329F.alert = (kiri_gn_get(bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], 'Socket_2') == '')
        box_6329F.enabled = True
        box_6329F.active = True
        box_6329F.use_property_split = False
        box_6329F.use_property_decorate = False
        box_6329F.alignment = 'Expand'.upper()
        box_6329F.scale_x = 1.0
        box_6329F.scale_y = 1.0
        if not True: box_6329F.operator_context = "EXEC_DEFAULT"
        box_6329F.label(text='UV Map is required', icon_value=0)
    if (kiri_gn_get(bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], 'Socket_4') == None):
        box_3791C = layout_function.box()
        box_3791C.alert = (kiri_gn_get(bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], 'Socket_4') == None)
        box_3791C.enabled = True
        box_3791C.active = True
        box_3791C.use_property_split = False
        box_3791C.use_property_decorate = False
        box_3791C.alignment = 'Expand'.upper()
        box_3791C.scale_x = 1.0
        box_3791C.scale_y = 1.0
        if not True: box_3791C.operator_context = "EXEC_DEFAULT"
        box_3791C.label(text='Base Texture is required', icon_value=0)


class SNA_OT_Remove_Edit_By_Colour_Modifier_C523D(bpy.types.Operator):
    bl_idname = "sna.remove_edit_by_colour_modifier_c523d"
    bl_label = "Remove Edit By Colour Modifier"
    bl_description = "Removes the Edit By Colour modifier"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        bpy.context.view_layer.objects.active.modifiers.remove(modifier=bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], )
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Add_Edit_By_Colour_Modifier_381C0(bpy.types.Operator):
    bl_idname = "sna.add_edit_by_colour_modifier_381c0"
    bl_label = "Add Edit By Colour Modifier"
    bl_description = "Adds the Edit By Colour modifier to the active object"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        sna_add_edit_by_colour_modifier_function_execute_7A473()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


def sna_add_remove_modifier_function_interface_02DDA(layout_function, ):
    if (bpy.context.mode == 'OBJECT'):
        if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_Edit_By_Colour_GN' in bpy.context.view_layer.objects.active.modifiers):
            grid_4A8AA = layout_function.grid_flow(columns=3, row_major=False, even_columns=False, even_rows=False, align=True)
            grid_4A8AA.enabled = True
            grid_4A8AA.active = True
            grid_4A8AA.use_property_split = False
            grid_4A8AA.use_property_decorate = False
            grid_4A8AA.alignment = 'Expand'.upper()
            grid_4A8AA.scale_x = 1.0
            grid_4A8AA.scale_y = 1.0
            if not True: grid_4A8AA.operator_context = "EXEC_DEFAULT"
            kiri_gn_layout_prop(grid_4A8AA, bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], 'show_viewport', text='', icon_value=0, emboss=True)
            op = grid_4A8AA.operator('sna.remove_edit_by_colour_modifier_c523d', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'trash.svg')), emboss=True, depress=False)
            op = grid_4A8AA.operator('sna.apply_edit_by_colour_modifier_45130', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'check.svg')), emboss=True, depress=False)
        else:
            col_13DC5 = layout_function.column(heading='', align=False)
            col_13DC5.alert = True
            col_13DC5.enabled = True
            col_13DC5.active = True
            col_13DC5.use_property_split = False
            col_13DC5.use_property_decorate = False
            col_13DC5.scale_x = 1.0
            col_13DC5.scale_y = 2.0
            col_13DC5.alignment = 'Expand'.upper()
            col_13DC5.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            op = col_13DC5.operator('sna.add_edit_by_colour_modifier_381c0', text='Add Edit By Colour Modifier', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'plus-circle.svg')), emboss=True, depress=False)
    else:
        layout_function.label(text='Enter Object Mode to add the modifier', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'tips-one.svg')))


def sna_add_edit_by_colour_modifier_function_execute_7A473():
    if (property_exists("bpy.data.node_groups", globals(), locals()) and 'KIRI_Edit_By_Colour_GN' in bpy.data.node_groups):
        pass
    else:
        before_data = list(bpy.data.node_groups)
        bpy.ops.wm.append(directory=os.path.join(os.path.dirname(__file__), 'assets', 'KIRI_Edit_By_Colour_NODE_APPEND.blend') + r'\NodeTree', filename='KIRI_Edit_By_Colour_GN', link=False)
        new_data = list(filter(lambda d: not d in before_data, list(bpy.data.node_groups)))
        appended_EA80E = None if not new_data else new_data[0]
    if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_Edit_By_Colour_GN' in bpy.context.view_layer.objects.active.modifiers):
        pass
    else:
        modifier_13AD0 = bpy.context.view_layer.objects.active.modifiers.new(name='KIRI_Edit_By_Colour_GN', type='NODES', )
    bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'].node_group = bpy.data.node_groups['KIRI_Edit_By_Colour_GN']
    if (property_exists("bpy.data.materials", globals(), locals()) and 'KIRI_LOGO' in bpy.data.materials):
        pass
    else:
        before_data = list(bpy.data.materials)
        bpy.ops.wm.append(directory=os.path.join(os.path.dirname(__file__), 'assets', 'KIRI_Edit_By_Colour_NODE_APPEND.blend') + r'\Material', filename='KIRI_LOGO', link=False)
        new_data = list(filter(lambda d: not d in before_data, list(bpy.data.materials)))
        appended_6FC99 = None if not new_data else new_data[0]
    bpy.context.view_layer.objects.active.sna_ebc_object_properties.live_effects_proxy_switch = 'Set Material'
    kiri_gn_set(bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], 'Socket_26', bpy.data.materials['KIRI_LOGO'])
    if (property_exists("bpy.data.materials", globals(), locals()) and 'Retopo Material' in bpy.data.materials):
        pass
    else:
        before_data = list(bpy.data.materials)
        bpy.ops.wm.append(directory=os.path.join(os.path.dirname(__file__), 'assets', 'KIRI_Edit_By_Colour_NODE_APPEND.blend') + r'\Material', filename='Retopo Material', link=False)
        new_data = list(filter(lambda d: not d in before_data, list(bpy.data.materials)))
        appended_F775F = None if not new_data else new_data[0]
    kiri_gn_set(bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], 'Socket_63', bpy.data.materials['Retopo Material'])
    bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'].show_in_editmode = False
    bpy.context.active_object.update_tag(refresh={'DATA'}, )
    if bpy.context and bpy.context.screen:
        for a in bpy.context.screen.areas:
            a.tag_redraw()


class SNA_OT_Apply_Edit_By_Colour_Modifier_45130(bpy.types.Operator):
    bl_idname = "sna.apply_edit_by_colour_modifier_45130"
    bl_label = "Apply Edit By Colour Modifier"
    bl_description = "Applies the Edit By Colour modifier"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        modifier_name = 'KIRI_Edit_By_Colour_GN'
        object_name = bpy.context.view_layer.objects.active.name
        obj = bpy.data.objects.get(object_name)
        if obj:
            modifier = obj.modifiers.get(modifier_name)
            if modifier:
                if not modifier.show_viewport:
                    # Simply remove the modifier if it's hidden
                    obj.modifiers.remove(modifier)
                    print(f"Removed hidden modifier '{modifier_name}' from object '{object_name}'.")
                else:
                    # Apply normally if visible
                    bpy.ops.object.modifier_apply(modifier=modifier_name)
                    print(f"Applied visible modifier '{modifier_name}' to object '{object_name}'.")
            else:
                print(f"Modifier '{modifier_name}' not found on object '{object_name}'.")
        else:
            print(f"Object '{object_name}' not found.")
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


def sna_adjust_selection_function_interface_541E9(layout_function, ):
    layout_function.label(text='Selection', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'color-palette.svg')))
    box_9F213 = layout_function.box()
    box_9F213.alert = False
    box_9F213.enabled = True
    box_9F213.active = True
    box_9F213.use_property_split = False
    box_9F213.use_property_decorate = False
    box_9F213.alignment = 'Expand'.upper()
    box_9F213.scale_x = 1.0
    box_9F213.scale_y = 1.0
    if not True: box_9F213.operator_context = "EXEC_DEFAULT"
    attr_03B44 = '["' + str('Socket_35' + '"]') 
    kiri_gn_layout_prop(box_9F213, bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], attr_03B44, text='', icon_value=0, emboss=True)
    attr_52066 = '["' + str('Socket_3' + '"]') 
    kiri_gn_layout_prop(box_9F213, bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], attr_52066, text='', icon_value=0, emboss=True)
    if ((kiri_gn_get(bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], 'Socket_35') == 0) or (kiri_gn_get(bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], 'Socket_35') == 1)):
        box_0CA7B = layout_function.box()
        box_0CA7B.alert = False
        box_0CA7B.enabled = True
        box_0CA7B.active = True
        box_0CA7B.use_property_split = False
        box_0CA7B.use_property_decorate = False
        box_0CA7B.alignment = 'Expand'.upper()
        box_0CA7B.scale_x = 1.0
        box_0CA7B.scale_y = 1.0
        if not True: box_0CA7B.operator_context = "EXEC_DEFAULT"
        attr_20E93 = '["' + str('Socket_21' + '"]') 
        kiri_gn_layout_prop(box_0CA7B, bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], attr_20E93, text='Colour Threshold', icon_value=0, emboss=True)
        attr_E51CE = '["' + str('Socket_33' + '"]') 
        kiri_gn_layout_prop(box_0CA7B, bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], attr_E51CE, text='Saturation Threshold', icon_value=0, emboss=True)
        attr_574A7 = '["' + str('Socket_34' + '"]') 
        kiri_gn_layout_prop(box_0CA7B, bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], attr_574A7, text='Value Threshold', icon_value=0, emboss=True)
    box_EC903 = layout_function.box()
    box_EC903.alert = False
    box_EC903.enabled = True
    box_EC903.active = True
    box_EC903.use_property_split = False
    box_EC903.use_property_decorate = False
    box_EC903.alignment = 'Expand'.upper()
    box_EC903.scale_x = 1.0
    box_EC903.scale_y = 1.0
    if not True: box_EC903.operator_context = "EXEC_DEFAULT"
    attr_F9A32 = '["' + str('Socket_44' + '"]') 
    kiri_gn_layout_prop(box_EC903, bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], attr_F9A32, text='Filter Small Islands', icon_value=0, emboss=True, toggle=True)
    if kiri_gn_get(bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], 'Socket_44'):
        attr_55096 = '["' + str('Socket_45' + '"]') 
        kiri_gn_layout_prop(box_EC903, bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], attr_55096, text='Island Threshold', icon_value=0, emboss=True, toggle=True)
    box_6CA41 = layout_function.box()
    box_6CA41.alert = False
    box_6CA41.enabled = True
    box_6CA41.active = True
    box_6CA41.use_property_split = False
    box_6CA41.use_property_decorate = False
    box_6CA41.alignment = 'Expand'.upper()
    box_6CA41.scale_x = 1.0
    box_6CA41.scale_y = 1.0
    if not True: box_6CA41.operator_context = "EXEC_DEFAULT"
    attr_2B70C = '["' + str('Socket_5' + '"]') 
    kiri_gn_layout_prop(box_6CA41, bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], attr_2B70C, text='+ Grow / - Shrink Selection', icon_value=0, emboss=True)
    box_E4145 = layout_function.box()
    box_E4145.alert = False
    box_E4145.enabled = True
    box_E4145.active = True
    box_E4145.use_property_split = False
    box_E4145.use_property_decorate = False
    box_E4145.alignment = 'Expand'.upper()
    box_E4145.scale_x = 1.0
    box_E4145.scale_y = 1.0
    if not True: box_E4145.operator_context = "EXEC_DEFAULT"
    attr_DDF2E = '["' + str('Socket_47' + '"]') 
    kiri_gn_layout_prop(box_E4145, bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], attr_DDF2E, text='', icon_value=0, emboss=True)
    if (kiri_gn_get(bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], 'Socket_47') == 0):
        pass
    else:
        col_12627 = box_E4145.column(heading='', align=False)
        col_12627.alert = False
        col_12627.enabled = True
        col_12627.active = True
        col_12627.use_property_split = False
        col_12627.use_property_decorate = False
        col_12627.scale_x = 1.0
        col_12627.scale_y = 1.0
        col_12627.alignment = 'Expand'.upper()
        col_12627.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        box_945FC = col_12627.box()
        box_945FC.alert = False
        box_945FC.enabled = True
        box_945FC.active = True
        box_945FC.use_property_split = False
        box_945FC.use_property_decorate = False
        box_945FC.alignment = 'Expand'.upper()
        box_945FC.scale_x = 1.0
        box_945FC.scale_y = 1.0
        if not True: box_945FC.operator_context = "EXEC_DEFAULT"
        box_945FC.label(text='Mask Object', icon_value=0)
        attr_7E01F = '["' + str('Socket_36' + '"]') 
        kiri_gn_layout_prop(box_945FC, bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], attr_7E01F, text='', icon_value=0, emboss=True)
        box_1EE16 = col_12627.box()
        box_1EE16.alert = False
        box_1EE16.enabled = True
        box_1EE16.active = True
        box_1EE16.use_property_split = False
        box_1EE16.use_property_decorate = False
        box_1EE16.alignment = 'Expand'.upper()
        box_1EE16.scale_x = 1.0
        box_1EE16.scale_y = 1.0
        if not True: box_1EE16.operator_context = "EXEC_DEFAULT"
        op = box_1EE16.operator('sna.add_wire_cube_24ccd', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'noun-cube-7915485-FFFFFF.svg')), emboss=True, depress=False)
    box_CC1AA = layout_function.box()
    box_CC1AA.alert = False
    box_CC1AA.enabled = True
    box_CC1AA.active = True
    box_CC1AA.use_property_split = False
    box_CC1AA.use_property_decorate = False
    box_CC1AA.alignment = 'Expand'.upper()
    box_CC1AA.scale_x = 1.0
    box_CC1AA.scale_y = 1.0
    if not True: box_CC1AA.operator_context = "EXEC_DEFAULT"
    attr_C9718 = '["' + str('Socket_55' + '"]') 
    kiri_gn_layout_prop(box_CC1AA, bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], attr_C9718, text='Smooth Boundary', icon_value=0, emboss=True, toggle=True)
    if kiri_gn_get(bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], 'Socket_55'):
        attr_91361 = '["' + str('Socket_53' + '"]') 
        kiri_gn_layout_prop(box_CC1AA, bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], attr_91361, text='Smoothing Iterations', icon_value=0, emboss=True, toggle=True)


class SNA_OT_Add_Wire_Cube_24Ccd(bpy.types.Operator):
    bl_idname = "sna.add_wire_cube_24ccd"
    bl_label = "Add wire cube"
    bl_description = "Add a wireframe cube at the 3D cursor location."
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        before_data = list(bpy.data.objects)
        bpy.ops.wm.append(directory=os.path.join(os.path.dirname(__file__), 'assets', 'KIRI_Edit_By_Colour_OBJECT_APPEND.blend') + r'\Object', filename='Wire Cube', link=False)
        new_data = list(filter(lambda d: not d in before_data, list(bpy.data.objects)))
        appended_D8D24 = None if not new_data else new_data[0]
        appended_D8D24.location = bpy.context.scene.cursor.location
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


def sna_edit_effects_function_interface_6C02F(layout_function, ):
    layout_function.label(text='Edit Effects', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'color-palette.svg')))
    box_B7AC1 = layout_function.box()
    box_B7AC1.alert = False
    box_B7AC1.enabled = True
    box_B7AC1.active = True
    box_B7AC1.use_property_split = False
    box_B7AC1.use_property_decorate = False
    box_B7AC1.alignment = 'Expand'.upper()
    box_B7AC1.scale_x = 1.0
    box_B7AC1.scale_y = 1.0
    if not True: box_B7AC1.operator_context = "EXEC_DEFAULT"
    op = box_B7AC1.operator('sna.edit_by_colour__select_77ba8', text='Select', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'mouse-pointer.svg')), emboss=True, depress=False)
    op.sna_apply_subdivision = False
    op.sna_set_live_effects_to = 'None'
    op = box_B7AC1.operator('sna.edit_by_colour__split_819ad', text='Split', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'pause.svg')), emboss=True, depress=False)
    op.sna_apply_subdivision = False
    op.sna_set_live_effects_to = 'None'
    op = box_B7AC1.operator('sna.edit_by_colour__duplicate_f7267', text='Duplicate', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'noun-layer-7392514-FFFFFF.svg')), emboss=True, depress=False)
    op.sna_apply_subdivision = False
    op.sna_set_live_effects_to = 'None'


class SNA_OT_Edit_By_Colour__Select_77Ba8(bpy.types.Operator):
    bl_idname = "sna.edit_by_colour__select_77ba8"
    bl_label = "Edit By Colour - Select"
    bl_description = "Selects faces currently assigned by the Edit By Colour modifier"
    bl_options = {"REGISTER", "UNDO"}
    sna_apply_subdivision: bpy.props.BoolProperty(name='Apply Subdivision?', description='', default=False)

    def sna_set_live_effects_to_enum_items(self, context):
        return [("No Items", "No Items", "No generate enum items node found to create items!", "ERROR", 0)]
    sna_set_live_effects_to: bpy.props.EnumProperty(name='Set Live Effects to:', description='', items=[('None', 'None', '', 0, 0), ('Set Material', 'Set Material', '', 0, 1), ('No Change', 'No Change', '', 0, 2)])

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        sna_ebc_select_function_execute_82A8F(self.sna_apply_subdivision, self.sna_set_live_effects_to)
        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout
        box_8EA7B = layout.box()
        box_8EA7B.alert = False
        box_8EA7B.enabled = True
        box_8EA7B.active = True
        box_8EA7B.use_property_split = False
        box_8EA7B.use_property_decorate = False
        box_8EA7B.alignment = 'Expand'.upper()
        box_8EA7B.scale_x = 1.0
        box_8EA7B.scale_y = 1.0
        if not True: box_8EA7B.operator_context = "EXEC_DEFAULT"
        box_C2E42 = box_8EA7B.box()
        box_C2E42.alert = False
        box_C2E42.enabled = True
        box_C2E42.active = True
        box_C2E42.use_property_split = False
        box_C2E42.use_property_decorate = False
        box_C2E42.alignment = 'Expand'.upper()
        box_C2E42.scale_x = 1.0
        box_C2E42.scale_y = 1.0
        if not True: box_C2E42.operator_context = "EXEC_DEFAULT"
        box_C2E42.label(text='The Edit By Colour modifier will be applied, then re-added', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'tips-one.svg')))
        box_C2E42.label(text='         These effects are destructive', icon_value=0)
        box_8EA7B.label(text='Set Live Effects to:', icon_value=0)
        box_8EA7B.prop(self, 'sna_set_live_effects_to', text='', icon_value=0, emboss=True)
        box_8EA7B.prop(self, 'sna_apply_subdivision', text='Apply Subdivisions', icon_value=0, emboss=True, toggle=False)
        if self.sna_apply_subdivision:
            col_16831 = box_8EA7B.column(heading='', align=False)
            col_16831.alert = False
            col_16831.enabled = True
            col_16831.active = True
            col_16831.use_property_split = False
            col_16831.use_property_decorate = False
            col_16831.scale_x = 1.0
            col_16831.scale_y = 1.0
            col_16831.alignment = 'Expand'.upper()
            col_16831.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            box_DB4E3 = col_16831.box()
            box_DB4E3.alert = False
            box_DB4E3.enabled = True
            box_DB4E3.active = True
            box_DB4E3.use_property_split = False
            box_DB4E3.use_property_decorate = False
            box_DB4E3.alignment = 'Expand'.upper()
            box_DB4E3.scale_x = 1.0
            box_DB4E3.scale_y = 1.0
            if not True: box_DB4E3.operator_context = "EXEC_DEFAULT"
            box_DB4E3.label(text='This act is destructive', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'tips-one.svg')))
            box_DB4E3.label(text='Select will take longer with higher face counts', icon_value=0)
            box_DB4E3.label(text='Other modifiers will not be applied', icon_value=0)
            box_930B3 = col_16831.box()
            box_930B3.alert = False
            box_930B3.enabled = True
            box_930B3.active = True
            box_930B3.use_property_split = False
            box_930B3.use_property_decorate = False
            box_930B3.alignment = 'Expand'.upper()
            box_930B3.scale_x = 1.0
            box_930B3.scale_y = 1.0
            if not True: box_930B3.operator_context = "EXEC_DEFAULT"
            box_930B3.label(text='Base face count =' + ' ' + str(len(bpy.context.view_layer.objects.active.data.polygons)), icon_value=0)
            box_930B3.label(text='Face count with subdivisions + other modifiers =' + ' ' + str(ebcfunctionedit_effects['sna_evaluatedfacecount']), icon_value=0)

    def invoke(self, context, event):
        bm_D9A23 = bmesh.new()
        if bpy.context.view_layer.objects.active:
            if bpy.context.view_layer.objects.active.mode == 'EDIT' and False:
                bm_D9A23 = bmesh.from_edit_mesh(bpy.context.view_layer.objects.active.data)
            else:
                if True:
                    dg = bpy.context.evaluated_depsgraph_get()
                    bm_D9A23.from_mesh(bpy.context.view_layer.objects.active.evaluated_get(dg).to_mesh())
                else:
                    bm_D9A23.from_mesh(bpy.context.view_layer.objects.active.data)
        if False:
            bm_D9A23.transform(bpy.context.view_layer.objects.active.matrix_world)
        bm_D9A23.verts.ensure_lookup_table()
        bm_D9A23.faces.ensure_lookup_table()
        bm_D9A23.edges.ensure_lookup_table()
        ebcfunctionedit_effects['sna_evaluatedfacecount'] = len(bm_D9A23.faces)
        return context.window_manager.invoke_props_dialog(self, width=500)


def sna_ebc_select_function_execute_82A8F(Apply_Subdivision, Set_Effects_To):
    if (property_exists("bpy.context.view_layer.objects.active.data.attributes", globals(), locals()) and 'EBC_Selection' in bpy.context.view_layer.objects.active.data.attributes):
        bpy.context.view_layer.objects.active.data.attributes.remove(attribute=bpy.context.view_layer.objects.active.data.attributes['EBC_Selection'], )
    ebcfunctionedit_effects['sna_templiveeffects'] = kiri_gn_get(bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], 'Socket_48')
    ebcfunctionedit_effects['sna_tempsubdividemesh'] = kiri_gn_get(bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], 'Socket_50')
    ebcfunctionedit_effects['sna_tempuvmap'] = kiri_gn_get(bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], 'Socket_2')
    ebcfunctionedit_effects['sna_tempbasetexture'] = kiri_gn_get(bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], 'Socket_4')
    bpy.context.scene.sna_ebc_scene_properties.colour_selection = kiri_gn_get(bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], 'Socket_3')
    ebcfunctionedit_effects['sna_tempselectiontype'] = string_to_type(kiri_gn_get(bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], 'Socket_35'), int, 0)
    ebcfunctionedit_effects['sna_tempcolourthreshold'] = kiri_gn_get(bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], 'Socket_21')
    ebcfunctionedit_effects['sna_tempsaturationthreshold'] = kiri_gn_get(bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], 'Socket_33')
    ebcfunctionedit_effects['sna_tempvaluethreshold'] = kiri_gn_get(bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], 'Socket_34')
    ebcfunctionedit_effects['sna_tempgrowshrink'] = kiri_gn_get(bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], 'Socket_5')
    ebcfunctionedit_effects['sna_tempmasking'] = string_to_type(kiri_gn_get(bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], 'Socket_47'), int, 0)
    ebcfunctionedit_effects['sna_tempmaskobject'] = kiri_gn_get(bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], 'Socket_36')
    ebcfunctionedit_effects['sna_tempfilterislands'] = kiri_gn_get(bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], 'Socket_44')
    ebcfunctionedit_effects['sna_tempislandthreshold'] = kiri_gn_get(bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], 'Socket_45')
    ebcfunctionedit_effects['sna_tempsetmaterial'] = kiri_gn_get(bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], 'Socket_26')
    ebcfunctionedit_effects['sna_tempsmoothfaces'] = kiri_gn_get(bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], 'Socket_22')
    if Apply_Subdivision:
        pass
    else:
        kiri_gn_set(bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], 'Socket_50', 0)
    kiri_gn_set(bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], 'Socket_48', 0)
    bpy.context.active_object.update_tag(refresh={'DATA'}, )
    if bpy.context and bpy.context.screen:
        for a in bpy.context.screen.areas:
            a.tag_redraw()
    modifier_name = 'KIRI_Edit_By_Colour_GN'
    object_name = bpy.context.view_layer.objects.active.name
    obj = bpy.data.objects.get(object_name)
    if obj:
        modifier = obj.modifiers.get(modifier_name)
        if modifier:
            if not modifier.show_viewport:
                # Simply remove the modifier if it's hidden
                obj.modifiers.remove(modifier)
                print(f"Removed hidden modifier '{modifier_name}' from object '{object_name}'.")
            else:
                # Apply normally if visible
                bpy.ops.object.modifier_apply(modifier=modifier_name)
                print(f"Applied visible modifier '{modifier_name}' to object '{object_name}'.")
        else:
            print(f"Modifier '{modifier_name}' not found on object '{object_name}'.")
    else:
        print(f"Object '{object_name}' not found.")
    sna_add_edit_by_colour_modifier_function_execute_7A473()
    kiri_gn_set(bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], 'Socket_2', ebcfunctionedit_effects['sna_tempuvmap'])
    kiri_gn_set(bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], 'Socket_4', ebcfunctionedit_effects['sna_tempbasetexture'])
    kiri_gn_set(bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], 'Socket_3', bpy.context.scene.sna_ebc_scene_properties.colour_selection)
    kiri_gn_set(bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], 'Socket_35', ebcfunctionedit_effects['sna_tempselectiontype'])
    kiri_gn_set(bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], 'Socket_21', ebcfunctionedit_effects['sna_tempcolourthreshold'])
    kiri_gn_set(bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], 'Socket_33', ebcfunctionedit_effects['sna_tempsaturationthreshold'])
    kiri_gn_set(bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], 'Socket_34', ebcfunctionedit_effects['sna_tempvaluethreshold'])
    kiri_gn_set(bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], 'Socket_5', ebcfunctionedit_effects['sna_tempgrowshrink'])
    kiri_gn_set(bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], 'Socket_47', ebcfunctionedit_effects['sna_tempmasking'])
    kiri_gn_set(bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], 'Socket_36', ebcfunctionedit_effects['sna_tempmaskobject'])
    kiri_gn_set(bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], 'Socket_44', ebcfunctionedit_effects['sna_tempfilterislands'])
    kiri_gn_set(bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], 'Socket_45', ebcfunctionedit_effects['sna_tempislandthreshold'])
    kiri_gn_set(bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], 'Socket_26', ebcfunctionedit_effects['sna_tempsetmaterial'])
    kiri_gn_set(bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], 'Socket_22', ebcfunctionedit_effects['sna_tempsmoothfaces'])
    if Apply_Subdivision:
        kiri_gn_set(bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], 'Socket_50', ebcfunctionedit_effects['sna_tempsubdividemesh'])
    if (Set_Effects_To == 'None'):
        kiri_gn_set(bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], 'Socket_48', 0)
        bpy.context.active_object.update_tag(refresh={'DATA'}, )
        if bpy.context and bpy.context.screen:
            for a in bpy.context.screen.areas:
                a.tag_redraw()
        bpy.context.view_layer.objects.active.sna_ebc_object_properties.live_effects_proxy_switch = Set_Effects_To
    if (Set_Effects_To == 'Set Material'):
        kiri_gn_set(bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], 'Socket_48', 3)
        bpy.context.active_object.update_tag(refresh={'DATA'}, )
        if bpy.context and bpy.context.screen:
            for a in bpy.context.screen.areas:
                a.tag_redraw()
        bpy.context.view_layer.objects.active.sna_ebc_object_properties.live_effects_proxy_switch = Set_Effects_To
    if (Set_Effects_To == 'No Change'):
        kiri_gn_set(bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], 'Socket_48', ebcfunctionedit_effects['sna_templiveeffects'])
        bpy.context.view_layer.objects.active.sna_ebc_object_properties.live_effects_proxy_switch = ((((('Retopo Loops' if (ebcfunctionedit_effects['sna_templiveeffects'] != 4) else 'Smooth and Set Material') if (ebcfunctionedit_effects['sna_templiveeffects'] != 3) else 'Set Material') if (ebcfunctionedit_effects['sna_templiveeffects'] != 2) else 'Smooth') if (ebcfunctionedit_effects['sna_templiveeffects'] != 1) else 'Delete Faces') if (ebcfunctionedit_effects['sna_templiveeffects'] != 0) else 'None')
        bpy.context.active_object.update_tag(refresh={'DATA'}, )
        if bpy.context and bpy.context.screen:
            for a in bpy.context.screen.areas:
                a.tag_redraw()
    bpy.ops.object.mode_set('INVOKE_DEFAULT', mode='EDIT', toggle=False)
    bpy.ops.mesh.select_mode('INVOKE_DEFAULT', type='FACE')
    bpy.ops.mesh.select_all('INVOKE_DEFAULT', action='DESELECT')
    bpy.context.view_layer.objects.active.data.attributes.active = bpy.context.view_layer.objects.active.data.attributes['EBC_Selection']
    bpy.ops.mesh.select_by_attribute('INVOKE_DEFAULT', )


class SNA_OT_Edit_By_Colour__Split_819Ad(bpy.types.Operator):
    bl_idname = "sna.edit_by_colour__split_819ad"
    bl_label = "Edit By Colour - Split"
    bl_description = "Splits faces currently assigned by the Edit By Colour modifier from the current mesh."
    bl_options = {"REGISTER", "UNDO"}
    sna_apply_subdivision: bpy.props.BoolProperty(name='Apply Subdivision?', description='', default=False)

    def sna_set_live_effects_to_enum_items(self, context):
        return [("No Items", "No Items", "No generate enum items node found to create items!", "ERROR", 0)]
    sna_set_live_effects_to: bpy.props.EnumProperty(name='Set Live Effects to:', description='', items=[('None', 'None', '', 0, 0), ('Set Material', 'Set Material', '', 0, 1), ('No Change', 'No Change', '', 0, 2)])

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        sna_ebc_select_function_execute_82A8F(self.sna_apply_subdivision, self.sna_set_live_effects_to)
        bpy.ops.mesh.separate('INVOKE_DEFAULT', type='SELECTED')
        bpy.ops.object.mode_set('INVOKE_DEFAULT', mode='OBJECT', toggle=True)
        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout
        box_7F2D8 = layout.box()
        box_7F2D8.alert = False
        box_7F2D8.enabled = True
        box_7F2D8.active = True
        box_7F2D8.use_property_split = False
        box_7F2D8.use_property_decorate = False
        box_7F2D8.alignment = 'Expand'.upper()
        box_7F2D8.scale_x = 1.0
        box_7F2D8.scale_y = 1.0
        if not True: box_7F2D8.operator_context = "EXEC_DEFAULT"
        box_9AE97 = box_7F2D8.box()
        box_9AE97.alert = False
        box_9AE97.enabled = True
        box_9AE97.active = True
        box_9AE97.use_property_split = False
        box_9AE97.use_property_decorate = False
        box_9AE97.alignment = 'Expand'.upper()
        box_9AE97.scale_x = 1.0
        box_9AE97.scale_y = 1.0
        if not True: box_9AE97.operator_context = "EXEC_DEFAULT"
        box_9AE97.label(text='The Edit By Colour modifier will be applied, then re-added', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'tips-one.svg')))
        box_9AE97.label(text='         These effects are destructive', icon_value=0)
        box_7F2D8.label(text='Set Live Effects to:', icon_value=0)
        box_7F2D8.prop(self, 'sna_set_live_effects_to', text='', icon_value=0, emboss=True)
        box_7F2D8.prop(self, 'sna_apply_subdivision', text='Apply Subdivisions', icon_value=0, emboss=True, toggle=False)
        if self.sna_apply_subdivision:
            col_0AD18 = box_7F2D8.column(heading='', align=False)
            col_0AD18.alert = False
            col_0AD18.enabled = True
            col_0AD18.active = True
            col_0AD18.use_property_split = False
            col_0AD18.use_property_decorate = False
            col_0AD18.scale_x = 1.0
            col_0AD18.scale_y = 1.0
            col_0AD18.alignment = 'Expand'.upper()
            col_0AD18.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            box_91209 = col_0AD18.box()
            box_91209.alert = False
            box_91209.enabled = True
            box_91209.active = True
            box_91209.use_property_split = False
            box_91209.use_property_decorate = False
            box_91209.alignment = 'Expand'.upper()
            box_91209.scale_x = 1.0
            box_91209.scale_y = 1.0
            if not True: box_91209.operator_context = "EXEC_DEFAULT"
            box_91209.label(text='This act is destructive', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'tips-one.svg')))
            box_91209.label(text='Select will take longer with higher face counts', icon_value=0)
            box_91209.label(text='Other modifiers will not be applied', icon_value=0)
            box_AA5B1 = col_0AD18.box()
            box_AA5B1.alert = False
            box_AA5B1.enabled = True
            box_AA5B1.active = True
            box_AA5B1.use_property_split = False
            box_AA5B1.use_property_decorate = False
            box_AA5B1.alignment = 'Expand'.upper()
            box_AA5B1.scale_x = 1.0
            box_AA5B1.scale_y = 1.0
            if not True: box_AA5B1.operator_context = "EXEC_DEFAULT"
            box_AA5B1.label(text='Base face count =' + ' ' + str(len(bpy.context.view_layer.objects.active.data.polygons)), icon_value=0)
            box_AA5B1.label(text='Face count with subdivisions + other modifiers =' + ' ' + str(ebcfunctionedit_effects['sna_evaluatedfacecount']), icon_value=0)

    def invoke(self, context, event):
        bm_75D99 = bmesh.new()
        if bpy.context.view_layer.objects.active:
            if bpy.context.view_layer.objects.active.mode == 'EDIT' and False:
                bm_75D99 = bmesh.from_edit_mesh(bpy.context.view_layer.objects.active.data)
            else:
                if True:
                    dg = bpy.context.evaluated_depsgraph_get()
                    bm_75D99.from_mesh(bpy.context.view_layer.objects.active.evaluated_get(dg).to_mesh())
                else:
                    bm_75D99.from_mesh(bpy.context.view_layer.objects.active.data)
        if False:
            bm_75D99.transform(bpy.context.view_layer.objects.active.matrix_world)
        bm_75D99.verts.ensure_lookup_table()
        bm_75D99.faces.ensure_lookup_table()
        bm_75D99.edges.ensure_lookup_table()
        ebcfunctionedit_effects['sna_evaluatedfacecount'] = len(bm_75D99.faces)
        return context.window_manager.invoke_props_dialog(self, width=500)


class SNA_OT_Edit_By_Colour__Duplicate_F7267(bpy.types.Operator):
    bl_idname = "sna.edit_by_colour__duplicate_f7267"
    bl_label = "Edit By Colour - Duplicate"
    bl_description = "Dupliates faces currently assigned by the Edit By Colour modifier and leaves the original mesh intact."
    bl_options = {"REGISTER", "UNDO"}
    sna_apply_subdivision: bpy.props.BoolProperty(name='Apply Subdivision?', description='', default=False)

    def sna_set_live_effects_to_enum_items(self, context):
        return [("No Items", "No Items", "No generate enum items node found to create items!", "ERROR", 0)]
    sna_set_live_effects_to: bpy.props.EnumProperty(name='Set Live Effects to:', description='', items=[('None', 'None', '', 0, 0), ('Set Material', 'Set Material', '', 0, 1), ('No Change', 'No Change', '', 0, 2)])

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        sna_ebc_select_function_execute_82A8F(self.sna_apply_subdivision, self.sna_set_live_effects_to)
        # Get the active object
        obj = bpy.context.active_object
        # Store the selected faces' indices
        selected_faces = [f.index for f in obj.data.polygons if f.select]
        # Duplicate the selected faces
        bpy.ops.mesh.duplicate()
        # Separate the duplicated faces
        bpy.ops.mesh.separate(type='SELECTED')
        # Switch to object mode
        bpy.ops.object.mode_set(mode='OBJECT')
        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout
        box_10D06 = layout.box()
        box_10D06.alert = False
        box_10D06.enabled = True
        box_10D06.active = True
        box_10D06.use_property_split = False
        box_10D06.use_property_decorate = False
        box_10D06.alignment = 'Expand'.upper()
        box_10D06.scale_x = 1.0
        box_10D06.scale_y = 1.0
        if not True: box_10D06.operator_context = "EXEC_DEFAULT"
        box_77480 = box_10D06.box()
        box_77480.alert = False
        box_77480.enabled = True
        box_77480.active = True
        box_77480.use_property_split = False
        box_77480.use_property_decorate = False
        box_77480.alignment = 'Expand'.upper()
        box_77480.scale_x = 1.0
        box_77480.scale_y = 1.0
        if not True: box_77480.operator_context = "EXEC_DEFAULT"
        box_77480.label(text='The Edit By Colour modifier will be applied, then re-added', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'tips-one.svg')))
        box_77480.label(text='         These effects are destructive', icon_value=0)
        box_10D06.label(text='Set Live Effects to:', icon_value=0)
        box_10D06.prop(self, 'sna_set_live_effects_to', text='', icon_value=0, emboss=True)
        box_10D06.prop(self, 'sna_apply_subdivision', text='Apply Subdivisions', icon_value=0, emboss=True, toggle=False)
        if self.sna_apply_subdivision:
            col_A5DE0 = box_10D06.column(heading='', align=False)
            col_A5DE0.alert = False
            col_A5DE0.enabled = True
            col_A5DE0.active = True
            col_A5DE0.use_property_split = False
            col_A5DE0.use_property_decorate = False
            col_A5DE0.scale_x = 1.0
            col_A5DE0.scale_y = 1.0
            col_A5DE0.alignment = 'Expand'.upper()
            col_A5DE0.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            box_7FC90 = col_A5DE0.box()
            box_7FC90.alert = False
            box_7FC90.enabled = True
            box_7FC90.active = True
            box_7FC90.use_property_split = False
            box_7FC90.use_property_decorate = False
            box_7FC90.alignment = 'Expand'.upper()
            box_7FC90.scale_x = 1.0
            box_7FC90.scale_y = 1.0
            if not True: box_7FC90.operator_context = "EXEC_DEFAULT"
            box_7FC90.label(text='This act is destructive', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'tips-one.svg')))
            box_7FC90.label(text='Select will take longer with higher face counts', icon_value=0)
            box_7FC90.label(text='Other modifiers will not be applied', icon_value=0)
            box_ABABF = col_A5DE0.box()
            box_ABABF.alert = False
            box_ABABF.enabled = True
            box_ABABF.active = True
            box_ABABF.use_property_split = False
            box_ABABF.use_property_decorate = False
            box_ABABF.alignment = 'Expand'.upper()
            box_ABABF.scale_x = 1.0
            box_ABABF.scale_y = 1.0
            if not True: box_ABABF.operator_context = "EXEC_DEFAULT"
            box_ABABF.label(text='Base face count =' + ' ' + str(len(bpy.context.view_layer.objects.active.data.polygons)), icon_value=0)
            box_ABABF.label(text='Face count with subdivisions + other modifiers =' + ' ' + str(ebcfunctionedit_effects['sna_evaluatedfacecount']), icon_value=0)

    def invoke(self, context, event):
        bm_A0AA9 = bmesh.new()
        if bpy.context.view_layer.objects.active:
            if bpy.context.view_layer.objects.active.mode == 'EDIT' and False:
                bm_A0AA9 = bmesh.from_edit_mesh(bpy.context.view_layer.objects.active.data)
            else:
                if True:
                    dg = bpy.context.evaluated_depsgraph_get()
                    bm_A0AA9.from_mesh(bpy.context.view_layer.objects.active.evaluated_get(dg).to_mesh())
                else:
                    bm_A0AA9.from_mesh(bpy.context.view_layer.objects.active.data)
        if False:
            bm_A0AA9.transform(bpy.context.view_layer.objects.active.matrix_world)
        bm_A0AA9.verts.ensure_lookup_table()
        bm_A0AA9.faces.ensure_lookup_table()
        bm_A0AA9.edges.ensure_lookup_table()
        ebcfunctionedit_effects['sna_evaluatedfacecount'] = len(bm_A0AA9.faces)
        return context.window_manager.invoke_props_dialog(self, width=500)


def sna_live_effects_function_interface_5A08A(layout_function, ):
    layout_function.label(text='Live Effects', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'color-palette.svg')))
    box_F7F47 = layout_function.box()
    box_F7F47.alert = True
    box_F7F47.enabled = True
    box_F7F47.active = True
    box_F7F47.use_property_split = False
    box_F7F47.use_property_decorate = False
    box_F7F47.alignment = 'Expand'.upper()
    box_F7F47.scale_x = 1.0
    box_F7F47.scale_y = 1.0
    if not True: box_F7F47.operator_context = "EXEC_DEFAULT"
    box_F7F47.prop(bpy.context.view_layer.objects.active.sna_ebc_object_properties, 'live_effects_proxy_switch', text='', icon_value=0, emboss=True)
    if ((kiri_gn_get(bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], 'Socket_48') == 0) or (kiri_gn_get(bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], 'Socket_48') == 1)):
        pass
    else:
        col_6723E = box_F7F47.column(heading='', align=False)
        col_6723E.alert = False
        col_6723E.enabled = True
        col_6723E.active = True
        col_6723E.use_property_split = False
        col_6723E.use_property_decorate = False
        col_6723E.scale_x = 1.0
        col_6723E.scale_y = 1.0
        col_6723E.alignment = 'Expand'.upper()
        col_6723E.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        if ((kiri_gn_get(bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], 'Socket_48') == 2) or (kiri_gn_get(bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], 'Socket_48') == 4)):
            attr_DAD0F = '["' + str('Socket_22' + '"]') 
            kiri_gn_layout_prop(col_6723E, bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], attr_DAD0F, text='Smooth Iterations', icon_value=0, emboss=True)
        if ((kiri_gn_get(bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], 'Socket_48') == 3) or (kiri_gn_get(bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], 'Socket_48') == 4)):
            col_A135B = col_6723E.column(heading='', align=False)
            col_A135B.alert = False
            col_A135B.enabled = True
            col_A135B.active = True
            col_A135B.use_property_split = False
            col_A135B.use_property_decorate = False
            col_A135B.scale_x = 1.0
            col_A135B.scale_y = 1.0
            col_A135B.alignment = 'Expand'.upper()
            col_A135B.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            kiri_gn_layout_prop_search(col_A135B, bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], '["Socket_26"]', bpy.data, 'materials', text='Material', icon='NONE')


def sna_retopo_loops_function_interface_61CF5(layout_function, ):
    layout_function.label(text='Retopo Loops', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'color-palette.svg')))
    box_BA276 = layout_function.box()
    box_BA276.alert = False
    box_BA276.enabled = True
    box_BA276.active = True
    box_BA276.use_property_split = False
    box_BA276.use_property_decorate = False
    box_BA276.alignment = 'Expand'.upper()
    box_BA276.scale_x = 1.0
    box_BA276.scale_y = 1.0
    if not True: box_BA276.operator_context = "EXEC_DEFAULT"
    box_BA276.label(text='Adjust', icon_value=0)
    kiri_gn_layout_prop_search(box_BA276, bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], '["Socket_63"]', bpy.data, 'materials', text='Material', icon='NONE')
    attr_A89E4 = '["' + str('Socket_62' + '"]') 
    kiri_gn_layout_prop(box_BA276, bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], attr_A89E4, text='Preview With Base', icon_value=0, emboss=True, toggle=True)
    attr_0282E = '["' + str('Socket_57' + '"]') 
    kiri_gn_layout_prop(box_BA276, bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], attr_0282E, text='Loop Resolution', icon_value=0, emboss=True, toggle=True)
    attr_14B05 = '["' + str('Socket_66' + '"]') 
    kiri_gn_layout_prop(box_BA276, bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], attr_14B05, text='Smooth Loops', icon_value=0, emboss=True)
    attr_277B1 = '["' + str('Socket_58' + '"]') 
    kiri_gn_layout_prop(box_BA276, bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], attr_277B1, text='Loop Width', icon_value=0, emboss=True)
    attr_AAB84 = '["' + str('Socket_61' + '"]') 
    kiri_gn_layout_prop(box_BA276, bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], attr_AAB84, text='Surface Offset', icon_value=0, emboss=True)
    attr_A49F0 = '["' + str('Socket_60' + '"]') 
    kiri_gn_layout_prop(box_BA276, bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], attr_A49F0, text='Shrinkwrap', icon_value=0, emboss=True, toggle=True)
    box_8D5ED = box_BA276.box()
    box_8D5ED.alert = False
    box_8D5ED.enabled = True
    box_8D5ED.active = True
    box_8D5ED.use_property_split = False
    box_8D5ED.use_property_decorate = False
    box_8D5ED.alignment = 'Expand'.upper()
    box_8D5ED.scale_x = 1.0
    box_8D5ED.scale_y = 1.0
    if not True: box_8D5ED.operator_context = "EXEC_DEFAULT"
    box_8D5ED.label(text='Clean Up', icon_value=0)
    attr_942EF = '["' + str('Socket_64' + '"]') 
    kiri_gn_layout_prop(box_8D5ED, bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], attr_942EF, text='Preview Curve', icon_value=0, emboss=True, toggle=True)
    attr_E6119 = '["' + str('Socket_65' + '"]') 
    kiri_gn_layout_prop(box_8D5ED, bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], attr_E6119, text='Remove Shorter Than:', icon_value=0, emboss=True)
    box_408A8 = box_BA276.box()
    box_408A8.alert = False
    box_408A8.enabled = True
    box_408A8.active = True
    box_408A8.use_property_split = False
    box_408A8.use_property_decorate = False
    box_408A8.alignment = 'Expand'.upper()
    box_408A8.scale_x = 1.0
    box_408A8.scale_y = 1.0
    if not True: box_408A8.operator_context = "EXEC_DEFAULT"
    op = box_408A8.operator('sna.apply_retopo_loops_7ea68', text='Apply Loops', icon_value=0, emboss=True, depress=False)
    op.sna_set_originals_effects = 'Set Material'
    op.sna_add_shrinkwrap_and_subdiv = True


class SNA_OT_Apply_Retopo_Loops_7Ea68(bpy.types.Operator):
    bl_idname = "sna.apply_retopo_loops_7ea68"
    bl_label = "Apply Retopo Loops"
    bl_description = "Applies the retopology loops as a new object."
    bl_options = {"REGISTER", "UNDO"}

    def sna_set_originals_effects_enum_items(self, context):
        return [("No Items", "No Items", "No generate enum items node found to create items!", "ERROR", 0)]
    sna_set_originals_effects: bpy.props.EnumProperty(name='Set Originals Effects', description='', items=[('Set Material', 'Set Material', '', 0, 0), ('Retopo Loops', 'Retopo Loops', '', 0, 1), ('None', 'None', '', 0, 2)])
    sna_add_shrinkwrap_and_subdiv: bpy.props.BoolProperty(name='Add Shrinkwrap and Subdiv', description='', default=True)

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        ebcfunctionretopo_loops['sna_ebc_temp_store_active_object'] = bpy.context.view_layer.objects.active
        source_obj_name = bpy.context.view_layer.objects.active.name
        offset_x = 0.0
        new_object_name = None
        # Input variables
        #source_obj_name = "Cube"  # Change this to your object's name
        #offset_x = 0.0  # Input float variable for X offset
        # Get the source object
        source_obj = bpy.data.objects.get(source_obj_name)
        # Check if the object exists
        if source_obj:
            # Create a copy of the object
            new_obj = source_obj.copy()
            new_obj.data = source_obj.data.copy()
            # Link the new object to the scene
            bpy.context.scene.collection.objects.link(new_obj)
            # Apply the offset if any
            new_obj.location.x += offset_x
            # Store the new object's name in a variable
            new_object_name = new_obj.name
        else:
            new_object_name = "ERROR: Source object not found"
        # Output the new object's name (this will be captured by Serpens)
        print(new_object_name)
        ebcfunctionretopo_loops['sna_ebc_temp_store_retopo_object'] = bpy.data.objects[new_object_name]
        kiri_gn_set(ebcfunctionretopo_loops['sna_ebc_temp_store_retopo_object'].modifiers['KIRI_Edit_By_Colour_GN'], 'Socket_62', False)
        kiri_gn_set(ebcfunctionretopo_loops['sna_ebc_temp_store_retopo_object'].modifiers['KIRI_Edit_By_Colour_GN'], 'Socket_64', False)
        kiri_gn_set(ebcfunctionretopo_loops['sna_ebc_temp_store_active_object'].modifiers['KIRI_Edit_By_Colour_GN'], 'Socket_48', (5 if (self.sna_set_originals_effects != 'None') else 0) if (self.sna_set_originals_effects != 'Set Material') else 3)
        bpy.context.view_layer.objects.active.sna_ebc_object_properties.live_effects_proxy_switch = self.sna_set_originals_effects
        ebcfunctionretopo_loops['sna_ebc_temp_store_active_object'].update_tag(refresh={'DATA'}, )
        if bpy.context and bpy.context.screen:
            for a in bpy.context.screen.areas:
                a.tag_redraw()
        ebcfunctionretopo_loops['sna_ebc_temp_store_retopo_object'].update_tag(refresh={'DATA'}, )
        if bpy.context and bpy.context.screen:
            for a in bpy.context.screen.areas:
                a.tag_redraw()
        for i_CD250 in range(len(bpy.context.scene.objects)):
            bpy.context.scene.objects[i_CD250].select_set(state=False, view_layer=bpy.context.view_layer, )
        ebcfunctionretopo_loops['sna_ebc_temp_store_retopo_object'].select_set(state=True, view_layer=bpy.context.view_layer, )
        bpy.context.view_layer.objects.active = ebcfunctionretopo_loops['sna_ebc_temp_store_retopo_object']
        bpy.ops.object.modifier_apply('INVOKE_DEFAULT', modifier='KIRI_Edit_By_Colour_GN')
        if self.sna_add_shrinkwrap_and_subdiv:
            modifier_8FCC1 = bpy.context.view_layer.objects.active.modifiers.new(name='EBC Subdiv', type='SUBSURF', )
            modifier_63518 = bpy.context.view_layer.objects.active.modifiers.new(name='EBC Shrinkwrap', type='SHRINKWRAP', )
            modifier_63518.target = ebcfunctionretopo_loops['sna_ebc_temp_store_active_object']
        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout
        box_F96AC = layout.box()
        box_F96AC.alert = False
        box_F96AC.enabled = True
        box_F96AC.active = True
        box_F96AC.use_property_split = False
        box_F96AC.use_property_decorate = False
        box_F96AC.alignment = 'Expand'.upper()
        box_F96AC.scale_x = 1.0
        box_F96AC.scale_y = 1.0
        if not True: box_F96AC.operator_context = "EXEC_DEFAULT"
        box_F96AC.label(text='Apply Loops Settings', icon_value=0)
        box_F96AC.label(text="Set Original's Effects To:", icon_value=0)
        box_F96AC.prop(self, 'sna_set_originals_effects', text='', icon_value=0, emboss=True)
        box_F96AC.prop(self, 'sna_add_shrinkwrap_and_subdiv', text='Add Shrinkwrap and Subdiv', icon_value=0, emboss=True)

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=500)


def sna_sculpt_function_interface_92592(layout_function, ):
    layout_function.label(text='Sculpt', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'color-palette.svg')))
    box_21A98 = layout_function.box()
    box_21A98.alert = False
    box_21A98.enabled = True
    box_21A98.active = True
    box_21A98.use_property_split = False
    box_21A98.use_property_decorate = False
    box_21A98.alignment = 'Expand'.upper()
    box_21A98.scale_x = 1.0
    box_21A98.scale_y = 1.0
    if not True: box_21A98.operator_context = "EXEC_DEFAULT"
    if 'OBJECT'==bpy.context.mode:
        op = box_21A98.operator('sna.selection_to_face_sets_69a50', text='Selection to Face Sets', icon_value=0, emboss=True, depress=False)
        op.sna_apply_subdivision = False
        op.sna_set_live_effects_to = 'None'
    if (bpy.context.mode == 'SCULPT'):
        col_CC812 = box_21A98.column(heading='', align=False)
        col_CC812.alert = False
        col_CC812.enabled = True
        col_CC812.active = True
        col_CC812.use_property_split = False
        col_CC812.use_property_decorate = False
        col_CC812.scale_x = 1.0
        col_CC812.scale_y = 1.0
        col_CC812.alignment = 'Expand'.upper()
        col_CC812.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_CC812.prop(kiri_sculpt_automasking_settings(bpy.context.scene.tool_settings.sculpt), 'use_automasking_face_sets', text='Auto Mask By Face Sets', icon_value=0, emboss=True, toggle=True)
        op = col_CC812.operator('sculpt.face_sets_create', text='Face Set From Visible (Clear)', icon_value=0, emboss=True, depress=False)
        op.mode = 'VISIBLE'
        box_98238 = col_CC812.box()
        box_98238.alert = False
        box_98238.enabled = True
        box_98238.active = True
        box_98238.use_property_split = False
        box_98238.use_property_decorate = False
        box_98238.alignment = 'Expand'.upper()
        box_98238.scale_x = 1.0
        box_98238.scale_y = 1.0
        if not True: box_98238.operator_context = "EXEC_DEFAULT"
        box_98238.label(text='Grow Face Set = Ctrl + W', icon_value=0)
        box_98238.label(text='Shrink Face Set = Ctrl + Alt + W', icon_value=0)


class SNA_OT_Selection_To_Face_Sets_69A50(bpy.types.Operator):
    bl_idname = "sna.selection_to_face_sets_69a50"
    bl_label = "Selection to Face Sets"
    bl_description = "Enters sculpting mode and creates Face Sets based on the Edit By Colour selection."
    bl_options = {"REGISTER", "UNDO"}
    sna_apply_subdivision: bpy.props.BoolProperty(name='Apply Subdivision?', description='', default=False)

    def sna_set_live_effects_to_enum_items(self, context):
        return [("No Items", "No Items", "No generate enum items node found to create items!", "ERROR", 0)]
    sna_set_live_effects_to: bpy.props.EnumProperty(name='Set Live Effects to', description='', items=[('None', 'None', '', 0, 0), ('Set Material', 'Set Material', '', 0, 1), ('No Change', 'No Change', '', 0, 2)])

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        shade_mode = 'SOLID'  # Options: 'SOLID', 'RENDERED', 'MATERIAL', 'WIREFRAME'
        # Loop through all screens
        for screen in bpy.data.screens:
            # Loop through all areas in each screen
            for area in screen.areas:
                # Check if the area is a 3D View
                if area.type == 'VIEW_3D':
                    # Get the 3D viewport's shading settings
                    space = area.spaces[0]
                    # Set the shading type
                    space.shading.type = shade_mode
        sna_ebc_select_function_execute_82A8F(self.sna_apply_subdivision, self.sna_set_live_effects_to)
        bpy.ops.object.mode_set('INVOKE_DEFAULT', mode='SCULPT')
        bpy.ops.sculpt.face_sets_create('INVOKE_DEFAULT', mode='SELECTION')
        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout
        box_C5083 = layout.box()
        box_C5083.alert = False
        box_C5083.enabled = True
        box_C5083.active = True
        box_C5083.use_property_split = False
        box_C5083.use_property_decorate = False
        box_C5083.alignment = 'Expand'.upper()
        box_C5083.scale_x = 1.0
        box_C5083.scale_y = 1.0
        if not True: box_C5083.operator_context = "EXEC_DEFAULT"
        box_78E53 = box_C5083.box()
        box_78E53.alert = False
        box_78E53.enabled = True
        box_78E53.active = True
        box_78E53.use_property_split = False
        box_78E53.use_property_decorate = False
        box_78E53.alignment = 'Expand'.upper()
        box_78E53.scale_x = 1.0
        box_78E53.scale_y = 1.0
        if not True: box_78E53.operator_context = "EXEC_DEFAULT"
        box_78E53.label(text='The Edit By Colour modifier will be applied, then re-added', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'tips-one.svg')))
        box_78E53.label(text='         These effects are destructive', icon_value=0)
        box_C5083.label(text='Set Live Effects to:', icon_value=0)
        box_C5083.prop(self, 'sna_set_live_effects_to', text='', icon_value=0, emboss=True)
        box_C5083.prop(self, 'sna_apply_subdivision', text='Apply Subdivisions', icon_value=0, emboss=True, toggle=False)
        if self.sna_apply_subdivision:
            col_68F58 = box_C5083.column(heading='', align=False)
            col_68F58.alert = False
            col_68F58.enabled = True
            col_68F58.active = True
            col_68F58.use_property_split = False
            col_68F58.use_property_decorate = False
            col_68F58.scale_x = 1.0
            col_68F58.scale_y = 1.0
            col_68F58.alignment = 'Expand'.upper()
            col_68F58.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            box_8B5B8 = col_68F58.box()
            box_8B5B8.alert = False
            box_8B5B8.enabled = True
            box_8B5B8.active = True
            box_8B5B8.use_property_split = False
            box_8B5B8.use_property_decorate = False
            box_8B5B8.alignment = 'Expand'.upper()
            box_8B5B8.scale_x = 1.0
            box_8B5B8.scale_y = 1.0
            if not True: box_8B5B8.operator_context = "EXEC_DEFAULT"
            box_8B5B8.label(text='This act is destructive', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'tips-one.svg')))
            box_8B5B8.label(text='Select will take longer with higher face counts', icon_value=0)
            box_8B5B8.label(text='Other modifiers will not be applied', icon_value=0)
            box_7A6F5 = col_68F58.box()
            box_7A6F5.alert = False
            box_7A6F5.enabled = True
            box_7A6F5.active = True
            box_7A6F5.use_property_split = False
            box_7A6F5.use_property_decorate = False
            box_7A6F5.alignment = 'Expand'.upper()
            box_7A6F5.scale_x = 1.0
            box_7A6F5.scale_y = 1.0
            if not True: box_7A6F5.operator_context = "EXEC_DEFAULT"
            box_7A6F5.label(text='Base face count =' + ' ' + str(len(bpy.context.view_layer.objects.active.data.polygons)), icon_value=0)
            box_7A6F5.label(text='Face count with subdivisions + other modifiers =' + ' ' + str(ebcfunctionedit_effects['sna_evaluatedfacecount']), icon_value=0)

    def invoke(self, context, event):
        bm_3B63D = bmesh.new()
        if bpy.context.view_layer.objects.active:
            if bpy.context.view_layer.objects.active.mode == 'EDIT' and False:
                bm_3B63D = bmesh.from_edit_mesh(bpy.context.view_layer.objects.active.data)
            else:
                if True:
                    dg = bpy.context.evaluated_depsgraph_get()
                    bm_3B63D.from_mesh(bpy.context.view_layer.objects.active.evaluated_get(dg).to_mesh())
                else:
                    bm_3B63D.from_mesh(bpy.context.view_layer.objects.active.data)
        if False:
            bm_3B63D.transform(bpy.context.view_layer.objects.active.matrix_world)
        bm_3B63D.verts.ensure_lookup_table()
        bm_3B63D.faces.ensure_lookup_table()
        bm_3B63D.edges.ensure_lookup_table()
        ebcfunctionedit_effects['sna_evaluatedfacecount'] = len(bm_3B63D.faces)
        return context.window_manager.invoke_props_dialog(self, width=500)


class SNA_PT_EDIT_BY_COLOUR_BY_KIRI_ENGINE_2BDB2(bpy.types.Panel):
    bl_label = 'Edit By Colour by KIRI Engine'
    bl_idname = 'SNA_PT_EDIT_BY_COLOUR_BY_KIRI_ENGINE_2BDB2'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = ''
    bl_category = 'Edit By Colour'
    bl_order = 0
    bl_ui_units_x=0

    @classmethod
    def poll(cls, context):
        return not (False)

    def draw_header(self, context):
        layout = self.layout
        layout.template_icon(icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'kiriengine icon.png')), scale=0.0)

    def draw(self, context):
        layout = self.layout
        layout_function = layout
        sna_edit_by_colour_functions_function_interface_7277A(layout_function, )
        layout_function = layout
        sna_external_links_menu_8E1B8(layout_function, )


def sna_external_links_menu_8E1B8(layout_function, ):
    box_DD590 = layout_function.box()
    box_DD590.alert = False
    box_DD590.enabled = True
    box_DD590.active = True
    box_DD590.use_property_split = False
    box_DD590.use_property_decorate = False
    box_DD590.alignment = 'Expand'.upper()
    box_DD590.scale_x = 1.0
    box_DD590.scale_y = 1.0
    if not True: box_DD590.operator_context = "EXEC_DEFAULT"
    col_7EB57 = box_DD590.column(heading='', align=True)
    col_7EB57.alert = False
    col_7EB57.enabled = True
    col_7EB57.active = True
    col_7EB57.use_property_split = False
    col_7EB57.use_property_decorate = False
    col_7EB57.scale_x = 1.0
    col_7EB57.scale_y = 1.0
    col_7EB57.alignment = 'Expand'.upper()
    col_7EB57.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    box_8183E = col_7EB57.box()
    box_8183E.alert = False
    box_8183E.enabled = True
    box_8183E.active = True
    box_8183E.use_property_split = False
    box_8183E.use_property_decorate = False
    box_8183E.alignment = 'Center'.upper()
    box_8183E.scale_x = 1.0
    box_8183E.scale_y = 1.0
    if not True: box_8183E.operator_context = "EXEC_DEFAULT"
    box_8183E.label(text='About KIRI Engine', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'color-palette.svg')))
    box_8183E.template_icon(icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'Addon speel 2.png')), scale=10.0)
    op = box_8183E.operator('sna.dgs_render_launch_kiri_site_84772', text='Learn More', icon_value=0, emboss=True, depress=False)
    box_63F09 = col_7EB57.box()
    box_63F09.alert = False
    box_63F09.enabled = True
    box_63F09.active = True
    box_63F09.use_property_split = False
    box_63F09.use_property_decorate = True
    box_63F09.alignment = 'Expand'.upper()
    box_63F09.scale_x = 1.0
    box_63F09.scale_y = 1.2000000476837158
    if not True: box_63F09.operator_context = "EXEC_DEFAULT"
    row_786FB = box_63F09.row(heading='', align=True)
    row_786FB.alert = False
    row_786FB.enabled = True
    row_786FB.active = True
    row_786FB.use_property_split = False
    row_786FB.use_property_decorate = False
    row_786FB.scale_x = 1.0
    row_786FB.scale_y = 1.0
    row_786FB.alignment = 'Expand'.upper()
    row_786FB.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    row_786FB.label(text='Documentation', icon_value=0)
    split_7852F = row_786FB.split(factor=0.30000001192092896, align=True)
    split_7852F.alert = False
    split_7852F.enabled = True
    split_7852F.active = True
    split_7852F.use_property_split = False
    split_7852F.use_property_decorate = False
    split_7852F.scale_x = 1.0
    split_7852F.scale_y = 1.0
    split_7852F.alignment = 'Expand'.upper()
    if not True: split_7852F.operator_context = "EXEC_DEFAULT"
    op = split_7852F.operator('sna.dgs_render_open_documentation_3b870', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'documentation.svg')), emboss=True, depress=False)
    op = split_7852F.operator('sna.dgs_render_open_tutorial_video_d0cd5', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'video.svg')), emboss=True, depress=False)
    box_C5949 = col_7EB57.box()
    box_C5949.alert = False
    box_C5949.enabled = True
    box_C5949.active = True
    box_C5949.use_property_split = False
    box_C5949.use_property_decorate = False
    box_C5949.alignment = 'Expand'.upper()
    box_C5949.scale_x = 1.0
    box_C5949.scale_y = 1.0
    if not True: box_C5949.operator_context = "EXEC_DEFAULT"
    row_7C27F = box_C5949.row(heading='', align=False)
    row_7C27F.alert = False
    row_7C27F.enabled = True
    row_7C27F.active = True
    row_7C27F.use_property_split = False
    row_7C27F.use_property_decorate = False
    row_7C27F.scale_x = 1.0
    row_7C27F.scale_y = 1.2000000476837158
    row_7C27F.alignment = 'Expand'.upper()
    row_7C27F.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    row_7C27F.label(text='Get More Addons', icon_value=0)
    split_57202 = row_7C27F.split(factor=0.5, align=True)
    split_57202.alert = False
    split_57202.enabled = True
    split_57202.active = True
    split_57202.use_property_split = False
    split_57202.use_property_decorate = False
    split_57202.scale_x = 1.0
    split_57202.scale_y = 1.0
    split_57202.alignment = 'Expand'.upper()
    if not True: split_57202.operator_context = "EXEC_DEFAULT"
    op = split_57202.operator('sna.dgs_render_launch_superhive_store_0bcb5', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'SuperHive Logo White.png')), emboss=True, depress=False)
    op = split_57202.operator('sna.dgs_render_launch_kiri_blender_addons_page_9427f', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'kiriengine blender addon icon color.svg')), emboss=True, depress=False)


class SNA_OT_Dgs_Render_Launch_Kiri_Site_84772(bpy.types.Operator):
    bl_idname = "sna.dgs_render_launch_kiri_site_84772"
    bl_label = "3DGS Render: Launch KIRI Site"
    bl_description = "Launches a browser for the KIRI Engine main site"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        url = 'https://www.kiriengine.app/'
        # Open the web browser and go to the specified URL
        webbrowser.open(url)
        print(f"Opening web browser to {url}")
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Dgs_Render_Launch_Superhive_Store_0Bcb5(bpy.types.Operator):
    bl_idname = "sna.dgs_render_launch_superhive_store_0bcb5"
    bl_label = "3DGS Render: Launch SuperHive Store"
    bl_description = "Launches a browser for the KIRI Engine SuperHive store"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        url = 'https://blendermarket.com/creators/blender-addon-from-kiri-engine'
        # Open the web browser and go to the specified URL
        webbrowser.open(url)
        print(f"Opening web browser to {url}")
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Dgs_Render_Launch_Kiri_Blender_Addons_Page_9427F(bpy.types.Operator):
    bl_idname = "sna.dgs_render_launch_kiri_blender_addons_page_9427f"
    bl_label = "3DGS Render: Launch KIRI Blender Addons page"
    bl_description = "Launches a browser for the KIRI Engine Blender Market store"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        url = 'https://www.kiriengine.app/blender-addon'
        # Open the web browser and go to the specified URL
        webbrowser.open(url)
        print(f"Opening web browser to {url}")
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Dgs_Render_Open_Documentation_3B870(bpy.types.Operator):
    bl_idname = "sna.dgs_render_open_documentation_3b870"
    bl_label = "3DGS Render: Open Documentation"
    bl_description = "Launches a browser with the addon documentation"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        url = 'https://www.kiriengine.app/blender-addon/3dgs-render'
        # Open the web browser and go to the specified URL
        webbrowser.open(url)
        print(f"Opening web browser to {url}")
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Dgs_Render_Open_Tutorial_Video_D0Cd5(bpy.types.Operator):
    bl_idname = "sna.dgs_render_open_tutorial_video_d0cd5"
    bl_label = "3DGS Render: Open Tutorial Video"
    bl_description = "Launches a browser with the addon documentation video"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        url = 'https://www.youtube.com/@BlenderAddon-fromKIRI'
        # Open the web browser and go to the specified URL
        webbrowser.open(url)
        print(f"Opening web browser to {url}")
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


def sna_edit_by_colour_functions_function_interface_7277A(layout_function, ):
    if (bpy.context.view_layer.objects.active == None):
        pass
    else:
        box_5BFA9 = layout_function.box()
        box_5BFA9.alert = False
        box_5BFA9.enabled = True
        box_5BFA9.active = True
        box_5BFA9.use_property_split = False
        box_5BFA9.use_property_decorate = False
        box_5BFA9.alignment = 'Expand'.upper()
        box_5BFA9.scale_x = 1.0
        box_5BFA9.scale_y = 1.0
        if not True: box_5BFA9.operator_context = "EXEC_DEFAULT"
        box_DC03C = box_5BFA9.box()
        box_DC03C.alert = False
        box_DC03C.enabled = True
        box_DC03C.active = True
        box_DC03C.use_property_split = False
        box_DC03C.use_property_decorate = False
        box_DC03C.alignment = 'Expand'.upper()
        box_DC03C.scale_x = 1.0
        box_DC03C.scale_y = 1.0
        if not True: box_DC03C.operator_context = "EXEC_DEFAULT"
        layout_function = box_DC03C
        sna_add_remove_modifier_function_interface_02DDA(layout_function, )
        if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_Edit_By_Colour_GN' in bpy.context.view_layer.objects.active.modifiers):
            box_49EC8 = box_5BFA9.box()
            box_49EC8.alert = False
            box_49EC8.enabled = True
            box_49EC8.active = True
            box_49EC8.use_property_split = False
            box_49EC8.use_property_decorate = False
            box_49EC8.alignment = 'Expand'.upper()
            box_49EC8.scale_x = 1.0
            box_49EC8.scale_y = 1.0
            if not True: box_49EC8.operator_context = "EXEC_DEFAULT"
            layout_function = box_49EC8
            sna_active_object_properties_function_interface_3951A(layout_function, )
        if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'KIRI_Edit_By_Colour_GN' in bpy.context.view_layer.objects.active.modifiers):
            if (kiri_gn_get(bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], 'Socket_4') == None):
                pass
            else:
                col_2BD89 = box_5BFA9.column(heading='', align=False)
                col_2BD89.alert = False
                col_2BD89.enabled = True
                col_2BD89.active = True
                col_2BD89.use_property_split = False
                col_2BD89.use_property_decorate = False
                col_2BD89.scale_x = 1.0
                col_2BD89.scale_y = 1.0
                col_2BD89.alignment = 'Expand'.upper()
                col_2BD89.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                box_3C86E = col_2BD89.box()
                box_3C86E.alert = False
                box_3C86E.enabled = True
                box_3C86E.active = True
                box_3C86E.use_property_split = False
                box_3C86E.use_property_decorate = False
                box_3C86E.alignment = 'Expand'.upper()
                box_3C86E.scale_x = 1.0
                box_3C86E.scale_y = 1.0
                if not True: box_3C86E.operator_context = "EXEC_DEFAULT"
                layout_function = box_3C86E
                sna_live_effects_function_interface_5A08A(layout_function, )
                if (kiri_gn_get(bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], 'Socket_48') == 5):
                    box_4AEEA = col_2BD89.box()
                    box_4AEEA.alert = False
                    box_4AEEA.enabled = True
                    box_4AEEA.active = True
                    box_4AEEA.use_property_split = False
                    box_4AEEA.use_property_decorate = False
                    box_4AEEA.alignment = 'Expand'.upper()
                    box_4AEEA.scale_x = 1.0
                    box_4AEEA.scale_y = 1.0
                    if not True: box_4AEEA.operator_context = "EXEC_DEFAULT"
                    grid_31ECB = box_4AEEA.grid_flow(columns=2, row_major=False, even_columns=False, even_rows=False, align=True)
                    grid_31ECB.enabled = True
                    grid_31ECB.active = True
                    grid_31ECB.use_property_split = False
                    grid_31ECB.use_property_decorate = False
                    grid_31ECB.alignment = 'Expand'.upper()
                    grid_31ECB.scale_x = 1.0
                    grid_31ECB.scale_y = 1.0
                    if not True: grid_31ECB.operator_context = "EXEC_DEFAULT"
                    grid_31ECB.prop(bpy.context.scene.sna_ebc_scene_properties, 'active_menu_retopo_loops', text=bpy.context.scene.sna_ebc_scene_properties.active_menu_retopo_loops, icon_value=0, emboss=True, expand=True)
                else:
                    box_594E9 = col_2BD89.box()
                    box_594E9.alert = False
                    box_594E9.enabled = True
                    box_594E9.active = True
                    box_594E9.use_property_split = False
                    box_594E9.use_property_decorate = False
                    box_594E9.alignment = 'Expand'.upper()
                    box_594E9.scale_x = 1.0
                    box_594E9.scale_y = 1.0
                    if not True: box_594E9.operator_context = "EXEC_DEFAULT"
                    grid_40E66 = box_594E9.grid_flow(columns=2, row_major=False, even_columns=False, even_rows=False, align=True)
                    grid_40E66.enabled = True
                    grid_40E66.active = True
                    grid_40E66.use_property_split = False
                    grid_40E66.use_property_decorate = False
                    grid_40E66.alignment = 'Expand'.upper()
                    grid_40E66.scale_x = 1.0
                    grid_40E66.scale_y = 1.0
                    if not True: grid_40E66.operator_context = "EXEC_DEFAULT"
                    grid_40E66.prop(bpy.context.scene.sna_ebc_scene_properties, 'active_menu_full', text=bpy.context.scene.sna_ebc_scene_properties.active_menu_full, icon_value=0, emboss=True, expand=True)
                if (kiri_gn_get(bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], 'Socket_48') == 5):
                    if (bpy.context.scene.sna_ebc_scene_properties.active_menu_retopo_loops == 'Colour Selection'):
                        box_06706 = col_2BD89.box()
                        box_06706.alert = False
                        box_06706.enabled = True
                        box_06706.active = True
                        box_06706.use_property_split = False
                        box_06706.use_property_decorate = False
                        box_06706.alignment = 'Expand'.upper()
                        box_06706.scale_x = 1.0
                        box_06706.scale_y = 1.0
                        if not True: box_06706.operator_context = "EXEC_DEFAULT"
                        layout_function = box_06706
                        sna_adjust_selection_function_interface_541E9(layout_function, )
                else:
                    if (bpy.context.scene.sna_ebc_scene_properties.active_menu_full == 'Colour Selection'):
                        box_3F66F = col_2BD89.box()
                        box_3F66F.alert = False
                        box_3F66F.enabled = True
                        box_3F66F.active = True
                        box_3F66F.use_property_split = False
                        box_3F66F.use_property_decorate = False
                        box_3F66F.alignment = 'Expand'.upper()
                        box_3F66F.scale_x = 1.0
                        box_3F66F.scale_y = 1.0
                        if not True: box_3F66F.operator_context = "EXEC_DEFAULT"
                        layout_function = box_3F66F
                        sna_adjust_selection_function_interface_541E9(layout_function, )
                if 'OBJECT'==bpy.context.mode:
                    if (kiri_gn_get(bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], 'Socket_48') == 5):
                        pass
                    else:
                        if (bpy.context.scene.sna_ebc_scene_properties.active_menu_full == 'Edit Mesh'):
                            box_84303 = col_2BD89.box()
                            box_84303.alert = False
                            box_84303.enabled = True
                            box_84303.active = True
                            box_84303.use_property_split = False
                            box_84303.use_property_decorate = False
                            box_84303.alignment = 'Expand'.upper()
                            box_84303.scale_x = 1.0
                            box_84303.scale_y = 1.0
                            if not True: box_84303.operator_context = "EXEC_DEFAULT"
                            layout_function = box_84303
                            sna_edit_effects_function_interface_6C02F(layout_function, )
                if 'OBJECT'==bpy.context.mode:
                    if (kiri_gn_get(bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], 'Socket_48') == 5):
                        pass
                    else:
                        if (bpy.context.scene.sna_ebc_scene_properties.active_menu_full == 'Texture'):
                            box_16002 = col_2BD89.box()
                            box_16002.alert = False
                            box_16002.enabled = True
                            box_16002.active = True
                            box_16002.use_property_split = False
                            box_16002.use_property_decorate = False
                            box_16002.alignment = 'Expand'.upper()
                            box_16002.scale_x = 1.0
                            box_16002.scale_y = 1.0
                            if not True: box_16002.operator_context = "EXEC_DEFAULT"
                            layout_function = box_16002
                            sna_texture_function_interface_D6644(layout_function, )
                if ('SCULPT'==bpy.context.mode or 'OBJECT'==bpy.context.mode):
                    if (kiri_gn_get(bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], 'Socket_48') == 5):
                        pass
                    else:
                        if (bpy.context.scene.sna_ebc_scene_properties.active_menu_full == 'Sculpt'):
                            box_26DF2 = col_2BD89.box()
                            box_26DF2.alert = False
                            box_26DF2.enabled = True
                            box_26DF2.active = True
                            box_26DF2.use_property_split = False
                            box_26DF2.use_property_decorate = False
                            box_26DF2.alignment = 'Expand'.upper()
                            box_26DF2.scale_x = 1.0
                            box_26DF2.scale_y = 1.0
                            if not True: box_26DF2.operator_context = "EXEC_DEFAULT"
                            layout_function = box_26DF2
                            sna_sculpt_function_interface_92592(layout_function, )
                if 'OBJECT'==bpy.context.mode:
                    if (kiri_gn_get(bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], 'Socket_48') == 5):
                        if (bpy.context.scene.sna_ebc_scene_properties.active_menu_retopo_loops == 'Retopo Loops'):
                            box_83655 = col_2BD89.box()
                            box_83655.alert = False
                            box_83655.enabled = True
                            box_83655.active = True
                            box_83655.use_property_split = False
                            box_83655.use_property_decorate = False
                            box_83655.alignment = 'Expand'.upper()
                            box_83655.scale_x = 1.0
                            box_83655.scale_y = 1.0
                            if not True: box_83655.operator_context = "EXEC_DEFAULT"
                            layout_function = box_83655
                            sna_retopo_loops_function_interface_61CF5(layout_function, )


def sna_texture_function_interface_D6644(layout_function, ):
    layout_function.label(text='Texture', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'color-palette.svg')))
    layout_function = layout_function
    sna_shader_attributes_function_interface_0EC7B(layout_function, )
    layout_function = layout_function
    sna_bake_patch_function_interface_834B3(layout_function, )
    layout_function = layout_function
    sna_bake_combined_function_interface_4566F(layout_function, )


class SNA_OT_Add_Ebc_Attribute_To_Selected_Material_3F5C9(bpy.types.Operator):
    bl_idname = "sna.add_ebc_attribute_to_selected_material_3f5c9"
    bl_label = "Add EBC attribute to selected material"
    bl_description = "Applies the EBC selection as an attribute and adds an attribute node to the selected material."
    bl_options = {"REGISTER", "UNDO"}
    sna_apply_subdivision: bpy.props.BoolProperty(name='Apply Subdivision?', description='', default=False)

    def sna_set_live_effects_to_enum_items(self, context):
        return [("No Items", "No Items", "No generate enum items node found to create items!", "ERROR", 0)]
    sna_set_live_effects_to: bpy.props.EnumProperty(name='Set Live Effects to:', description='', items=[('None', 'None', '', 0, 0), ('Set Material', 'Set Material', '', 0, 1), ('No Change', 'No Change', '', 0, 2)])

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        if (bpy.context.scene.sna_ebc_scene_properties.base_material == None):
            self.report({'ERROR'}, message='No material assigned')
        else:
            sna_ebc_select_function_execute_82A8F(self.sna_apply_subdivision, self.sna_set_live_effects_to)
            bpy.ops.object.mode_set('INVOKE_DEFAULT', mode='OBJECT')
            node_281D0 = bpy.context.scene.sna_ebc_scene_properties.base_material.node_tree.nodes.new(type='ShaderNodeAttribute', )
            node_281D0.attribute_name = 'EBC_Selection'
            if (property_exists("bpy.context.view_layer.objects.active.active_material.node_tree.nodes", globals(), locals()) and 'Material Output' in bpy.context.view_layer.objects.active.active_material.node_tree.nodes):
                node_281D0.location = (bpy.context.scene.sna_ebc_scene_properties.base_material.node_tree.nodes['Material Output'].location[0], float(bpy.context.scene.sna_ebc_scene_properties.base_material.node_tree.nodes['Material Output'].location[1] + 200.0))
        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout
        box_85BF0 = layout.box()
        box_85BF0.alert = False
        box_85BF0.enabled = True
        box_85BF0.active = True
        box_85BF0.use_property_split = False
        box_85BF0.use_property_decorate = False
        box_85BF0.alignment = 'Expand'.upper()
        box_85BF0.scale_x = 1.0
        box_85BF0.scale_y = 1.0
        if not True: box_85BF0.operator_context = "EXEC_DEFAULT"
        box_7232E = box_85BF0.box()
        box_7232E.alert = False
        box_7232E.enabled = True
        box_7232E.active = True
        box_7232E.use_property_split = False
        box_7232E.use_property_decorate = False
        box_7232E.alignment = 'Expand'.upper()
        box_7232E.scale_x = 1.0
        box_7232E.scale_y = 1.0
        if not True: box_7232E.operator_context = "EXEC_DEFAULT"
        box_971AA = box_7232E.box()
        box_971AA.alert = False
        box_971AA.enabled = True
        box_971AA.active = True
        box_971AA.use_property_split = False
        box_971AA.use_property_decorate = False
        box_971AA.alignment = 'Expand'.upper()
        box_971AA.scale_x = 1.0
        box_971AA.scale_y = 1.0
        if not True: box_971AA.operator_context = "EXEC_DEFAULT"
        box_971AA.label(text='The Edit By Colour modifier will be applied, then re-added', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'tips-one.svg')))
        box_971AA.label(text='         These effects are destructive', icon_value=0)
        box_7232E.label(text='Set Live Effects to:', icon_value=0)
        box_7232E.prop(self, 'sna_set_live_effects_to', text='', icon_value=0, emboss=True)
        box_7232E.prop(self, 'sna_apply_subdivision', text='Apply Subdivisions', icon_value=0, emboss=True, toggle=False)
        if self.sna_apply_subdivision:
            col_BBE4C = box_7232E.column(heading='', align=False)
            col_BBE4C.alert = False
            col_BBE4C.enabled = True
            col_BBE4C.active = True
            col_BBE4C.use_property_split = False
            col_BBE4C.use_property_decorate = False
            col_BBE4C.scale_x = 1.0
            col_BBE4C.scale_y = 1.0
            col_BBE4C.alignment = 'Expand'.upper()
            col_BBE4C.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            box_CDF6B = col_BBE4C.box()
            box_CDF6B.alert = False
            box_CDF6B.enabled = True
            box_CDF6B.active = True
            box_CDF6B.use_property_split = False
            box_CDF6B.use_property_decorate = False
            box_CDF6B.alignment = 'Expand'.upper()
            box_CDF6B.scale_x = 1.0
            box_CDF6B.scale_y = 1.0
            if not True: box_CDF6B.operator_context = "EXEC_DEFAULT"
            box_CDF6B.label(text='This act is destructive', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'tips-one.svg')))
            box_CDF6B.label(text='Select will take longer with higher face counts', icon_value=0)
            box_CDF6B.label(text='Other modifiers will not be applied', icon_value=0)
            box_F46BD = col_BBE4C.box()
            box_F46BD.alert = False
            box_F46BD.enabled = True
            box_F46BD.active = True
            box_F46BD.use_property_split = False
            box_F46BD.use_property_decorate = False
            box_F46BD.alignment = 'Expand'.upper()
            box_F46BD.scale_x = 1.0
            box_F46BD.scale_y = 1.0
            if not True: box_F46BD.operator_context = "EXEC_DEFAULT"
            box_F46BD.label(text='Base face count =' + ' ' + str(len(bpy.context.view_layer.objects.active.data.polygons)), icon_value=0)
            box_F46BD.label(text='Face count with subdivisions + other modifiers =' + ' ' + str(ebcfunctionedit_effects['sna_evaluatedfacecount']), icon_value=0)
        box_85BF0.label(text='Shader Attribute Settings', icon_value=0)
        box_29F78 = box_85BF0.box()
        box_29F78.alert = False
        box_29F78.enabled = True
        box_29F78.active = True
        box_29F78.use_property_split = False
        box_29F78.use_property_decorate = False
        box_29F78.alignment = 'Expand'.upper()
        box_29F78.scale_x = 1.0
        box_29F78.scale_y = 1.0
        if not True: box_29F78.operator_context = "EXEC_DEFAULT"
        box_29F78.prop_search(bpy.context.scene.sna_ebc_scene_properties, 'base_material', bpy.data, 'materials', text='Material', icon='NONE')

    def invoke(self, context, event):
        bpy.context.scene.sna_ebc_scene_properties.base_material = bpy.context.view_layer.objects.active.material_slots[0].material
        bm_0D07F = bmesh.new()
        if bpy.context.view_layer.objects.active:
            if bpy.context.view_layer.objects.active.mode == 'EDIT' and False:
                bm_0D07F = bmesh.from_edit_mesh(bpy.context.view_layer.objects.active.data)
            else:
                if True:
                    dg = bpy.context.evaluated_depsgraph_get()
                    bm_0D07F.from_mesh(bpy.context.view_layer.objects.active.evaluated_get(dg).to_mesh())
                else:
                    bm_0D07F.from_mesh(bpy.context.view_layer.objects.active.data)
        if False:
            bm_0D07F.transform(bpy.context.view_layer.objects.active.matrix_world)
        bm_0D07F.verts.ensure_lookup_table()
        bm_0D07F.faces.ensure_lookup_table()
        bm_0D07F.edges.ensure_lookup_table()
        ebcfunctionedit_effects['sna_evaluatedfacecount'] = len(bm_0D07F.faces)
        return context.window_manager.invoke_props_dialog(self, width=500)


def sna_shader_attributes_function_interface_0EC7B(layout_function, ):
    box_F143E = layout_function.box()
    box_F143E.alert = False
    box_F143E.enabled = True
    box_F143E.active = True
    box_F143E.use_property_split = False
    box_F143E.use_property_decorate = False
    box_F143E.alignment = 'Expand'.upper()
    box_F143E.scale_x = 1.0
    box_F143E.scale_y = 1.0
    if not True: box_F143E.operator_context = "EXEC_DEFAULT"
    box_F143E.label(text='Shader Attributes', icon_value=0)
    if (bpy.context.mode == 'OBJECT'):
        op = box_F143E.operator('sna.add_ebc_attribute_to_selected_material_3f5c9', text='Create Material Attributes', icon_value=0, emboss=True, depress=False)
        op.sna_apply_subdivision = False
        op.sna_set_live_effects_to = 'None'


class SNA_OT_Bake_Set_Material__Original_Dafdb(bpy.types.Operator):
    bl_idname = "sna.bake_set_material__original_dafdb"
    bl_label = "Bake Set Material + Original"
    bl_description = "Bakes all materials currently assigned to the active object."
    bl_options = {"REGISTER", "UNDO"}
    sna_bake_samples: bpy.props.IntProperty(name='Bake Samples', description='', default=10, subtype='NONE', min=1)
    sna_bake_diffuse: bpy.props.BoolProperty(name='Bake Diffuse', description='', default=False)
    sna_bake_roughness: bpy.props.BoolProperty(name='Bake Roughness', description='', default=False)
    sna_bake_normal: bpy.props.BoolProperty(name='Bake Normal', description='', default=False)

    def sna_bake_resolution_enum_items(self, context):
        return [("No Items", "No Items", "No generate enum items node found to create items!", "ERROR", 0)]
    sna_bake_resolution: bpy.props.EnumProperty(name='Bake Resolution', description='', items=[('1K', '1K', '', 0, 0), ('2K', '2K', '', 0, 1), ('4K', '4K', '', 0, 2), ('8K', '8K', '', 0, 3)])
    sna_apply_subdivision: bpy.props.BoolProperty(name='Apply Subdivision?', description='', default=False)

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        if ((not self.sna_bake_diffuse) and (not self.sna_bake_roughness) and (not self.sna_bake_normal)):
            self.report({'INFO'}, message='No bake passes selected - no changes made')
        else:
            target_object = bpy.context.view_layer.objects.active
            remove_empty = True
            remove_unused = True
            # REMOVE UNUSED MATERIALS
            # Removes unused material slots from an object (empty slots and slots not used by any polygons)
            #target_object: Object to clean materials from
            #Type: Pointer
            #Pointer: bpy.types.Object
            #Description: Target object to remove unused materials from
            #remove_empty: Remove slots with no material assigned
            #Values: True, False
            #Default: True
            #Description: Whether to remove slots that have no material assigned
            #remove_unused: Remove slots not used by any polygons
            #Values: True, False
            #Default: True
            #Description: Whether to remove slots that aren't used by any faces
            # Input variables
            #target_object = None
            #remove_empty = True
            #remove_unused = True
            # Output variables
            success = False
            error_message = ""
            removed_count = 0
            try:
                print(f"Cleaning materials for object: {target_object.name}")
                initial_slot_count = len(target_object.material_slots)
                print(f"Initial material slots: {initial_slot_count}")
                # First pass: Remove empty slots
                if remove_empty:
                    print("Checking for empty slots...")
                    for i in range(len(target_object.material_slots) - 1, -1, -1):
                        if target_object.material_slots[i].material is None:
                            target_object.data.materials.pop(index=i)
                            print(f"Removed empty slot at index {i}")
                            removed_count += 1
                # Second pass: Remove unused slots
                if remove_unused and hasattr(target_object.data, "polygons"):
                    print("Checking for unused slots...")
                    used_indices = {p.material_index for p in target_object.data.polygons}
                    print(f"Found used material indices: {used_indices}")
                    for i in range(len(target_object.material_slots) - 1, -1, -1):
                        if i not in used_indices:
                            target_object.data.materials.pop(index=i)
                            print(f"Removed unused slot at index {i}")
                            removed_count += 1
                final_slot_count = len(target_object.material_slots)
                print(f"Removed {removed_count} slots total")
                print(f"Final material slot count: {final_slot_count}")
                success = True
            except Exception as e:
                error_message = str(e)
                print(f"Error cleaning materials: {error_message}")
                removed_count = 0
            if self.sna_apply_subdivision:
                pass
            else:
                kiri_gn_set(bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], 'Socket_50', 0)
            if (kiri_gn_get(bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], 'Socket_26') == None):
                pass
            else:
                ebctexturebake_combined['sna_ebc_temp_store_set_material'] = kiri_gn_get(bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], 'Socket_26')
            ebctexturebake_combined['sna_ebc_temp_store_base_texture'] = kiri_gn_get(bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], 'Socket_4')
            modifier_name = 'KIRI_Edit_By_Colour_GN'
            object_name = bpy.context.view_layer.objects.active.name
            obj = bpy.data.objects.get(object_name)
            if obj:
                modifier = obj.modifiers.get(modifier_name)
                if modifier:
                    if not modifier.show_viewport:
                        # Simply remove the modifier if it's hidden
                        obj.modifiers.remove(modifier)
                        print(f"Removed hidden modifier '{modifier_name}' from object '{object_name}'.")
                    else:
                        # Apply normally if visible
                        bpy.ops.object.modifier_apply(modifier=modifier_name)
                        print(f"Applied visible modifier '{modifier_name}' to object '{object_name}'.")
                else:
                    print(f"Modifier '{modifier_name}' not found on object '{object_name}'.")
            else:
                print(f"Object '{object_name}' not found.")
            sna_add_edit_by_colour_modifier_function_execute_7A473()
            kiri_gn_set(bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], 'Socket_4', ebctexturebake_combined['sna_ebc_temp_store_base_texture'])
            kiri_gn_set(bpy.context.view_layer.objects.active.modifiers['KIRI_Edit_By_Colour_GN'], 'Socket_48', 0)
            bpy.context.active_object.update_tag(refresh={'DATA'}, )
            if bpy.context and bpy.context.screen:
                for a in bpy.context.screen.areas:
                    a.tag_redraw()
            bpy.context.view_layer.objects.active.sna_ebc_object_properties.live_effects_proxy_switch = 'None'
            bpy.context.scene.sna_ebc_scene_properties.active_menu_full = 'Texture'
            bpy.context.scene.render.engine = 'CYCLES'
            bpy.context.scene.cycles.use_denoising = False
            bpy.context.scene.cycles.samples = self.sna_bake_samples
            ebctexturebake_combined['sna_ebc_bake_type_list'] = []
            if self.sna_bake_diffuse:
                ebctexturebake_combined['sna_ebc_bake_type_list'].append('DIFFUSE')
            if self.sna_bake_roughness:
                ebctexturebake_combined['sna_ebc_bake_type_list'].append('ROUGHNESS')
            if self.sna_bake_normal:
                ebctexturebake_combined['sna_ebc_bake_type_list'].append('NORMAL')
            for i_0660C in range(len(bpy.context.view_layer.objects.active.material_slots)):
                for i_57D31 in range(len(bpy.context.view_layer.objects.active.material_slots[i_0660C].material.node_tree.nodes)):
                    bpy.context.view_layer.objects.active.material_slots[i_0660C].material.node_tree.nodes[i_57D31].select = False
            if (property_exists("bpy.data.materials", globals(), locals()) and 'Combined_Bake_Material' in bpy.data.materials):
                pass
            else:
                before_data = list(bpy.data.materials)
                bpy.ops.wm.append(directory=os.path.join(os.path.dirname(__file__), 'assets', 'KIRI_Edit_By_Colour_OBJECT_APPEND.blend') + r'\Material', filename='EBC_Combined_Bake_Material', link=False)
                new_data = list(filter(lambda d: not d in before_data, list(bpy.data.materials)))
                appended_41152 = None if not new_data else new_data[0]
            ebctexturebake_combined['sna_ebc_bake_count'] = 0

            def delayed_0E63E():
                is_baking = None
                is_baking = bpy.app.is_job_running("OBJECT_BAKE")
                if is_baking:
                    pass
                else:
                    image_294E9 = bpy.data.images.new(name='Combined_Bake_' + ebctexturebake_combined['sna_ebc_bake_type_list'][ebctexturebake_combined['sna_ebc_bake_count']] + '_Texture', width=(((8192 if (self.sna_bake_resolution != '4K') else 4096) if (self.sna_bake_resolution != '2K') else 2048) if (self.sna_bake_resolution != '1K') else 1080), height=(((8192 if (self.sna_bake_resolution != '4K') else 4096) if (self.sna_bake_resolution != '2K') else 2048) if (self.sna_bake_resolution != '1K') else 1080), is_data=(ebctexturebake_combined['sna_ebc_bake_type_list'][ebctexturebake_combined['sna_ebc_bake_count']] != 'DIFFUSE'), )
                    if (ebctexturebake_combined['sna_ebc_bake_type_list'][ebctexturebake_combined['sna_ebc_bake_count']] == 'DIFFUSE'):
                        bpy.context.scene.sna_ebc_scene_properties.baked_diffuse_image = image_294E9
                    if (ebctexturebake_combined['sna_ebc_bake_type_list'][ebctexturebake_combined['sna_ebc_bake_count']] == 'ROUGHNESS'):
                        bpy.context.scene.sna_ebc_scene_properties.baked_roughness_image = image_294E9
                    if (ebctexturebake_combined['sna_ebc_bake_type_list'][ebctexturebake_combined['sna_ebc_bake_count']] == 'NORMAL'):
                        bpy.context.scene.sna_ebc_scene_properties.baked_normal_image = image_294E9
                    for i_1AD62 in range(len(bpy.context.view_layer.objects.active.material_slots)):
                        if (property_exists("bpy.context.view_layer.objects.active.material_slots[i_1AD62].material.node_tree.nodes", globals(), locals()) and 'Combined_Bake_' + ebctexturebake_combined['sna_ebc_bake_type_list'][ebctexturebake_combined['sna_ebc_bake_count']] + '_Node' in bpy.context.view_layer.objects.active.material_slots[i_1AD62].material.node_tree.nodes):
                            pass
                        else:
                            node_ECC29 = bpy.context.view_layer.objects.active.material_slots[i_1AD62].material.node_tree.nodes.new(type='ShaderNodeTexImage', )
                            node_ECC29.name = 'Combined_Bake_' + ebctexturebake_combined['sna_ebc_bake_type_list'][ebctexturebake_combined['sna_ebc_bake_count']] + '_Node'
                            node_ECC29.label = 'Combined_Bake_' + ebctexturebake_combined['sna_ebc_bake_type_list'][ebctexturebake_combined['sna_ebc_bake_count']] + '_Node'
                            node_ECC29.use_custom_color = True
                            node_ECC29.color = (0.09107446670532227, 0.274009108543396, 1.0)
                            node_ECC29.location = (400.0, float(ebctexturebake_combined['sna_ebc_bake_count'] * -250.0))
                            node_ECC29.image = image_294E9
                            bpy.context.view_layer.objects.active.material_slots[i_1AD62].material.node_tree.nodes.active = node_ECC29
                            node_ECC29.select = True
                        bpy.context.view_layer.objects.active.material_slots[i_1AD62].material.node_tree.nodes['Combined_Bake_' + ebctexturebake_combined['sna_ebc_bake_type_list'][ebctexturebake_combined['sna_ebc_bake_count']] + '_Node'].image = image_294E9
                        bpy.context.view_layer.objects.active.material_slots[i_1AD62].material.node_tree.nodes.active = bpy.context.view_layer.objects.active.material_slots[i_1AD62].material.node_tree.nodes['Combined_Bake_' + ebctexturebake_combined['sna_ebc_bake_type_list'][ebctexturebake_combined['sna_ebc_bake_count']] + '_Node']
                        bpy.context.view_layer.objects.active.material_slots[i_1AD62].material.node_tree.nodes['Combined_Bake_' + ebctexturebake_combined['sna_ebc_bake_type_list'][ebctexturebake_combined['sna_ebc_bake_count']] + '_Node'].select = True
                    bpy.context.view_layer.objects.active.select_set(state=True, view_layer=bpy.context.view_layer, )
                    bpy.ops.object.bake('INVOKE_DEFAULT', type=ebctexturebake_combined['sna_ebc_bake_type_list'][ebctexturebake_combined['sna_ebc_bake_count']], pass_filter=set([('COLOR' if (ebctexturebake_combined['sna_ebc_bake_type_list'][ebctexturebake_combined['sna_ebc_bake_count']] == 'DIFFUSE') else 'NONE')]), margin=16, use_selected_to_active=False, max_ray_distance=0.0, cage_extrusion=1.0, normal_space='TANGENT', normal_r='POS_X', normal_g='POS_Y', normal_b='POS_Z', target='IMAGE_TEXTURES', save_mode='INTERNAL', use_clear=True)
                    ebctexturebake_combined['sna_ebc_bake_count'] += 1
                if (ebctexturebake_combined['sna_ebc_bake_count'] == len(ebctexturebake_combined['sna_ebc_bake_type_list'])):
                    return None
                return 0.10000000149011612
            bpy.app.timers.register(delayed_0E63E, first_interval=0.0)
        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout
        box_45332 = layout.box()
        box_45332.alert = False
        box_45332.enabled = True
        box_45332.active = True
        box_45332.use_property_split = False
        box_45332.use_property_decorate = False
        box_45332.alignment = 'Expand'.upper()
        box_45332.scale_x = 1.0
        box_45332.scale_y = 1.0
        if not True: box_45332.operator_context = "EXEC_DEFAULT"
        box_5D865 = box_45332.box()
        box_5D865.alert = False
        box_5D865.enabled = True
        box_5D865.active = True
        box_5D865.use_property_split = False
        box_5D865.use_property_decorate = False
        box_5D865.alignment = 'Expand'.upper()
        box_5D865.scale_x = 1.0
        box_5D865.scale_y = 1.0
        if not True: box_5D865.operator_context = "EXEC_DEFAULT"
        box_A2874 = box_5D865.box()
        box_A2874.alert = False
        box_A2874.enabled = True
        box_A2874.active = True
        box_A2874.use_property_split = False
        box_A2874.use_property_decorate = False
        box_A2874.alignment = 'Expand'.upper()
        box_A2874.scale_x = 1.0
        box_A2874.scale_y = 1.0
        if not True: box_A2874.operator_context = "EXEC_DEFAULT"
        box_A2874.label(text='The Edit By Colour modifier will be applied, then re-added', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'tips-one.svg')))
        box_A2874.label(text='         These effects are destructive', icon_value=0)
        box_5D865.prop(self, 'sna_apply_subdivision', text='Apply Subdivisions', icon_value=0, emboss=True)
        box_45332.label(text='Bake Settings', icon_value=0)
        box_67968 = box_45332.box()
        box_67968.alert = False
        box_67968.enabled = True
        box_67968.active = True
        box_67968.use_property_split = False
        box_67968.use_property_decorate = False
        box_67968.alignment = 'Expand'.upper()
        box_67968.scale_x = 1.0
        box_67968.scale_y = 1.0
        if not True: box_67968.operator_context = "EXEC_DEFAULT"
        box_67968.prop(bpy.context.scene.cycles, 'device', text='Bake Device', icon_value=0, emboss=True)
        box_67968.prop(self, 'sna_bake_samples', text='Bake Samples', icon_value=0, emboss=True)
        box_C3C21 = box_45332.box()
        box_C3C21.alert = False
        box_C3C21.enabled = True
        box_C3C21.active = True
        box_C3C21.use_property_split = False
        box_C3C21.use_property_decorate = False
        box_C3C21.alignment = 'Expand'.upper()
        box_C3C21.scale_x = 1.0
        box_C3C21.scale_y = 1.0
        if not True: box_C3C21.operator_context = "EXEC_DEFAULT"
        box_C3C21.prop_search(bpy.context.scene.sna_ebc_scene_properties, 'base_material', bpy.data, 'objects', text='Base Material', icon='NONE')
        box_1531A = box_45332.box()
        box_1531A.alert = False
        box_1531A.enabled = True
        box_1531A.active = True
        box_1531A.use_property_split = False
        box_1531A.use_property_decorate = False
        box_1531A.alignment = 'Expand'.upper()
        box_1531A.scale_x = 1.0
        box_1531A.scale_y = 1.0
        if not True: box_1531A.operator_context = "EXEC_DEFAULT"
        box_1531A.prop(self, 'sna_bake_resolution', text='Bake Resolution', icon_value=0, emboss=True)
        box_BA395 = box_45332.box()
        box_BA395.alert = False
        box_BA395.enabled = True
        box_BA395.active = True
        box_BA395.use_property_split = False
        box_BA395.use_property_decorate = False
        box_BA395.alignment = 'Expand'.upper()
        box_BA395.scale_x = 1.0
        box_BA395.scale_y = 1.0
        if not True: box_BA395.operator_context = "EXEC_DEFAULT"
        box_BA395.prop(self, 'sna_bake_diffuse', text='Bake Diffuse', icon_value=0, emboss=True)
        box_BA395.prop(self, 'sna_bake_roughness', text='Bake Roughness', icon_value=0, emboss=True)
        box_BA395.prop(self, 'sna_bake_normal', text='Bake Normal', icon_value=0, emboss=True)

    def invoke(self, context, event):
        bpy.context.scene.sna_ebc_scene_properties.base_material = bpy.context.view_layer.objects.active.material_slots[0].material
        return context.window_manager.invoke_props_dialog(self, width=500)


def sna_bake_combined_function_interface_4566F(layout_function, ):
    box_97CC3 = layout_function.box()
    box_97CC3.alert = False
    box_97CC3.enabled = True
    box_97CC3.active = True
    box_97CC3.use_property_split = False
    box_97CC3.use_property_decorate = False
    box_97CC3.alignment = 'Expand'.upper()
    box_97CC3.scale_x = 1.0
    box_97CC3.scale_y = 1.0
    if not True: box_97CC3.operator_context = "EXEC_DEFAULT"
    box_97CC3.label(text='Unify Textures', icon_value=0)
    op = box_97CC3.operator('sna.bake_set_material__original_dafdb', text='Bake Combined Material', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'material.svg')), emboss=True, depress=False)
    op.sna_bake_diffuse = False
    op.sna_bake_roughness = False
    op.sna_bake_normal = False
    op.sna_bake_resolution = '1K'
    op.sna_apply_subdivision = False
    op = box_97CC3.operator('sna.switch_to_combined_bake_material_a7d5f', text='Switch To Baked Material', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'update.svg')), emboss=True, depress=False)


class SNA_OT_Switch_To_Combined_Bake_Material_A7D5F(bpy.types.Operator):
    bl_idname = "sna.switch_to_combined_bake_material_a7d5f"
    bl_label = "Switch To Combined Bake Material"
    bl_description = "Removes all materials assigned to the active object and replaces them with the combined bake material."
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        target_object = bpy.context.view_layer.objects.active
        material_to_assign = bpy.context.scene.sna_ebc_scene_properties.combined_bake_material
        clear_unused = True
        make_active = True
        assign_all_faces = True
        # ASSIGN NEW MATERIAL SLOT
        # Adds a new material slot to an object and assigns the specified material to it with optional face assignment
        #target_object: Object to add material slot to
        #Type: Pointer
        #Pointer: bpy.types.Object
        #Description: Target object that will receive the new material slot
        #material_to_assign: Material to assign to new slot
        #Type: Pointer
        #Pointer: bpy.types.Material
        #Description: Material that will be assigned to the new slot
        #clear_unused: Clear unused materials first
        #Values: True, False
        #Default: False
        #Description: Whether to remove unused material slots before adding new one
        #make_active: Make new slot the active slot
        #Values: True, False
        #Default: True
        #Description: Whether to make the new slot the active material slot
        #assign_all_faces: Assign material to all faces
        #Values: True, False
        #Default: False
        #Description: Whether to assign this material to all faces of the object
        # Input variables
        #target_object = None
        #material_to_assign = None
        #clear_unused = False
        #make_active = True
        #assign_all_faces = False
        # Output variables
        success = False
        error_message = ""
        slot_index = -1
        try:
           print(f"Processing material slots for object: {target_object.name}")
           # Clear unused materials if requested
           if clear_unused:
               print("Clearing unused materials...")
               # Get initial slot count
               initial_slot_count = len(target_object.material_slots)
               print(f"Initial material slots: {initial_slot_count}")
               # Remove slots that have no material assigned
               for i in range(len(target_object.material_slots) - 1, -1, -1):
                   if target_object.material_slots[i].material is None:
                       target_object.data.materials.pop(index=i)
                       print(f"Removed empty slot at index {i}")
               # Check remaining slots for usage
               if hasattr(target_object.data, "polygons"):
                   used_indices = {p.material_index for p in target_object.data.polygons}
                   print(f"Found used material indices: {used_indices}")
                   # Remove unused slots from highest index to lowest
                   for i in range(len(target_object.material_slots) - 1, -1, -1):
                       if i not in used_indices:
                           target_object.data.materials.pop(index=i)
                           print(f"Removed unused slot at index {i}")
               # Report cleanup results
               final_slot_count = len(target_object.material_slots)
               removed_count = initial_slot_count - final_slot_count
               print(f"Removed {removed_count} unused slots. Remaining slots: {final_slot_count}")
           # Add new material slot
           target_object.data.materials.append(None)
           slot_index = len(target_object.data.materials) - 1
           print(f"Created new slot at index: {slot_index}")
           # Assign material to the new slot
           target_object.data.materials[slot_index] = material_to_assign
           print(f"Assigned material: {material_to_assign.name}")
           # Assign this material slot to all polygons if requested
           if assign_all_faces and hasattr(target_object.data, "polygons"):
               print("Assigning material to all faces...")
               for polygon in target_object.data.polygons:
                   polygon.material_index = slot_index
               print(f"Assigned material index {slot_index} to {len(target_object.data.polygons)} faces")
           # Make slot active if requested
           if make_active:
               target_object.active_material_index = slot_index
               print("Set as active material slot")
           success = True
           print("Material slot assignment completed successfully")
        except Exception as e:
           error_message = str(e)
           print(f"Error assigning material slot: {error_message}")
           slot_index = -1
        if (property_exists("bpy.context.scene.sna_ebc_scene_properties.combined_bake_material.node_tree.nodes", globals(), locals()) and 'Principled BSDF' in bpy.context.scene.sna_ebc_scene_properties.combined_bake_material.node_tree.nodes):
            if (property_exists("bpy.context.scene.sna_ebc_scene_properties.combined_bake_material.node_tree.nodes", globals(), locals()) and 'Normal Map' in bpy.context.scene.sna_ebc_scene_properties.combined_bake_material.node_tree.nodes):
                for i_927EE in range(len(bpy.context.scene.sna_ebc_scene_properties.combined_bake_material.node_tree.nodes)):
                    if 'Combined_Bake_DIFFUSE' in bpy.context.scene.sna_ebc_scene_properties.combined_bake_material.node_tree.nodes[i_927EE].name:
                        if (bpy.context.scene.sna_ebc_scene_properties.baked_diffuse_image == None):
                            pass
                        else:
                            bpy.context.scene.sna_ebc_scene_properties.combined_bake_material.node_tree.nodes[i_927EE].image = bpy.context.scene.sna_ebc_scene_properties.baked_diffuse_image
                    if 'Combined_Bake_ROUGHNESS' in bpy.context.scene.sna_ebc_scene_properties.combined_bake_material.node_tree.nodes[i_927EE].name:
                        if (bpy.context.scene.sna_ebc_scene_properties.baked_roughness_image == None):
                            pass
                        else:
                            bpy.context.scene.sna_ebc_scene_properties.combined_bake_material.node_tree.nodes[i_927EE].image = bpy.context.scene.sna_ebc_scene_properties.baked_roughness_image
                    if 'Combined_Bake_NORMAL' in bpy.context.scene.sna_ebc_scene_properties.combined_bake_material.node_tree.nodes[i_927EE].name:
                        if (bpy.context.scene.sna_ebc_scene_properties.baked_normal_image == None):
                            pass
                        else:
                            bpy.context.scene.sna_ebc_scene_properties.combined_bake_material.node_tree.nodes[i_927EE].image = bpy.context.scene.sna_ebc_scene_properties.baked_normal_image
                    target_object = bpy.context.view_layer.objects.active
                    remove_empty = True
                    remove_unused = True
                    # REMOVE UNUSED MATERIALS
                    # Removes unused material slots from an object (empty slots and slots not used by any polygons)
                    #target_object: Object to clean materials from
                    #Type: Pointer
                    #Pointer: bpy.types.Object
                    #Description: Target object to remove unused materials from
                    #remove_empty: Remove slots with no material assigned
                    #Values: True, False
                    #Default: True
                    #Description: Whether to remove slots that have no material assigned
                    #remove_unused: Remove slots not used by any polygons
                    #Values: True, False
                    #Default: True
                    #Description: Whether to remove slots that aren't used by any faces
                    # Input variables
                    #target_object = None
                    #remove_empty = True
                    #remove_unused = True
                    # Output variables
                    success = False
                    error_message = ""
                    removed_count = 0
                    try:
                        print(f"Cleaning materials for object: {target_object.name}")
                        initial_slot_count = len(target_object.material_slots)
                        print(f"Initial material slots: {initial_slot_count}")
                        # First pass: Remove empty slots
                        if remove_empty:
                            print("Checking for empty slots...")
                            for i in range(len(target_object.material_slots) - 1, -1, -1):
                                if target_object.material_slots[i].material is None:
                                    target_object.data.materials.pop(index=i)
                                    print(f"Removed empty slot at index {i}")
                                    removed_count += 1
                        # Second pass: Remove unused slots
                        if remove_unused and hasattr(target_object.data, "polygons"):
                            print("Checking for unused slots...")
                            used_indices = {p.material_index for p in target_object.data.polygons}
                            print(f"Found used material indices: {used_indices}")
                            for i in range(len(target_object.material_slots) - 1, -1, -1):
                                if i not in used_indices:
                                    target_object.data.materials.pop(index=i)
                                    print(f"Removed unused slot at index {i}")
                                    removed_count += 1
                        final_slot_count = len(target_object.material_slots)
                        print(f"Removed {removed_count} slots total")
                        print(f"Final material slot count: {final_slot_count}")
                        success = True
                    except Exception as e:
                        error_message = str(e)
                        print(f"Error cleaning materials: {error_message}")
                        removed_count = 0
            else:
                self.report({'ERROR'}, message='Normal Map node not found in Combined Bake material')
        else:
            self.report({'ERROR'}, message='Principled BSDF not found in Combined Bake material')
        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout
        box_488F8 = layout.box()
        box_488F8.alert = False
        box_488F8.enabled = True
        box_488F8.active = True
        box_488F8.use_property_split = False
        box_488F8.use_property_decorate = False
        box_488F8.alignment = 'Expand'.upper()
        box_488F8.scale_x = 1.0
        box_488F8.scale_y = 1.0
        if not True: box_488F8.operator_context = "EXEC_DEFAULT"
        box_ABB21 = box_488F8.box()
        box_ABB21.alert = False
        box_ABB21.enabled = True
        box_ABB21.active = True
        box_ABB21.use_property_split = False
        box_ABB21.use_property_decorate = False
        box_ABB21.alignment = 'Expand'.upper()
        box_ABB21.scale_x = 1.0
        box_ABB21.scale_y = 1.0
        if not True: box_ABB21.operator_context = "EXEC_DEFAULT"
        box_ABB21.label(text='All faces on the active object will be set to', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'tips-one.svg')))
        box_ABB21.label(text="use the 'Combined_Bake' material", icon_value=0)
        box_F2AC4 = box_488F8.box()
        box_F2AC4.alert = False
        box_F2AC4.enabled = True
        box_F2AC4.active = True
        box_F2AC4.use_property_split = False
        box_F2AC4.use_property_decorate = False
        box_F2AC4.alignment = 'Expand'.upper()
        box_F2AC4.scale_x = 1.0
        box_F2AC4.scale_y = 1.0
        if not True: box_F2AC4.operator_context = "EXEC_DEFAULT"
        box_F2AC4.label(text='Combined Bake Material', icon_value=0)
        box_F2AC4.prop_search(bpy.context.scene.sna_ebc_scene_properties, 'combined_bake_material', bpy.data, 'materials', text='', icon='NONE')
        box_9D0E3 = box_488F8.box()
        box_9D0E3.alert = False
        box_9D0E3.enabled = True
        box_9D0E3.active = True
        box_9D0E3.use_property_split = False
        box_9D0E3.use_property_decorate = False
        box_9D0E3.alignment = 'Expand'.upper()
        box_9D0E3.scale_x = 1.0
        box_9D0E3.scale_y = 1.0
        if not True: box_9D0E3.operator_context = "EXEC_DEFAULT"
        box_9D0E3.label(text='Baked Diffuse Texture', icon_value=0)
        box_9D0E3.prop(bpy.context.scene.sna_ebc_scene_properties, 'baked_diffuse_image', text='', icon_value=0, emboss=True)
        box_9D0E3.label(text='Baked Roughness Texture', icon_value=0)
        box_9D0E3.prop(bpy.context.scene.sna_ebc_scene_properties, 'baked_roughness_image', text='', icon_value=0, emboss=True)
        box_9D0E3.label(text='Baked Normal Texture', icon_value=0)
        box_9D0E3.prop(bpy.context.scene.sna_ebc_scene_properties, 'baked_normal_image', text='', icon_value=0, emboss=True)

    def invoke(self, context, event):
        if (property_exists("bpy.data.materials", globals(), locals()) and 'EBC_Combined_Bake_Material' in bpy.data.materials):
            bpy.context.scene.sna_ebc_scene_properties.combined_bake_material = bpy.data.materials['EBC_Combined_Bake_Material']
        return context.window_manager.invoke_props_dialog(self, width=400)


class SNA_OT_Bake_To_Patch_Fa828(bpy.types.Operator):
    bl_idname = "sna.bake_to_patch_fa828"
    bl_label = "Bake To Patch"
    bl_description = "Bakes from the active object to the assigned bake patch material."
    bl_options = {"REGISTER", "UNDO"}
    sna_bake_samples: bpy.props.IntProperty(name='Bake Samples', description='', default=10, subtype='NONE', min=1)
    sna_bake_diffuse: bpy.props.BoolProperty(name='Bake Diffuse', description='', default=False)
    sna_bake_roughness: bpy.props.BoolProperty(name='Bake Roughness', description='', default=False)
    sna_bake_normal: bpy.props.BoolProperty(name='Bake Normal', description='', default=False)

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        if ((not self.sna_bake_diffuse) and (not self.sna_bake_roughness) and (not self.sna_bake_normal)):
            self.report({'INFO'}, message='No bake passes selected - no changes made')
        else:
            target_object = bpy.context.scene.sna_ebc_scene_properties.bake_base_object
            material_to_assign = bpy.context.scene.sna_ebc_scene_properties.bake_patch_material
            make_active = True
            clear_unused = True
            assign_all_faces = False
            # ASSIGN NEW MATERIAL SLOT
            # Adds a new material slot to an object and assigns the specified material to it with optional face assignment
            #target_object: Object to add material slot to
            #Type: Pointer
            #Pointer: bpy.types.Object
            #Description: Target object that will receive the new material slot
            #material_to_assign: Material to assign to new slot
            #Type: Pointer
            #Pointer: bpy.types.Material
            #Description: Material that will be assigned to the new slot
            #clear_unused: Clear unused materials first
            #Values: True, False
            #Default: False
            #Description: Whether to remove unused material slots before adding new one
            #make_active: Make new slot the active slot
            #Values: True, False
            #Default: True
            #Description: Whether to make the new slot the active material slot
            #assign_all_faces: Assign material to all faces
            #Values: True, False
            #Default: False
            #Description: Whether to assign this material to all faces of the object
            # Input variables
            #target_object = None
            #material_to_assign = None
            #clear_unused = False
            #make_active = True
            #assign_all_faces = False
            # Output variables
            success = False
            error_message = ""
            slot_index = -1
            try:
               print(f"Processing material slots for object: {target_object.name}")
               # Clear unused materials if requested
               if clear_unused:
                   print("Clearing unused materials...")
                   # Get initial slot count
                   initial_slot_count = len(target_object.material_slots)
                   print(f"Initial material slots: {initial_slot_count}")
                   # Remove slots that have no material assigned
                   for i in range(len(target_object.material_slots) - 1, -1, -1):
                       if target_object.material_slots[i].material is None:
                           target_object.data.materials.pop(index=i)
                           print(f"Removed empty slot at index {i}")
                   # Check remaining slots for usage
                   if hasattr(target_object.data, "polygons"):
                       used_indices = {p.material_index for p in target_object.data.polygons}
                       print(f"Found used material indices: {used_indices}")
                       # Remove unused slots from highest index to lowest
                       for i in range(len(target_object.material_slots) - 1, -1, -1):
                           if i not in used_indices:
                               target_object.data.materials.pop(index=i)
                               print(f"Removed unused slot at index {i}")
                   # Report cleanup results
                   final_slot_count = len(target_object.material_slots)
                   removed_count = initial_slot_count - final_slot_count
                   print(f"Removed {removed_count} unused slots. Remaining slots: {final_slot_count}")
               # Add new material slot
               target_object.data.materials.append(None)
               slot_index = len(target_object.data.materials) - 1
               print(f"Created new slot at index: {slot_index}")
               # Assign material to the new slot
               target_object.data.materials[slot_index] = material_to_assign
               print(f"Assigned material: {material_to_assign.name}")
               # Assign this material slot to all polygons if requested
               if assign_all_faces and hasattr(target_object.data, "polygons"):
                   print("Assigning material to all faces...")
                   for polygon in target_object.data.polygons:
                       polygon.material_index = slot_index
                   print(f"Assigned material index {slot_index} to {len(target_object.data.polygons)} faces")
               # Make slot active if requested
               if make_active:
                   target_object.active_material_index = slot_index
                   print("Set as active material slot")
               success = True
               print("Material slot assignment completed successfully")
            except Exception as e:
               error_message = str(e)
               print(f"Error assigning material slot: {error_message}")
               slot_index = -1
            bpy.context.scene.render.engine = 'CYCLES'
            bpy.context.scene.cycles.use_denoising = False
            bpy.context.scene.cycles.samples = self.sna_bake_samples
            for i_99343 in range(len(bpy.context.scene.objects)):
                bpy.context.scene.objects[i_99343].select_set(state=False, view_layer=bpy.context.view_layer, )
            bpy.context.scene.sna_ebc_scene_properties.bake_base_object.select_set(state=True, view_layer=bpy.context.view_layer, )
            bpy.context.scene.sna_ebc_scene_properties.bake_patch_object.select_set(state=True, view_layer=bpy.context.view_layer, )
            bpy.context.view_layer.objects.active = bpy.context.scene.sna_ebc_scene_properties.bake_patch_object
            ebctexturebake_patch['sna_ebc_bake_type_list'] = []
            if self.sna_bake_diffuse:
                ebctexturebake_patch['sna_ebc_bake_type_list'].append('DIFFUSE')
            if self.sna_bake_roughness:
                ebctexturebake_patch['sna_ebc_bake_type_list'].append('ROUGHNESS')
            if self.sna_bake_normal:
                ebctexturebake_patch['sna_ebc_bake_type_list'].append('NORMAL')
            ebctexturebake_patch['sna_ebc_bake_count'] = 0

            def delayed_F7E06():
                is_baking = None
                is_baking = bpy.app.is_job_running("OBJECT_BAKE")
                if is_baking:
                    pass
                else:
                    for i_D2F31 in range(len(bpy.context.scene.sna_ebc_scene_properties.bake_patch_material.node_tree.nodes)):
                        if ebctexturebake_patch['sna_ebc_bake_type_list'][ebctexturebake_patch['sna_ebc_bake_count']] + '_Image_Node' in bpy.context.scene.sna_ebc_scene_properties.bake_patch_material.node_tree.nodes[i_D2F31].name:
                            bpy.context.scene.sna_ebc_scene_properties.bake_patch_material.node_tree.nodes.active = bpy.context.scene.sna_ebc_scene_properties.bake_patch_material.node_tree.nodes[i_D2F31]
                            bpy.context.scene.sna_ebc_scene_properties.bake_patch_material.node_tree.nodes[i_D2F31].select = True
                            ebctexturebake_patch['sna_ebc_active_bake_node'] = bpy.context.scene.sna_ebc_scene_properties.bake_patch_material.node_tree.nodes[i_D2F31]
                            for i_6728E in range(len(bpy.context.scene.sna_ebc_scene_properties.bake_patch_material.node_tree.nodes[i_D2F31].outputs[0].links)-1,-1,-1):
                                bpy.context.scene.sna_ebc_scene_properties.bake_patch_material.node_tree.links.remove(link=bpy.context.scene.sna_ebc_scene_properties.bake_patch_material.node_tree.nodes[i_D2F31].outputs[0].links[i_6728E], )
                        else:
                            bpy.context.scene.sna_ebc_scene_properties.bake_patch_material.node_tree.nodes[i_D2F31].select = False
                    bpy.ops.object.bake('INVOKE_DEFAULT', type=ebctexturebake_patch['sna_ebc_bake_type_list'][ebctexturebake_patch['sna_ebc_bake_count']], pass_filter=set([('COLOR' if (ebctexturebake_patch['sna_ebc_bake_type_list'][ebctexturebake_patch['sna_ebc_bake_count']] == 'DIFFUSE') else 'NONE')]), margin=16, use_selected_to_active=True, max_ray_distance=0.0, cage_extrusion=1.0, normal_space='TANGENT', normal_r='POS_X', normal_g='POS_Y', normal_b='POS_Z', target='IMAGE_TEXTURES', save_mode='INTERNAL', use_clear=True)
                    ebctexturebake_patch['sna_ebc_bake_count'] += 1
                if (ebctexturebake_patch['sna_ebc_bake_count'] == len(ebctexturebake_patch['sna_ebc_bake_type_list'])):
                    return None
                return 0.10000000149011612
            bpy.app.timers.register(delayed_F7E06, first_interval=0.0)
        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout
        box_1DD24 = layout.box()
        box_1DD24.alert = False
        box_1DD24.enabled = True
        box_1DD24.active = True
        box_1DD24.use_property_split = False
        box_1DD24.use_property_decorate = False
        box_1DD24.alignment = 'Expand'.upper()
        box_1DD24.scale_x = 1.0
        box_1DD24.scale_y = 1.0
        if not True: box_1DD24.operator_context = "EXEC_DEFAULT"
        box_1DD24.label(text='Bake Settings', icon_value=0)
        box_DE272 = box_1DD24.box()
        box_DE272.alert = False
        box_DE272.enabled = True
        box_DE272.active = True
        box_DE272.use_property_split = False
        box_DE272.use_property_decorate = False
        box_DE272.alignment = 'Expand'.upper()
        box_DE272.scale_x = 1.0
        box_DE272.scale_y = 1.0
        if not True: box_DE272.operator_context = "EXEC_DEFAULT"
        box_DE272.prop_search(bpy.context.scene.sna_ebc_scene_properties, 'bake_base_object', bpy.data, 'objects', text='Base Object', icon='NONE')
        box_DE272.prop_search(bpy.context.scene.sna_ebc_scene_properties, 'bake_patch_object', bpy.data, 'objects', text='Bake Patch', icon='NONE')
        box_DE272.prop_search(bpy.context.scene.sna_ebc_scene_properties, 'bake_patch_material', bpy.data, 'objects', text='Bake Patch Material', icon='NONE')
        box_19C7C = box_1DD24.box()
        box_19C7C.alert = False
        box_19C7C.enabled = True
        box_19C7C.active = True
        box_19C7C.use_property_split = False
        box_19C7C.use_property_decorate = False
        box_19C7C.alignment = 'Expand'.upper()
        box_19C7C.scale_x = 1.0
        box_19C7C.scale_y = 1.0
        if not True: box_19C7C.operator_context = "EXEC_DEFAULT"
        box_19C7C.prop(bpy.context.scene.cycles, 'device', text='Bake Device', icon_value=0, emboss=True)
        box_19C7C.prop(self, 'sna_bake_samples', text='Bake Samples', icon_value=0, emboss=True)
        box_C4A56 = box_1DD24.box()
        box_C4A56.alert = False
        box_C4A56.enabled = True
        box_C4A56.active = True
        box_C4A56.use_property_split = False
        box_C4A56.use_property_decorate = False
        box_C4A56.alignment = 'Expand'.upper()
        box_C4A56.scale_x = 1.0
        box_C4A56.scale_y = 1.0
        if not True: box_C4A56.operator_context = "EXEC_DEFAULT"
        box_C4A56.prop(self, 'sna_bake_diffuse', text='Bake Diffuse', icon_value=0, emboss=True)
        box_C4A56.prop(self, 'sna_bake_roughness', text='Bake Roughness', icon_value=0, emboss=True)
        box_C4A56.prop(self, 'sna_bake_normal', text='Bake Normal', icon_value=0, emboss=True)

    def invoke(self, context, event):
        bpy.context.scene.sna_ebc_scene_properties.bake_base_object = bpy.context.view_layer.objects.active
        return context.window_manager.invoke_props_dialog(self, width=500)


class SNA_OT_Add_Bake_Patch_68526(bpy.types.Operator):
    bl_idname = "sna.add_bake_patch_68526"
    bl_label = "Add Bake Patch"
    bl_description = "Adds a mesh plane meant for baking."
    bl_options = {"REGISTER", "UNDO"}

    def sna_bake_patch_resolution_enum_items(self, context):
        return [("No Items", "No Items", "No generate enum items node found to create items!", "ERROR", 0)]
    sna_bake_patch_resolution: bpy.props.EnumProperty(name='Bake Patch Resolution', description='', items=[('1K', '1K', '', 0, 0), ('2K', '2K', '', 0, 1), ('4K', '4K', '', 0, 2)])

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        ebctexturebake_patch['sna_ebc_temp_store_active_object'] = bpy.context.view_layer.objects.active
        before_data = list(bpy.data.objects)
        bpy.ops.wm.append(directory=os.path.join(os.path.dirname(__file__), 'assets', 'KIRI_Edit_By_Colour_OBJECT_APPEND.blend') + r'\Object', filename=self.sna_bake_patch_resolution + '_Bake_Patch', link=False)
        new_data = list(filter(lambda d: not d in before_data, list(bpy.data.objects)))
        appended_42718 = None if not new_data else new_data[0]
        appended_42718.location = bpy.context.scene.cursor.location
        appended_42718.rotation_mode = 'QUATERNION'
        bpy.context.scene.cursor.rotation_mode = 'QUATERNION'
        appended_42718.rotation_quaternion = bpy.context.scene.cursor.rotation_quaternion
        modifier_49CBF = appended_42718.modifiers.new(name='Bake Patch Shrinkwrap', type='SHRINKWRAP', )
        modifier_49CBF.target = ebctexturebake_patch['sna_ebc_temp_store_active_object']
        modifier_49CBF.wrap_method = 'PROJECT'
        modifier_49CBF.use_negative_direction = True
        bpy.context.view_layer.objects.active = appended_42718
        bpy.context.scene.sna_ebc_scene_properties.bake_patch_material = appended_42718.material_slots[0].material
        bpy.context.scene.sna_ebc_scene_properties.bake_patch_object = appended_42718
        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout
        box_02260 = layout.box()
        box_02260.alert = False
        box_02260.enabled = True
        box_02260.active = True
        box_02260.use_property_split = False
        box_02260.use_property_decorate = False
        box_02260.alignment = 'Expand'.upper()
        box_02260.scale_x = 1.0
        box_02260.scale_y = 1.0
        if not True: box_02260.operator_context = "EXEC_DEFAULT"
        box_523A4 = box_02260.box()
        box_523A4.alert = False
        box_523A4.enabled = True
        box_523A4.active = True
        box_523A4.use_property_split = False
        box_523A4.use_property_decorate = False
        box_523A4.alignment = 'Expand'.upper()
        box_523A4.scale_x = 1.0
        box_523A4.scale_y = 1.0
        if not True: box_523A4.operator_context = "EXEC_DEFAULT"
        box_523A4.label(text='The active object will be set as the target', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'tips-one.svg')))
        box_523A4.label(text='Place 3D cursor first for best results', icon_value=0)
        box_02260.label(text='Bake Patch settings', icon_value=0)
        box_02260.prop(self, 'sna_bake_patch_resolution', text='Bake Patch resolution', icon_value=0, emboss=True)

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=500)


def sna_bake_patch_function_interface_834B3(layout_function, ):
    box_2279C = layout_function.box()
    box_2279C.alert = False
    box_2279C.enabled = True
    box_2279C.active = True
    box_2279C.use_property_split = False
    box_2279C.use_property_decorate = False
    box_2279C.alignment = 'Expand'.upper()
    box_2279C.scale_x = 1.0
    box_2279C.scale_y = 1.0
    if not True: box_2279C.operator_context = "EXEC_DEFAULT"
    box_2279C.label(text='Patch Baking', icon_value=0)
    op = box_2279C.operator('sna.add_bake_patch_68526', text='Add Bake Patch', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'plus-circle.svg')), emboss=True, depress=False)
    op.sna_bake_patch_resolution = '1K'
    op = box_2279C.operator('sna.bake_to_patch_fa828', text='Bake To Patch', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'patch-20-regular.svg')), emboss=True, depress=False)
    op.sna_bake_samples = 10
    op.sna_bake_diffuse = False
    op.sna_bake_roughness = False
    op.sna_bake_normal = False
    op = box_2279C.operator('sna.link_baked_textures_patch_067f8', text='Link Baked Textures', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'link.svg')), emboss=True, depress=False)
    op.sna_link_diffuse = True
    op.sna_link_roughness = False
    op.sna_link_normal = False


class SNA_OT_Link_Baked_Textures_Patch_067F8(bpy.types.Operator):
    bl_idname = "sna.link_baked_textures_patch_067f8"
    bl_label = "Link Baked Textures (Patch)"
    bl_description = "Re-links all newly baked and selected bake patch textures"
    bl_options = {"REGISTER", "UNDO"}
    sna_link_diffuse: bpy.props.BoolProperty(name='Link Diffuse', description='', default=False)
    sna_link_roughness: bpy.props.BoolProperty(name='Link Roughness', description='', default=False)
    sna_link_normal: bpy.props.BoolProperty(name='Link Normal', description='', default=False)

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        if (property_exists("bpy.context.scene.sna_ebc_scene_properties.bake_patch_material.node_tree.nodes", globals(), locals()) and 'Principled BSDF' in bpy.context.scene.sna_ebc_scene_properties.bake_patch_material.node_tree.nodes):
            if (property_exists("bpy.context.scene.sna_ebc_scene_properties.bake_patch_material.node_tree.nodes", globals(), locals()) and 'Normal Map' in bpy.context.scene.sna_ebc_scene_properties.bake_patch_material.node_tree.nodes):
                for i_9DB58 in range(len(bpy.context.scene.sna_ebc_scene_properties.bake_patch_material.node_tree.nodes)):
                    if ('Patch_DIFFUSE' in bpy.context.scene.sna_ebc_scene_properties.bake_patch_material.node_tree.nodes[i_9DB58].name or 'Patch_ROUGHNESS' in bpy.context.scene.sna_ebc_scene_properties.bake_patch_material.node_tree.nodes[i_9DB58].name or 'Patch_NORMAL' in bpy.context.scene.sna_ebc_scene_properties.bake_patch_material.node_tree.nodes[i_9DB58].name):
                        if ('Patch_DIFFUSE' in bpy.context.scene.sna_ebc_scene_properties.bake_patch_material.node_tree.nodes[i_9DB58].name and self.sna_link_diffuse):
                            link_D38BE = bpy.context.scene.sna_ebc_scene_properties.bake_patch_material.node_tree.links.new(input=bpy.context.scene.sna_ebc_scene_properties.bake_patch_material.node_tree.nodes['Principled BSDF'].inputs[0], output=bpy.context.scene.sna_ebc_scene_properties.bake_patch_material.node_tree.nodes[i_9DB58].outputs[0], )
                        if ('Patch_ROUGHNESS' in bpy.context.scene.sna_ebc_scene_properties.bake_patch_material.node_tree.nodes[i_9DB58].name and self.sna_link_roughness):
                            link_9765A = bpy.context.scene.sna_ebc_scene_properties.bake_patch_material.node_tree.links.new(input=bpy.context.scene.sna_ebc_scene_properties.bake_patch_material.node_tree.nodes['Principled BSDF'].inputs[2], output=bpy.context.scene.sna_ebc_scene_properties.bake_patch_material.node_tree.nodes[i_9DB58].outputs[0], )
                        if ('Patch_NORMAL' in bpy.context.scene.sna_ebc_scene_properties.bake_patch_material.node_tree.nodes[i_9DB58].name and self.sna_link_normal):
                            link_6D43C = bpy.context.scene.sna_ebc_scene_properties.bake_patch_material.node_tree.links.new(input=bpy.context.scene.sna_ebc_scene_properties.bake_patch_material.node_tree.nodes['Normal Map'].inputs[1], output=bpy.context.scene.sna_ebc_scene_properties.bake_patch_material.node_tree.nodes[i_9DB58].outputs[0], )
            else:
                self.report({'ERROR'}, message='Normal Map node not found in Bake Patch Material')
        else:
            self.report({'ERROR'}, message='Principled BSDF not found in Bake Patch Material')
        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout
        box_343B1 = layout.box()
        box_343B1.alert = False
        box_343B1.enabled = True
        box_343B1.active = True
        box_343B1.use_property_split = False
        box_343B1.use_property_decorate = False
        box_343B1.alignment = 'Expand'.upper()
        box_343B1.scale_x = 1.0
        box_343B1.scale_y = 1.0
        if not True: box_343B1.operator_context = "EXEC_DEFAULT"
        box_CDF97 = box_343B1.box()
        box_CDF97.alert = False
        box_CDF97.enabled = True
        box_CDF97.active = True
        box_CDF97.use_property_split = False
        box_CDF97.use_property_decorate = False
        box_CDF97.alignment = 'Expand'.upper()
        box_CDF97.scale_x = 1.0
        box_CDF97.scale_y = 1.0
        if not True: box_CDF97.operator_context = "EXEC_DEFAULT"
        box_CDF97.prop_search(bpy.context.scene.sna_ebc_scene_properties, 'bake_patch_object', bpy.data, 'objects', text='Bake Patch', icon='NONE')
        box_CDF97.prop_search(bpy.context.scene.sna_ebc_scene_properties, 'bake_patch_material', bpy.data, 'objects', text='Bake Patch Material', icon='NONE')
        box_F4CB0 = box_343B1.box()
        box_F4CB0.alert = False
        box_F4CB0.enabled = True
        box_F4CB0.active = True
        box_F4CB0.use_property_split = False
        box_F4CB0.use_property_decorate = False
        box_F4CB0.alignment = 'Expand'.upper()
        box_F4CB0.scale_x = 1.0
        box_F4CB0.scale_y = 1.0
        if not True: box_F4CB0.operator_context = "EXEC_DEFAULT"
        box_F4CB0.prop(self, 'sna_link_diffuse', text='Link Diffuse', icon_value=0, emboss=True)
        box_F4CB0.prop(self, 'sna_link_roughness', text='Link Roughness', icon_value=0, emboss=True)
        box_F4CB0.prop(self, 'sna_link_normal', text='Link Normal', icon_value=0, emboss=True)

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=500)


class SNA_GROUP_sna_ebc_scene_property_group(bpy.types.PropertyGroup):
    colour_selection: bpy.props.FloatVectorProperty(name='Colour_Selection', description='', size=4, default=(0.0, 0.0, 0.0, 0.0), subtype='NONE', unit='NONE', step=3, precision=6)
    active_menu_full: bpy.props.EnumProperty(name='Active_Menu_Full', description='', items=[('Colour Selection', 'Colour Selection', '', 0, 0), ('Texture', 'Texture', '', 0, 1), ('Edit Mesh', 'Edit Mesh', '', 0, 2), ('Sculpt', 'Sculpt', '', 0, 3)])
    active_menu_retopo_loops: bpy.props.EnumProperty(name='Active_Menu_Retopo_Loops', description='', items=[('Colour Selection', 'Colour Selection', '', 0, 0), ('Retopo Loops', 'Retopo Loops', '', 0, 1)])
    bake_patch_material: bpy.props.PointerProperty(name='Bake_Patch_Material', description='', type=bpy.types.Material)
    base_material: bpy.props.PointerProperty(name='Base_Material', description='', type=bpy.types.Material)
    bake_base_object: bpy.props.PointerProperty(name='Bake_Base_Object', description='', type=bpy.types.Object)
    bake_patch_object: bpy.props.PointerProperty(name='Bake_Patch_Object', description='', type=bpy.types.Object)
    combined_bake_material: bpy.props.PointerProperty(name='Combined_Bake_Material', description='', type=bpy.types.Material)
    baked_diffuse_image: bpy.props.PointerProperty(name='Baked_DIFFUSE_Image', description='', type=bpy.types.Image)
    baked_roughness_image: bpy.props.PointerProperty(name='Baked_ROUGHNESS_Image', description='', type=bpy.types.Image)
    baked_normal_image: bpy.props.PointerProperty(name='Baked_NORMAL_Image', description='', type=bpy.types.Image)


class SNA_GROUP_sna_ebc_object_property_group(bpy.types.PropertyGroup):
    live_effects_proxy_switch: bpy.props.EnumProperty(name='Live_Effects_Proxy_Switch', description='', items=[('None', 'None', '', 0, 0), ('Delete Faces', 'Delete Faces', '', 0, 1), ('Smooth', 'Smooth', '', 0, 2), ('Set Material', 'Set Material', '', 0, 3), ('Smooth and Set Material', 'Smooth and Set Material', '', 0, 4), ('Retopo Loops', 'Retopo Loops', '', 0, 5)], update=sna_update_live_effects_proxy_switch_52B23)


def register():
    global _icons
    _icons = bpy.utils.previews.new()
    bpy.utils.register_class(SNA_GROUP_sna_ebc_scene_property_group)
    bpy.utils.register_class(SNA_GROUP_sna_ebc_object_property_group)
    bpy.types.Scene.sna_ebc_scene_properties = bpy.props.PointerProperty(name='EBC Scene Properties', description='', type=SNA_GROUP_sna_ebc_scene_property_group)
    bpy.types.Object.sna_ebc_object_properties = bpy.props.PointerProperty(name='EBC Object Properties', description='', type=SNA_GROUP_sna_ebc_object_property_group)
    bpy.utils.register_class(SNA_OT_Remove_Edit_By_Colour_Modifier_C523D)
    bpy.utils.register_class(SNA_OT_Add_Edit_By_Colour_Modifier_381C0)
    bpy.utils.register_class(SNA_OT_Apply_Edit_By_Colour_Modifier_45130)
    bpy.utils.register_class(SNA_OT_Add_Wire_Cube_24Ccd)
    bpy.utils.register_class(SNA_OT_Edit_By_Colour__Select_77Ba8)
    bpy.utils.register_class(SNA_OT_Edit_By_Colour__Split_819Ad)
    bpy.utils.register_class(SNA_OT_Edit_By_Colour__Duplicate_F7267)
    bpy.utils.register_class(SNA_OT_Apply_Retopo_Loops_7Ea68)
    bpy.utils.register_class(SNA_OT_Selection_To_Face_Sets_69A50)
    bpy.utils.register_class(SNA_PT_EDIT_BY_COLOUR_BY_KIRI_ENGINE_2BDB2)
    bpy.utils.register_class(SNA_OT_Dgs_Render_Launch_Kiri_Site_84772)
    bpy.utils.register_class(SNA_OT_Dgs_Render_Launch_Superhive_Store_0Bcb5)
    bpy.utils.register_class(SNA_OT_Dgs_Render_Launch_Kiri_Blender_Addons_Page_9427F)
    bpy.utils.register_class(SNA_OT_Dgs_Render_Open_Documentation_3B870)
    bpy.utils.register_class(SNA_OT_Dgs_Render_Open_Tutorial_Video_D0Cd5)
    bpy.utils.register_class(SNA_OT_Add_Ebc_Attribute_To_Selected_Material_3F5C9)
    bpy.utils.register_class(SNA_OT_Bake_Set_Material__Original_Dafdb)
    bpy.utils.register_class(SNA_OT_Switch_To_Combined_Bake_Material_A7D5F)
    bpy.utils.register_class(SNA_OT_Bake_To_Patch_Fa828)
    bpy.utils.register_class(SNA_OT_Add_Bake_Patch_68526)
    bpy.utils.register_class(SNA_OT_Link_Baked_Textures_Patch_067F8)


def unregister():
    global _icons
    bpy.utils.previews.remove(_icons)
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    for km, kmi in addon_keymaps.values():
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    del bpy.types.Object.sna_ebc_object_properties
    del bpy.types.Scene.sna_ebc_scene_properties
    bpy.utils.unregister_class(SNA_GROUP_sna_ebc_object_property_group)
    bpy.utils.unregister_class(SNA_GROUP_sna_ebc_scene_property_group)
    bpy.utils.unregister_class(SNA_OT_Remove_Edit_By_Colour_Modifier_C523D)
    bpy.utils.unregister_class(SNA_OT_Add_Edit_By_Colour_Modifier_381C0)
    bpy.utils.unregister_class(SNA_OT_Apply_Edit_By_Colour_Modifier_45130)
    bpy.utils.unregister_class(SNA_OT_Add_Wire_Cube_24Ccd)
    bpy.utils.unregister_class(SNA_OT_Edit_By_Colour__Select_77Ba8)
    bpy.utils.unregister_class(SNA_OT_Edit_By_Colour__Split_819Ad)
    bpy.utils.unregister_class(SNA_OT_Edit_By_Colour__Duplicate_F7267)
    bpy.utils.unregister_class(SNA_OT_Apply_Retopo_Loops_7Ea68)
    bpy.utils.unregister_class(SNA_OT_Selection_To_Face_Sets_69A50)
    bpy.utils.unregister_class(SNA_PT_EDIT_BY_COLOUR_BY_KIRI_ENGINE_2BDB2)
    bpy.utils.unregister_class(SNA_OT_Dgs_Render_Launch_Kiri_Site_84772)
    bpy.utils.unregister_class(SNA_OT_Dgs_Render_Launch_Superhive_Store_0Bcb5)
    bpy.utils.unregister_class(SNA_OT_Dgs_Render_Launch_Kiri_Blender_Addons_Page_9427F)
    bpy.utils.unregister_class(SNA_OT_Dgs_Render_Open_Documentation_3B870)
    bpy.utils.unregister_class(SNA_OT_Dgs_Render_Open_Tutorial_Video_D0Cd5)
    bpy.utils.unregister_class(SNA_OT_Add_Ebc_Attribute_To_Selected_Material_3F5C9)
    bpy.utils.unregister_class(SNA_OT_Bake_Set_Material__Original_Dafdb)
    bpy.utils.unregister_class(SNA_OT_Switch_To_Combined_Bake_Material_A7D5F)
    bpy.utils.unregister_class(SNA_OT_Bake_To_Patch_Fa828)
    bpy.utils.unregister_class(SNA_OT_Add_Bake_Patch_68526)
    bpy.utils.unregister_class(SNA_OT_Link_Baked_Textures_Patch_067F8)
