import uuid
import bpy
from bpy.props import ( BoolProperty, FloatProperty, EnumProperty, StringProperty, IntProperty, PointerProperty, CollectionProperty, FloatVectorProperty )

from ...base.node import EG_PureNode
from ...base.library import create_enum
from ...socket.primitive import EGS_Value


class EGN_CompareOperator(EG_PureNode):
    """Event Compare Operator Node"""
    
    bl_idname = "EGN_CompareOperator"
    bl_label = "Compare Operator"

    operator: EnumProperty(
        name="Operator",
        items=create_enum(["<", ">", "<=", ">=", "==", "!="]),
        default="<"
    ) # type: ignore

    def draw_buttons(self, context, layout):
        layout.prop(self, "operator")

    def init(self, context):
        self.add_in(EGS_Value.bl_idname, "a")
        self.add_in(EGS_Value.bl_idname, "b")
        self.add_out("NodeSocketBool", "result") # bind: result -> on_result

    def on_result(self):
        selected_operator = self.operator
        value_a = self.get_input_value("a")
        value_b = self.get_input_value("b")

        if selected_operator == "<":
            return value_a < value_b

        if selected_operator == ">":
            return value_a > value_b
        
        if selected_operator == "<=":
            return value_a <= value_b
        
        if selected_operator == ">=":
            return value_a >= value_b
        
        if selected_operator == "==":
            return value_a == value_b
        
        if selected_operator == "!=":
            return value_a != value_b

        return False


class EGN_LogicalAndOperator(EG_PureNode):
    """Logical And Operator Node"""
    
    bl_idname = "EGN_LogicalAndOperator"
    bl_label = "And"

    def init(self, context):
        self.add_in("NodeSocketBool", "a")
        self.add_in("NodeSocketBool", "b")
        self.add_out("NodeSocketBool", "result") # bind: result -> on_result

    def on_result(self):
        value_a = self.get_input_value("a")
        value_b = self.get_input_value("b")

        return value_a and value_b


class EGN_LogicalOrOperator(EG_PureNode):
    """Logical Or Operator Node"""
    
    bl_idname = "EGN_LogicalOrOperator"
    bl_label = "Or"

    def init(self, context):
        self.add_in("NodeSocketBool", "a")
        self.add_in("NodeSocketBool", "b")
        self.add_out("NodeSocketBool", "result") # bind: result -> on_result

    def on_result(self):
        value_a = self.get_input_value("a")
        value_b = self.get_input_value("b")

        return value_a or value_b


class EGN_LogicalNotOperator(EG_PureNode):
    """Logical Not Operator Node"""
    
    bl_idname = "EGN_LogicalNotOperator"
    bl_label = "Not"

    def init(self, context):
        self.add_in("NodeSocketBool", "a")
        self.add_out("NodeSocketBool", "result") # bind: result -> on_result

    def on_result(self):
        value_a = self.get_input_value("a")
        return not value_a


class EGN_IdentityOperator(EG_PureNode):
    """Identity Operator Node"""
    
    bl_idname = "EGN_IdentityOperator"
    bl_label = "Identity Comparison"

    operator: EnumProperty(
        name="Operator",
        items=create_enum(["is", "is not"]),
        default="is"
    ) # type: ignore

    def init(self, context):
        self.add_in(EGS_Value.bl_idname, "a")
        self.add_in(EGS_Value.bl_idname, "b")
        self.add_out("NodeSocketBool", "result") # bind: result -> on_result

    def draw_buttons(self, context, layout):
        layout.prop(self, "operator")

    def on_result(self):
        value_a = self.get_input_value("a")
        value_b = self.get_input_value("b")

        if self.operator == "is":
            return value_a is value_b

        if self.operator == "is not":
            return value_a is not value_b

        return False


class EGN_MembershipOperator(EG_PureNode):
    """Membership Operator Node"""
    
    bl_idname = "EGN_MembershipOperator"
    bl_label = "Membership Check"

    operator: EnumProperty(
        name="Operator",
        items=create_enum(["in", "not in"]),
        default="in"
    ) # type: ignore

    def init(self, context):
        self.add_in(EGS_Value.bl_idname, "a")
        self.add_in(EGS_Value.bl_idname, "b")
        self.add_out("NodeSocketBool", "result") # bind: result -> on_result

    def draw_buttons(self, context, layout):
        layout.prop(self, "operator")

    def on_result(self):
        value_a = self.get_input_value("a")
        value_b = self.get_input_value("b")

        if self.operator == "in":
            return value_a in value_b

        if self.operator == "not in":
            return value_a not in value_b

        return False


class EGN_IsNone(EG_PureNode):
    """Check if value is None"""
    
    bl_idname = "EGN_IsNone"
    bl_label = "Is None"

    def init(self, context):
        self.add_in(EGS_Value.bl_idname, "a")
        self.add_out("NodeSocketBool", "result") # bind: result -> on_result

    def on_result(self):
        in_a = self.get_input_value("a")
        return in_a is None


classes = [
    EGN_CompareOperator,
    EGN_LogicalAndOperator,
    EGN_LogicalOrOperator,
    EGN_LogicalNotOperator,
    EGN_IdentityOperator,
    EGN_MembershipOperator,
    EGN_IsNone
]