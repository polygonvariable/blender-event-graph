import uuid
import bpy
from bpy.props import ( BoolProperty, FloatProperty, EnumProperty, StringProperty, IntProperty, PointerProperty, CollectionProperty, FloatVectorProperty )

from ...base.node import EG_Node
from ...base.library import create_enum, add_variable, get_variable

from ...socket.user import EGS_Object
from ...socket.primitive import EGS_Value

from ...operator.exec_main import EGOP_ExecuteMain


class EGN_Definition(EG_Node):
    """Event Definition Node"""
    
    bl_idname = "EGN_Definition"
    bl_label = "Definition"

    def init(self, context):
        super().init(context)
        self.add_exec_out("exec")
        self.add_out(EGS_Object.bl_idname, "args")

    def draw_buttons(self, context, layout):
        layout.operator(EGOP_ExecuteMain.bl_idname, text="Execute")

    def execute(self):
        self.execute_next("exec")


class EGN_Print(EG_Node):
    """Event Print Node"""
    
    bl_idname = "EGN_Print"
    bl_label = "Print"

    def init(self, context):
        super().init(context)
        self.add_exec_in("exec")
        self.add_in(EGS_Value.bl_idname, "value")
        self.add_exec_out("exec")

    def execute(self):
        print(self.get_input_value("value"))
        self.execute_next("exec")


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

class EGN_SetVariable(EG_Node):
    """Event Set Variable Node"""
    
    bl_idname = "EGN_SetVariable"
    bl_label = "Set Variable"

    name: StringProperty(name="Name") # type: ignore
    value = None

    def draw_buttons(self, context, layout):
        layout.prop(self, "name")

    def init(self, context):
        super().init(context)
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
    
def get_graphs(self, context):
    """Dynamically fetch all graphs of type EG_NodeTree."""
    graphs = [(tree.name, tree.name, "") for tree in bpy.data.node_groups if tree.bl_idname == "EG_NodeTree"]
    return graphs if graphs else [("None", "None", "No graphs available")]



class EGN_CallGraph(EG_Node):

    """Node to list available EG_NodeTree graphs."""
    
    bl_idname = "EGN_CallGraph"
    bl_label = "Call Graph"

    selected_graph: EnumProperty(
        name="Graph",
        description="Select an Event Graph",
        items=get_graphs
    ) # type: ignore

    def draw_buttons(self, context, layout):
        layout.prop(self, "selected_graph", text="Graph")

    def init(self, context):
        self.add_exec_in("exec")
        self.add_in("NodeSocketString", "args")
        self.add_exec_out("exec")
        self.add_out("NodeSocketString", "args")

    def execute(self):
        graph = bpy.data.node_groups.get(self.selected_graph)
        if graph:
            for node in graph.nodes:
                if node.bl_idname == "EGN_Definition" and hasattr(node, "execute"):
                    node.execute()

        self.execute_next("exec")


classes = [
    EGN_Definition,
    EGN_Print,
    EGN_Math,
    EGN_SetVariable,
    EGN_GetVariable,
    EGN_IfElse,
    EGN_OperatorAdd,
    EGN_CallGraph,
]