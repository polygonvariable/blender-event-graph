import bpy
from bpy.props import ( BoolProperty, FloatProperty, EnumProperty, StringProperty, IntProperty, PointerProperty, CollectionProperty )

from ..base.node import EG_Node
from ..base.library import create_enum
from ..operator.exec_main import EGOP_ExecuteMain


class EGN_Definition(EG_Node):
    """Event Definition Node"""
    
    bl_idname = "EGN_Definition"
    bl_label = "Definition"

    def init(self, context):
        self.add_exec_out("exec")

    def draw_buttons(self, context, layout):
        layout.operator(EGOP_ExecuteMain.bl_idname, text="Execute")

    def execute(self):
        self.execute_next("exec")


class EGN_Print(EG_Node):
    """Event Print Node"""
    
    bl_idname = "EGN_Print"
    bl_label = "Print"

    def init(self, context):
        self.add_exec_in("exec")
        self.add_in("EGS_Value", "value")
        self.add_exec_out("exec")

    def execute(self):
        print(self.get_input_value("value"))
        self.execute_next("exec")

class PNY_ToFloat(EG_Node):
    """Event To Float Node"""
    
    bl_idname = "PNY_ToFloat"
    bl_label = "To Float"

    def init(self, context):
        self.add_in("EGS_Value", "value")
        self.add_out("NodeSocketFloat", "result")

    def on_result(self):
        return float(self.get_input_value("value"))

class PNY_ToInt(EG_Node):
    """Event To Int Node"""
    
    bl_idname = "PNY_ToInt"
    bl_label = "To Int"

    def init(self, context):
        self.add_in("EGS_Value", "value")
        self.add_out("NodeSocketInt", "result")

    def on_result(self):
        return int(self.get_input_value("value"))

class PNY_ToString(EG_Node):
    """Event To String Node"""
    
    bl_idname = "PNY_ToString"
    bl_label = "To String"

    def init(self, context):
        self.add_in("EGS_Value", "value")
        self.add_out("NodeSocketString", "result")

    def on_result(self):
        return str(self.get_input_value("value"))
    

class EGN_Math(EG_Node):
    """Event Math Node"""
    
    bl_idname = "EGN_Math"
    bl_label = "Math"

    node_is_pure = True

    operator: EnumProperty(
        name="Operator",
        items=create_enum(["+", "-", "*", "/"]),
        default="+"
    ) # type: ignore

    def draw_buttons(self, context, layout):
        layout.prop(self, "operator")

    def init(self, context):
        self.add_in("NodeSocketFloat", "A")
        self.add_in("NodeSocketFloat", "B")
        self.add_out("NodeSocketFloat", "result") # result is linked to on_result

    def on_result(self):
        selected_operator = self.operator

        if selected_operator == "+":
            return self.get_input_value("A") + self.get_input_value("B")
        if selected_operator == "-":
            return self.get_input_value("A") - self.get_input_value("B")
        if selected_operator == "*":
            return self.get_input_value("A") * self.get_input_value("B")
        if selected_operator == "/":
            return self.get_input_value("A") / self.get_input_value("B")

        return 0


class EGN_IfElse(EG_Node):
    """Event If Else Node"""
    
    bl_idname = "EGN_IfElse"
    bl_label = "If Else"

    def init(self, context):
        self.add_exec_in("exec")
        self.add_in("NodeSocketBool", "condition")
        self.add_exec_out("true")
        self.add_exec_out("false")

    def execute(self):
        if self.get_input_value("condition"):
            self.execute_next("true")
        else:
            self.execute_next("false")


class EGN_ForLoop(EG_Node):
    """Event For Loop Node"""
    
    bl_idname = "EGN_ForLoop"
    bl_label = "For Loop"

    start: IntProperty(name="Start", default=0, min=0) # type: ignore
    end: IntProperty(name="End", default=10, min=0) # type: ignore

    def init(self, context):
        self.add_exec_in("exec")
        self.add_exec_out("loop")
        self.add_out("NodeSocketInt", "index")
        self.add_exec_out("completed")

    def on_index(self):
        return get_variable_for_node(self, "index")

    def execute(self):

        for i in range(self.start, self.end):
            add_variable_for_node(self, "index", i)
            self.execute_next("loop")

        remove_variable_for_node(self, "index")
        self.execute_next("completed")

    def draw_buttons(self, context, layout):
        layout.prop(self, "start")
        layout.prop(self, "end")


