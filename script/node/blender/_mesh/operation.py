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

    def init(self, context):
        self.add_exec_in("exec")
        self.add_in(EGS_Array.bl_idname, "object Ids", limit=100)
        self.add_exec_out("exec")
        self.add_out("NodeSocketString", "data Id") # bind: dataId -> on_data_Id
        self.add_out("NodeSocketString", "object Id") # bind: objectId -> on_object_Id

    def on_data_Id(self):
        return get_linked_cache(self, "data Id")
    
    def on_object_Id(self):
        return get_linked_cache(self, "object Id")

    def execute(self):
        in_objectIds = self.get_input_values("object Ids")

        if not in_objectIds:
            # print("Object Ids is empty")
            self.execute_next("exec")
            return

        bpy.ops.object.mode_set(mode="OBJECT")
        bpy.ops.object.select_all(action="DESELECT")

        selected_objects = []
        for objectId in in_objectIds:
            obj = bpy.data.objects.get(objectId)
            if obj and obj.type == "MESH":
                obj.select_set(True)
                selected_objects.append(obj)

        if len(selected_objects) < 2:
            # print("Not enough objects selected")
            self.execute_next("exec")
            return

        first_object = selected_objects[0]
        bpy.context.view_layer.objects.active = first_object

        bpy.ops.object.join()
        bpy.context.view_layer.update()

        add_linked_cache(self, "data Id", first_object.data.name)
        add_linked_cache(self, "object Id", first_object.name)

        # print("Meshes joined")
        self.execute_next("exec")

    def free(self):
        remove_linked_cache(self, "data Id")
        remove_linked_cache(self, "object Id")



classes = [
    EGN_JoinMeshes,
]