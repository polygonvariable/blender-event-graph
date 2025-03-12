import bpy
from bpy.ops import mesh
from bpy.props import ( BoolProperty, FloatProperty, EnumProperty, StringProperty, IntProperty, PointerProperty, CollectionProperty, FloatVectorProperty )
from bpy_extras.io_utils import ImportHelper

from ....base.node import EG_Node
from ....base.library import get_linked_cache, remove_linked_cache, add_linked_cache

from ....socket.derived import EGS_Array
from ....socket.primitive import EGS_Value


class EGN_JoinMeshes(EG_Node):
    """Join multiple meshes and returns its data and object Ids"""
    
    bl_idname = "egn.mesh.join"
    bl_label = "Join Meshes"
    bl_icon = "SELECT_EXTEND"

    prop_dataId: StringProperty(name="data Id") # type: ignore
    prop_objectId: StringProperty(name="object Id") # type: ignore

    def init(self, context):
        self.add_exec_in("exec")
        self.add_in(socket=EGS_Array.bl_idname, name="object Ids", limit=100)
        self.add_exec_out("success")
        self.add_exec_out("failed")
        self.add_out("NodeSocketString", "data Id") # bind: dataId -> on_data_Id
        self.add_out("NodeSocketString", "object Id") # bind: objectId -> on_object_Id

    def on_data_Id(self):
        return self.prop_dataId
    
    def on_object_Id(self):
        return self.prop_objectId

    def execute(self):
        self.prop_dataId = ""
        self.prop_objectId = ""

        in_objectIds = self.get_input_values("object Ids")

        if not isinstance(in_objectIds, list):
            self.execute_next("failed")
            return

        bpy.ops.object.mode_set(mode="OBJECT")
        bpy.ops.object.select_all(action="DESELECT")

        selected_objects = []
        for objectId in in_objectIds:
            current_object = bpy.data.objects.get(objectId)
            
            if current_object and current_object.type == "MESH":
                current_object.select_set(True)
                selected_objects.append(current_object)

        if len(selected_objects) < 2:
            self.execute_next("failed")
            return

        first_object = selected_objects[0]
        bpy.context.view_layer.objects.active = first_object

        self.prop_dataId = first_object.data.name
        self.prop_objectId = first_object.name

        bpy.ops.object.join()
        bpy.context.view_layer.update()

        self.execute_next("success")


classes = [
    EGN_JoinMeshes,
]