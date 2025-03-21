import bpy
from bpy.props import ( BoolProperty, FloatProperty, EnumProperty, StringProperty, IntProperty, PointerProperty, CollectionProperty )

from ...base.node import EG_PureNode
from ...socket.derived import EGS_Array, EGS_Set
from ...socket.primitive import EGS_Value


class PNY_ToFloat(EG_PureNode):
    """Event To Float Node"""
    
    bl_idname = "egn_python_to_float"
    bl_label = "To Float"
    bl_icon = "CENTER_ONLY"

    def init(self, context):
        self.add_in(EGS_Value.bl_idname, "value")
        self.add_out("NodeSocketFloat", "float") # bind: float -> on_float

    def on_float(self):
        return float(self.get_input_value("wildcard"))


class PNY_ToInteger(EG_PureNode):
    """Event To Integer Node"""
    
    bl_idname = "egn_python_to_integer"
    bl_label = "To Integer"
    bl_icon = "CENTER_ONLY"

    def init(self, context):
        self.add_in(EGS_Value.bl_idname, "value")
        self.add_out("NodeSocketInt", "int") # bind: int -> on_int

    def on_int(self):
        return int(self.get_input_value("value"))


class PNY_ToString(EG_PureNode):
    """Event To String Node"""
    
    bl_idname = "egn_python_to_string"
    bl_label = "To String"
    bl_icon = "CENTER_ONLY"

    def init(self, context):
        self.add_in(EGS_Value.bl_idname, "value")
        self.add_out("NodeSocketString", "string") # bind: string -> on_string

    def on_string(self):
        return str(self.get_input_value("value"))


class PNY_ArrayToSet(EG_PureNode):
    """Convert Array To Set Node"""
    
    bl_idname = "egn_python_array_to_set"
    bl_label = "Array To Set"
    bl_icon = "CENTER_ONLY"

    def init(self, context):
        self.add_in(EGS_Array.bl_idname, "array")
        self.add_out(EGS_Set.bl_idname, "set") # bind: set -> on_set

    def on_set(self):
        items = self.get_input_value("array")
        return set(items)


class PNY_SetToArray(EG_PureNode):
    """Convert Set To Array Node"""
    
    bl_idname = "egn_python_set_to_array"
    bl_label = "Set To Array"
    bl_icon = "CENTER_ONLY"

    def init(self, context):
        self.add_in(EGS_Set.bl_idname, "set")
        self.add_out(EGS_Array.bl_idname, "array") # bind: array -> on_array

    def on_array(self):
        items = self.get_input_value("set")
        return list(items)


classes = [
    PNY_ToInteger,
    PNY_ToString,
    PNY_ToFloat,
    PNY_ArrayToSet,
    PNY_SetToArray,
]