import bpy
from bpy.props import ( BoolProperty, FloatProperty, EnumProperty, StringProperty, IntProperty, PointerProperty, CollectionProperty )

from ..base.node import EG_Node
from ..base.library import create_enum


class EGN_LiteralInteger(EG_Node):
    """Event Literal Integer Node"""
    
    bl_idname = "EGN_LiteralInteger"
    bl_label = "Literal Integer"

    node_is_pure = True

    value: IntProperty(name="Value") # type: ignore

    def init(self, context):
        self.add_out("EGS_Integer", "value")

    def on_value(self):
        return self.value
    
    def draw_buttons(self, context, layout):
        layout.prop(self, "value")


class EGN_LiteralFloat(EG_Node):
    """Event Literal Float Node"""
    
    bl_idname = "EGN_LiteralFloat"
    bl_label = "Literal Float"

    node_is_pure = True

    value: FloatProperty(name="Value") # type: ignore

    def init(self, context):
        self.add_out("EGS_Float", "value")

    def on_value(self):
        return self.value
    
    def draw_buttons(self, context, layout):
        layout.prop(self, "value")


class EGN_LiteralString(EG_Node):
    """Event Literal String Node"""
    
    bl_idname = "EGN_LiteralString"
    bl_label = "Literal String"

    node_is_pure = True

    value: StringProperty(name="Value") # type: ignore

    def init(self, context):
        self.add_out("EGS_String", "value")

    def on_value(self):
        return self.value
    
    def draw_buttons(self, context, layout):
        layout.prop(self, "value")


class EGN_LiteralBoolean(EG_Node):
    """Event Literal Boolean Node"""
    
    bl_idname = "EGN_LiteralBoolean"
    bl_label = "Literal Boolean"

    node_is_pure = True

    value: BoolProperty(name="Value") # type: ignore

    def init(self, context):
        self.add_out("EGS_Boolean", "value")

    def on_value(self):
        return self.value
    
    def draw_buttons(self, context, layout):
        layout.prop(self, "value")


classes = [
    EGN_LiteralInteger,
    EGN_LiteralFloat,
    EGN_LiteralString,
    EGN_LiteralBoolean,
]