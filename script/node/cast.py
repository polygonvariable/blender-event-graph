import bpy
from bpy.props import ( BoolProperty, FloatProperty, EnumProperty, StringProperty, IntProperty, PointerProperty, CollectionProperty )

from ..base.node import EG_Node
from ..base.library import create_enum

from ..socket.primitive import EGS_Value


class PNY_ToFloat(EG_Node):
    """Event To Float Node"""
    
    bl_idname = "PNY_ToFloat"
    bl_label = "To Float"

    node_is_pure = True

    def init(self, context):
        self.add_in(EGS_Value.bl_idname, "value")
        self.add_out("NodeSocketFloat", "result") # bind: result -> on_result

    def on_result(self):
        return float(self.get_input_value("wildcard"))


class PNY_ToInteger(EG_Node):
    """Event To Integer Node"""
    
    bl_idname = "PNY_ToInteger"
    bl_label = "To Integer"

    node_is_pure = True

    def init(self, context):
        self.add_in(EGS_Value.bl_idname, "value")
        self.add_out("NodeSocketInt", "result") # bind: result -> on_result

    def on_result(self):
        return int(self.get_input_value("value"))


class PNY_ToString(EG_Node):
    """Event To String Node"""
    
    bl_idname = "PNY_ToString"
    bl_label = "To String"

    node_is_pure = True

    def init(self, context):
        self.add_in(EGS_Value.bl_idname, "value")
        self.add_out("NodeSocketString", "result") # bind: result -> on_result

    def on_result(self):
        return str(self.get_input_value("value"))


classes = [
    PNY_ToInteger,
    PNY_ToString,
    PNY_ToFloat,
]