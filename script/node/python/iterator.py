import uuid
import bpy
from bpy.props import ( BoolProperty, FloatProperty, EnumProperty, StringProperty, IntProperty, PointerProperty, CollectionProperty, FloatVectorProperty )

from ...base.node import EG_Node
from ...base.library import add_linked_value, get_linked_value, remove_linked_value

from ...socket.user import EGS_Object
from ...socket.primitive import EGS_Value
from ...socket.derived import EGS_Array


class EGN_ForLoop(EG_Node):
    """Event For Loop Node"""
    
    bl_idname = "EGN_ForLoop"
    bl_label = "For Loop"
    bl_icon = "UV_VERTEXSEL"

    start: IntProperty(name="Start", default=0, min=0) # type: ignore
    end: IntProperty(name="End", default=10, min=0) # type: ignore

    def init(self, context):
        super().init(context)
        self.add_exec_in("exec")
        self.add_exec_out("loop")
        self.add_out("NodeSocketInt", "index") # bind: index -> on_index
        self.add_exec_out("completed")

    def on_index(self):
        return get_linked_value(self, "index")

    def execute(self):

        for i in range(self.start, self.end):
            add_linked_value(self, "index", i)
            self.execute_next("loop")

        remove_linked_value(self, "index")
        self.execute_next("completed")

    def draw_buttons(self, context, layout):
        super().draw_buttons(context, layout)
        layout.prop(self, "start")
        layout.prop(self, "end")

    def free(self):
        remove_linked_value(self, "index")


class EGN_ForEach(EG_Node):
    """For Each Node to iterate over a list"""
    
    bl_idname = "EGN_ForEach"
    bl_label = "For Each"
    bl_icon = "UV_VERTEXSEL"

    def init(self, context):
        super().init(context)
        self.add_exec_in("exec")
        self.add_in(EGS_Array.bl_idname, "list")
        self.add_exec_out("loop")
        self.add_out(EGS_Value.bl_idname, "item") # bind: item -> on_item
        self.add_exec_out("completed")

        self.inputs["list"].default_value = []

    def on_item(self):
        return get_linked_value(self, "item")

    def execute(self):

        items = self.get_input_value("list")

        for item in items:
            add_linked_value(self, "item", item)
            self.execute_next("loop")

        remove_linked_value(self, "item")

        self.execute_next("completed")
    
    def free(self):
        remove_linked_value(self, "item")


classes = [
    EGN_ForLoop,
    EGN_ForEach
]