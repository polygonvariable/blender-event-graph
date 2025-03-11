import bpy
from bpy.props import ( BoolProperty, FloatProperty, EnumProperty, StringProperty, IntProperty, PointerProperty, CollectionProperty, FloatVectorProperty )

from ...base.node import EG_PureNode
from ...base.library import create_enum

from ...socket.derived import EGS_Vector2D, EGS_Vector4D


class EGN_LiteralInteger(EG_PureNode):
    """Event Literal Integer Node"""
    
    bl_idname = "egn_python_literal_integer"
    bl_label = "Literal Integer"

    value: IntProperty(name="Value") # type: ignore

    def init(self, context):
        self.add_out("NodeSocketInt", "value")

    def on_value(self):
        return self.value
    
    def draw_buttons(self, context, layout):
        layout.prop(self, "value")


class EGN_LiteralFloat(EG_PureNode):
    """Event Literal Float Node"""
    
    bl_idname = "egn_python_literal_float"
    bl_label = "Literal Float"

    value: FloatProperty(name="Value") # type: ignore

    def init(self, context):
        self.add_out("NodeSocketFloat", "value")

    def on_value(self):
        return self.value
    
    def draw_buttons(self, context, layout):
        layout.prop(self, "value")


class EGN_LiteralColor(EG_PureNode):
    """Event Literal Color Node"""
    
    bl_idname = "egn_python_literal_color"
    bl_label = "Literal Color"

    value: FloatVectorProperty(
        name="Value",
        min=0.0,
        max=1.0,
        default=(1.0, 1.0, 1.0, 1.0),
        subtype="COLOR",
        size=4
    ) # type: ignore

    def init(self, context):
        self.add_out("NodeSocketColor", "value")

    def on_value(self):
        return self.value
    
    def draw_buttons(self, context, layout):
        layout.prop(self, "value")


class EGN_LiteralString(EG_PureNode):
    """Event Literal String Node"""
    
    bl_idname = "egn_python_literal_string"
    bl_label = "Literal String"

    value: StringProperty(name="Value") # type: ignore

    def init(self, context):
        self.add_out("NodeSocketString", "value")

    def on_value(self):
        return self.value
    
    def draw_buttons(self, context, layout):
        layout.prop(self, "value")


class EGN_LiteralBoolean(EG_PureNode):
    """Event Literal Boolean Node"""
    
    bl_idname = "egn_python_literal_boolean"
    bl_label = "Literal Boolean"

    value: BoolProperty(name="Value") # type: ignore

    def init(self, context):
        self.add_out("NodeSocketBool", "value")

    def on_value(self):
        return self.value
    
    def draw_buttons(self, context, layout):
        layout.prop(self, "value")


class PNY_Break2D(EG_PureNode):
    """Event Break 2D Vector Node"""
    
    bl_idname = "egn_python_break_2d"
    bl_label = "Break 2D Vector"

    def init(self, context):
        self.add_in(EGS_Vector2D.bl_idname, "vector")
        self.add_out("NodeSocketFloat", "x") # bind: x -> on_x
        self.add_out("NodeSocketFloat", "y") # bind: y -> on_y

    def on_x(self):
        return self.get_input_value("vector")[0]

    def on_y(self):
        return self.get_input_value("vector")[1]
    

class PNY_Break3D(EG_PureNode):
    """Event Break 3D Vector Node"""
    
    bl_idname = "egn_python_break_3d"
    bl_label = "Break 3D Vector"

    def init(self, context):
        self.add_in("NodeSocketVector", "vector")
        self.add_out("NodeSocketFloat", "x") # bind: x -> on_x
        self.add_out("NodeSocketFloat", "y") # bind: y -> on_y
        self.add_out("NodeSocketFloat", "z") # bind: z -> on_z

    def on_x(self):
        return self.get_input_value("vector")[0]

    def on_y(self):
        return self.get_input_value("vector")[1]

    def on_z(self):
        return self.get_input_value("vector")[2]


class PNY_Break4D(EG_PureNode):
    """Event Break 4D Vector Node"""
    
    bl_idname = "egn_python_break_4d"
    bl_label = "Break 4D Vector"

    def init(self, context):
        self.add_in(EGS_Vector4D.bl_idname, "vector")
        self.add_out("NodeSocketFloat", "x") # bind: x -> on_x
        self.add_out("NodeSocketFloat", "y") # bind: y -> on_y
        self.add_out("NodeSocketFloat", "z") # bind: z -> on_z
        self.add_out("NodeSocketFloat", "w") # bind: w -> on_w

    def on_x(self):
        return self.get_input_value("vector")[0]

    def on_y(self):
        return self.get_input_value("vector")[1]

    def on_z(self):
        return self.get_input_value("vector")[2]
    
    def on_w(self):
        return self.get_input_value("vector")[3]


class PNY_Make2D(EG_PureNode):
    """Event Make 2D Vector Node"""
    
    bl_idname = "egn_python_make_2d"
    bl_label = "Make 2D Vector"

    def init(self, context):
        self.add_in("NodeSocketFloat", "x", 1, False)
        self.add_in("NodeSocketFloat", "y", 1, False)
        self.add_out(EGS_Vector2D.bl_idname, "result") # bind: result -> on_result

    def on_result(self):
        x = self.get_input_value("x")
        y = self.get_input_value("y")
        return [x, y]
    

class PNY_Make3D(EG_PureNode):
    """Event Make 3D Vector Node"""
    
    bl_idname = "egn_python_make_3d"
    bl_label = "Make 3D Vector"

    def init(self, context):
        self.add_in("NodeSocketFloat", "x", 1, False)
        self.add_in("NodeSocketFloat", "y", 1, False)
        self.add_in("NodeSocketFloat", "z", 1, False)
        self.add_out("NodeSocketVector", "result") # bind: result -> on_result

    def on_result(self):
        x = self.get_input_value("x")
        y = self.get_input_value("y")
        z = self.get_input_value("z")
        return [x, y, z]
    

class PNY_Make4D(EG_PureNode):
    """Event Make 4D Vector Node"""
    
    bl_idname = "egn_python_make_4d"
    bl_label = "Make 4D Vector"

    def init(self, context):
        self.add_in("NodeSocketFloat", "x", 1, False)
        self.add_in("NodeSocketFloat", "y", 1, False)
        self.add_in("NodeSocketFloat", "z", 1, False)
        self.add_in("NodeSocketFloat", "w", 1, False)
        self.add_out(EGS_Vector4D.bl_idname, "result") # bind: result -> on_result

    def on_result(self):
        x = self.get_input_value("x")
        y = self.get_input_value("y")
        z = self.get_input_value("z")
        w = self.get_input_value("w")
        return [x, y, z, w]


classes = [
    EGN_LiteralInteger,
    EGN_LiteralFloat,
    EGN_LiteralString,
    EGN_LiteralBoolean,
    EGN_LiteralColor,
    PNY_Make2D,
    PNY_Make3D,
    PNY_Make4D,
    PNY_Break2D,
    PNY_Break3D,
    PNY_Break4D
]