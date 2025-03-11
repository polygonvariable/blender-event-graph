import uuid
import bpy
from bpy.props import ( BoolProperty, FloatProperty, EnumProperty, StringProperty, IntProperty, PointerProperty, CollectionProperty, FloatVectorProperty )

from ...base.node import EG_Node
from ...base.library import create_enum

from ...socket.user import EGS_Object
from ...socket.primitive import EGS_Value

from ...operator.exec_main import EGOP_ExecuteMain



    
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
    EGN_CallGraph,
]