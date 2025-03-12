import bpy
from bpy.props import ( BoolProperty, FloatProperty, EnumProperty, StringProperty, IntProperty, PointerProperty, CollectionProperty, FloatVectorProperty )

from ...base.node import EG_Node, EG_PureNode
from ...base.library import get_linked_cache, remove_linked_cache, add_linked_cache, is_vector

from ...socket.user import EGS_Modifier
from ...socket.derived import EGS_Array
from ...socket.primitive import EGS_Value


class EGN_GetAllModifiers(EG_PureNode):
    """Get all modifiers of the object"""
    
    bl_idname = "egn_modifier_get_all"
    bl_label = "Get All Modifiers"
    bl_icon = "MOD_DECIM"

    def init(self, context):
        self.add_in("NodeSocketString", "object Id")
        self.add_out(socket=EGS_Modifier.bl_idname, name="modifiers", is_array=True) # bind: modifiers -> on_modifiers

    def on_modifiers(self):
        in_objectId = str(self.get_input_value("object Id"))
        bl_object = bpy.data.objects.get(in_objectId)
        
        if bl_object and bl_object.type == "MESH":
            return list(bl_object.modifiers)
        
        return []


class EGN_GetModifier(EG_PureNode):
    """Get a modifier at index of the object"""
    
    bl_idname = "egn_modifier_get"
    bl_label = "Get Modifier"
    bl_icon = "MOD_DECIM"

    def init(self, context):
        self.add_in("NodeSocketString", "object Id")
        self.add_in(socket="NodeSocketInt", name="index", hide_value=False)
        self.add_out(EGS_Modifier.bl_idname, "modifier") # bind: modifier -> on_modifier

    def on_modifier(self):
        in_objectId = str(self.get_input_value("object Id"))
        in_index = int(self.get_input_value("index"))

        bl_object = bpy.data.objects.get(in_objectId)

        if bl_object:
            if 0 <= in_index < len(bl_object.modifiers):
                return bl_object.modifiers[in_index]
        
        return ""


class EGN_FilterModifiers(EG_PureNode):
    """Filter modifier from list"""
    
    bl_idname = "egn_modifier_filter"
    bl_label = "Filter Modifiers"
    bl_icon = "MOD_DECIM"
    bl_width_default = 225

    prop_type: EnumProperty(
        name="Type",
        items=[(modifier.identifier, modifier.name, "") for modifier in bpy.types.Modifier.bl_rna.properties["type"].enum_items]
    ) # type: ignore

    def init(self, context):
        self.add_in(socket=EGS_Modifier.bl_idname, name="modifiers", is_array=True)
        self.add_out(socket=EGS_Modifier.bl_idname, name="modifiers", is_array=True) # bind: modifiers -> on_modifiers

    def draw_buttons(self, context, layout):
        layout.prop(self, "prop_type")

    def on_modifiers(self):
        in_modifiers = self.get_input_value("modifiers")
        if isinstance(in_modifiers, list):
            return [modifier for modifier in in_modifiers if modifier.type == self.prop_type]
        
        return []


class EGN_RemoveModifier(EG_Node):
    """Remove modifier from object"""
    
    bl_idname = "egn_modifier_remove"
    bl_label = "Remove Modifier"
    bl_icon = "MOD_DECIM"

    def init(self, context):
        self.add_exec_in("exec")
        self.add_in("NodeSocketString", "object Id")
        self.add_in(EGS_Modifier.bl_idname, "modifier")
        self.add_exec_out("success")
        self.add_exec_out("error")

    def execute(self):
        in_objectId = str(self.get_input_value("object Id"))
        in_modifier = self.get_input_value("modifier")

        bl_object = bpy.data.objects.get(in_objectId)

        if bl_object and in_modifier:
            bl_object.modifiers.remove(in_modifier)
            self.execute_next("success")
            return
        
        self.execute_next("error")


class EGN_RemoveModifierByIndex(EG_Node):
    """Remove modifier from object by index"""
    
    bl_idname = "egn_modifier_remove_by_index"
    bl_label = "Remove Modifier By Index"
    bl_icon = "MOD_DECIM"

    def init(self, context):
        self.add_exec_in("exec")
        self.add_in("NodeSocketString", "object Id")
        self.add_in(socket="NodeSocketInt", name="index", hide_value=False)
        self.add_exec_out("success")
        self.add_exec_out("error")

    def execute(self):
        in_objectId = str(self.get_input_value("object Id"))
        in_index = int(self.get_input_value("index"))

        bl_object = bpy.data.objects.get(in_objectId)

        if bl_object:
            if 0 <= in_index < len(bl_object.modifiers):
                bl_object.modifiers.remove(bl_object.modifiers[in_index])
                self.execute_next("success")
                return
        
        self.execute_next("error")


classes = [
    EGN_GetAllModifiers,
    EGN_GetModifier,
    EGN_FilterModifiers,
    EGN_RemoveModifier,
    EGN_RemoveModifierByIndex
]