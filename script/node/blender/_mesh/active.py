import bpy
from bpy.props import ( BoolProperty, FloatProperty, EnumProperty, StringProperty, IntProperty, PointerProperty, CollectionProperty, FloatVectorProperty )

from ....base.node import EG_Node, EG_PureNode
from ....base.library import create_enum, add_linked_cache, remove_linked_cache, get_linked_cache

from ....socket.derived import EGS_Array
from ....socket.primitive import EGS_Value


class EGN_MeshSelectAll(EG_Node):
    """Select all action for mesh in edit mode"""
    
    bl_idname = "egn_mesh_select_all"
    bl_label = "Mesh Select All"
    bl_icon = "MESH_DATA"

    prop_action: EnumProperty(
        name="Action",
        items=[
            ("SELECT", "Select", ""),
            ("DESELECT", "Deselect", ""),
            ("INVERT", "Invert", ""),
            ("TOGGLE", "Toggle", ""),
        ],
        default="SELECT"
    ) # type: ignore

    def init(self, context):
        self.add_exec_in("exec")
        self.add_exec_out("success")
        self.add_exec_out("failed")

    def draw_buttons(self, context, layout):
        layout.prop(self, "prop_action")

    def execute(self):
        if bpy.context.object.mode == "EDIT":
            bpy.ops.mesh.select_all(action=self.prop_action)
            self.execute_next("success")

        else:
            self.execute_next("failed")


classes = [
    EGN_MeshSelectAll
]