import bpy
from bpy.props import ( BoolProperty, FloatProperty, EnumProperty, StringProperty, IntProperty, PointerProperty, CollectionProperty, FloatVectorProperty )

from ....base.node import EG_Node, EG_PureNode
from ....base.library import add_linked_cache, remove_linked_cache, get_linked_cache

from ....socket.derived import EGS_Array
from ....socket.primitive import EGS_Value


class EGN_RenameObject(EG_Node):
    """Rename an object"""
    
    bl_idname = "egn.object.rename"
    bl_label = "Rename Object"
    bl_icon = "OBJECT_ORIGIN"

    def init(self, context):
        self.add_exec_in("exec")
        self.add_in("NodeSocketString", "object Id", 1, False)
        self.add_in("NodeSocketString", "name", 1, False)
        self.add_exec_out("exec")
        self.add_out("NodeSocketBool", "changed") # bind: changed -> on_changed

    def on_changed(self):
        return get_linked_cache(self, "changed")

    def execute(self):
        in_objectId = self.get_input_value("object Id")
        in_name = self.get_input_value("name")
        out_changed = False

        object_data = bpy.data.objects.get(in_objectId)

        if object_data:
            object_data.name = in_name
            object_data.type = ""
            out_changed = True

        add_linked_cache(self, "changed", out_changed)
        self.execute_next("exec")

    def free(self):
        remove_linked_cache(self, "changed")


class EGN_RenameData(EG_Node):
    """Rename object's data"""
    
    bl_idname = "egn.object.rename_data"
    bl_label = "Rename Data"
    bl_icon = "RNA"

    def init(self, context):
        self.add_exec_in("exec")
        self.add_in("NodeSocketString", "object Id", 1, False)
        self.add_in("NodeSocketString", "name", 1, False)
        self.add_exec_out("exec")
        self.add_out("NodeSocketBool", "changed") # bind: changed -> on_changed

    def on_changed(self):
        return get_linked_cache(self, "changed")

    def execute(self):
        in_objectId = self.get_input_value("object Id")
        in_name = self.get_input_value("name")
        out_changed = False

        object_data = bpy.data.objects.get(in_objectId)

        if object_data:
            object_data.data.name = in_name
            out_changed = True
        else:
            print("Object data not found")

        add_linked_cache(self, "changed", out_changed)
        self.execute_next("exec")

    def free(self):
        remove_linked_cache(self, "changed")


class EGN_DeleteObject(EG_Node):
    """Delete an object"""
    
    bl_idname = "egn.object.delete"
    bl_label = "Delete Object"
    bl_icon = "OBJECT_ORIGIN"

    def init(self, context):
        self.add_exec_in("exec")
        self.add_in("NodeSocketString", "object Id")
        self.add_exec_out("exec")
        self.add_out("NodeSocketBool", "success") # bind: success -> on_success

    def on_success(self):
        return get_linked_cache(self, "success")

    def execute(self):
        in_objectId = self.get_input_value("object Id")
        out_success = False

        object_data = bpy.data.objects.get(in_objectId)

        if object_data:
            bpy.data.objects.remove(object_data, do_unlink=True)
            bpy.ops.ed.undo_push()

            out_success = True

        add_linked_cache(self, "success", out_success)

        self.execute_next("exec")

    def free(self):
        remove_linked_cache(self, "success")


class EGN_DuplicateObject(EG_Node):
    """Duplicate an object"""
    
    bl_idname = "egn.object.duplicate"
    bl_label = "Duplicate Object"
    bl_icon = "OBJECT_ORIGIN"

    def init(self, context):
        self.add_exec_in("exec")
        self.add_in("NodeSocketString", "object Id")
        self.add_exec_out("exec")
        self.add_out("NodeSocketString", "object Id") # bind: object Id -> on_object_Id
        self.add_out("NodeSocketBool", "success") # bind: success -> on_success

    def on_object_Id(self):
        return get_linked_cache(self, "object Id")

    def on_success(self):
        return get_linked_cache(self, "success")

    def execute(self):
        in_objectId = self.get_input_value("object Id")
        out_objectId = None
        out_success = False

        object_data = bpy.data.objects.get(in_objectId)

        if object_data:
            new_object = object_data.copy()
            new_object.data = object_data.data.copy()

            bpy.context.collection.objects.link(new_object)
            bpy.ops.ed.undo_push()

            out_objectId = new_object.name
            out_success = True

        add_linked_cache(self, "object Id", out_objectId)
        add_linked_cache(self, "success", out_success)

        self.execute_next("exec")

    def free(self):
        remove_linked_cache(self, "object Id")
        remove_linked_cache(self, "success")


classes = [
    EGN_RenameObject,
    EGN_RenameData,
    EGN_DeleteObject,
    EGN_DuplicateObject
]