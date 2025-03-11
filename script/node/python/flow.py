import math
import bpy
from bpy.props import ( BoolProperty, FloatProperty, EnumProperty, StringProperty, IntProperty, PointerProperty, CollectionProperty, FloatVectorProperty )

from ...base.node import EG_Node
from ...base.library import add_linked_cache, get_linked_cache, remove_linked_cache

from ...socket.user import EGS_Object
from ...socket.primitive import EGS_Value
from ...socket.derived import EGS_Array
from ...operator.exec_main import EGOP_ExecuteMain


class EGN_Function(EG_Node):
    """Node to initialize a execution flow"""
    
    bl_idname = "egn_python_function"
    bl_label = "Function"
    bl_icon = "FF"

    def init(self, context):
        self.add_exec_out("exec")
        self.add_out(EGS_Object.bl_idname, "args")

    def draw_buttons(self, context, layout):
        layout.operator(EGOP_ExecuteMain.bl_idname, text="Execute")

    def execute(self):
        self.execute_next("exec")


class EGN_Callback(EG_Node):
    """A Callback Node"""
    
    bl_idname = "egn_python_callback"
    bl_label = "Callback"
    bl_icon = "FF"

    def init(self, context):
        self.add_exec_out("callback", is_callback=True)
        self.add_exec_out("exec")

    def execute(self):
        self.execute_next("exec")


class EGN_Branch(EG_Node):
    """Node to switch between execution flow based on boolean condition"""
    
    bl_idname = "egn_python_branch"
    bl_label = "Branch"

    def init(self, context):
        self.add_exec_in("exec")
        self.add_in("NodeSocketBool", "condition", 1, False)
        self.add_exec_out("true")
        self.add_exec_out("false")

    def execute(self):
        if self.get_input_value("condition"):
            self.execute_next("true")
        else:
            self.execute_next("false")


class EGN_Sequence(EG_Node):
    """A node that executes a sequence of nodes"""
    
    bl_idname = "egn_python_sequence"
    bl_label = "Sequence"

    def update_sockets(self, context):
        for socket in self.outputs:
            self.outputs.remove(socket)

        in_count = int(self.socket_limit + 1)
        for index in range(1, in_count):
            self.add_exec_out("exec " + str(index))

    socket_limit: IntProperty(name="Limit", default=1, update=update_sockets, min=1, max=10) # type: ignore

    def init(self, context):
        self.add_exec_in("exec")
        self.add_exec_out("exec 1")

    def draw_buttons(self, context, layout):
        layout.prop(self, "socket_limit")

    def execute(self):
        for socket in self.outputs:
            self.execute_next(socket.name)


class EGN_FlipFlop(EG_Node):
    """A node that switches between two execution flows"""
    
    bl_idname = "egn_python_flipflop"
    bl_label = "Flip Flop"

    active_state: BoolProperty(name="State", default=True) # type: ignore
    
    def init(self, context):
        self.add_exec_in("exec")
        self.add_exec_out("a")
        self.add_exec_out("b")

    def execute(self):
        if self.active_state:
            self.active_state = False
            self.execute_next("a")
        else:
            self.active_state = True
            self.execute_next("b")


class EGN_ForLoop(EG_Node):
    """Node to iterate over a range of values"""
    
    bl_idname = "egn_python_for_loop"
    bl_label = "For Loop"
    bl_icon = "UV_VERTEXSEL"

    prop_index: IntProperty(name="Index", default=0) # type: ignore

    def init(self, context):
        self.add_exec_in("exec")
        self.add_in(socket="NodeSocketInt", name="start", hide_value=False, default=0)
        self.add_in(socket="NodeSocketInt", name="end", hide_value=False, default=10)

        self.add_exec_out("loop")
        self.add_out("NodeSocketInt", "index") # bind: index -> on_index
        self.add_exec_out("completed")

    def on_index(self):
        return self.prop_index

    def execute(self):
        in_start = self.get_input_value("start")
        in_end = self.get_input_value("end")
        self.prop_index = in_start

        for index in range(in_start, in_end):
            self.prop_index = index
            self.execute_next("loop")

        self.execute_next("completed")


class EGN_ForEach(EG_Node):
    """Node to iterate over a list of values"""
    
    bl_idname = "egn_python_for_each"
    bl_label = "For Each"
    bl_icon = "UV_VERTEXSEL"

    def init(self, context):
        self.add_exec_in("exec")
        self.add_in(EGS_Array.bl_idname, "list")
        
        self.add_exec_out("loop")
        self.add_out(EGS_Value.bl_idname, "item") # bind: item -> on_item
        self.add_exec_out("completed")

        self.inputs["list"].default_value = []

    def on_item(self):
        return get_linked_cache(self, "item")

    def execute(self):

        in_list = self.get_input_value("list")

        for item in in_list:
            add_linked_cache(self, "item", item)
            self.execute_next("loop")

        remove_linked_cache(self, "item")
        self.execute_next("completed")
    
    def free(self):
        remove_linked_cache(self, "item")


classes = [
    EGN_Function,
    EGN_Callback,
    EGN_Branch,
    EGN_Sequence,
    EGN_FlipFlop,
    EGN_ForLoop,
    EGN_ForEach
]