class EGN_CompareOperator(EG_Node):
    """Event Compare Operator Node"""
    
    bl_idname = "EGN_CompareOperator"
    bl_label = "Compare Operator"

    node_is_pure = True

    operator: EnumProperty(
        name="Operator",
        items=create_enum(["<", ">", "<=", ">=", "==", "!="]),
        default="<"
    ) # type: ignore

    def draw_buttons(self, context, layout):
        layout.prop(self, "operator")

    def init(self, context):
        self.add_in("EGS_Value", "A")
        self.add_in("EGS_Value", "B")
        self.add_out("NodeSocketBool", "result")

    def on_result(self):
        selected_operator = self.operator

        if selected_operator == "<":
            return self.get_input_value("A") < self.get_input_value("B")
        if selected_operator == ">":
            return self.get_input_value("A") > self.get_input_value("B")
        if selected_operator == "<=":
            return self.get_input_value("A") <= self.get_input_value("B")
        if selected_operator == ">=":
            return self.get_input_value("A") >= self.get_input_value("B")
        if selected_operator == "==":
            return self.get_input_value("A") == self.get_input_value("B")
        if selected_operator == "!=":
            return self.get_input_value("A") != self.get_input_value("B")

        return False


variable_dict = {}

def add_variable(name, value):
    variable_dict[name] = value

def get_variable(name):
    return variable_dict.get(name, None)

def remove_variable(name):
    if name in variable_dict:
        del variable_dict[name]

def add_variable_for_node(node, name, value):
    add_variable(f"{node.node_uuid}_{name}", value)

def get_variable_for_node(node, name):
    return get_variable(f"{node.node_uuid}_{name}")

def remove_variable_for_node(node, name):
    remove_variable(f"{node.node_uuid}_{name}")

class EGN_SetVariable(EG_Node):
    """Event Set Variable Node"""
    
    bl_idname = "EGN_SetVariable"
    bl_label = "Set Variable"

    name: StringProperty(name="Name") # type: ignore
    value = None

    def draw_buttons(self, context, layout):
        layout.prop(self, "name")

    def init(self, context):
        self.add_exec_in("exec")
        self.add_in("EGS_Value", "value")
        self.add_exec_out("exec")

    def execute(self):
        add_variable(self.name, self.get_input_value("value"))
        self.execute_next("exec")

class EGN_GetVariable(EG_Node):
    """Event Get Variable Node"""
    
    bl_idname = "EGN_GetVariable"
    bl_label = "Get Variable"

    node_is_pure = True

    name: StringProperty(name="Name") # type: ignore

    def draw_buttons(self, context, layout):
        layout.prop(self, "name")

    def init(self, context):
        self.add_out("EGS_Value", "value")

    def on_value(self):
        return get_variable(self.name)
    
class EGN_Array(EG_Node):
    """Event Array Node"""
    
    bl_idname = "EGN_Array"
    bl_label = "Make Array"

    node_is_pure = True

    def init(self, context):
        self.add_in("EGS_Value", "item")
        self.add_out("EGS_Array", "array")

    def on_array(self):
        return self.get_input_values("item")


class EGN_OperatorAdd(EG_Node):
    """Event Operator Add Node"""
    
    bl_idname = "EGN_OperatorAdd"
    bl_label = "Add"

    node_is_pure = True

    def init(self, context):
        self.add_in("EGS_Value", "A")
        self.add_in("EGS_Value", "B")
        self.add_out("EGS_Value", "result")

    def on_result(self):
        return self.get_input_value("A") + self.get_input_value("B")
    
class EGN_ArrayAppend(EG_Node):
    """Event Array Append Node"""
    
    bl_idname = "EGN_ArrayAppend"
    bl_label = "Array Append"

    node_is_pure = True
    
    def init(self, context):
        self.add_in("EGS_Array", "array")
        self.add_in("EGS_Value", "item")
        self.add_out("EGS_Array", "array")

    def on_array(self):
        return self.get_input_value("array") + self.get_input_values("item")
    
class EGN_ArrayPop(EG_Node):
    """Event Array Pop Node"""
    
    bl_idname = "EGN_ArrayPop"
    bl_label = "Array Pop"

    node_is_pure = True
    
    def init(self, context):
        self.add_in("EGS_Array", "array")
        self.add_out("EGS_Array", "array")

    def on_array(self):
        arr = self.get_input_value("array")
        arr.pop()
        return arr

classes = [
    EGN_Definition,
    EGN_Print,
    EGN_Math,
    EGN_CompareOperator,
    EGN_SetVariable,
    EGN_GetVariable,
    PNY_ToInt,
    PNY_ToString,
    PNY_ToFloat,
    EGN_IfElse,
    EGN_ForLoop,
    EGN_Array,
    EGN_ArrayAppend,
    EGN_ArrayPop,
    EGN_OperatorAdd
]