import bpy
from bpy.props import ( BoolProperty, FloatProperty, EnumProperty, StringProperty, IntProperty, PointerProperty, CollectionProperty, FloatVectorProperty )

from ....base.node import EG_Node, EG_PureNode
from ....base.library import add_linked_cache, remove_linked_cache, get_linked_cache

from ....socket.derived import EGS_Array
from ....socket.primitive import EGS_Value


class EGN_RenameObject(EG_Node):
    """Rename an object"""
    
    bl_idname = "egn_object_rename"
    bl_label = "Rename Object"
    bl_icon = "OBJECT_ORIGIN"

    def init(self, context):
        self.add_exec_in("exec")
        self.add_in(socket="NodeSocketString", name="object Id", hide_value=False)
        self.add_in(socket="NodeSocketString", name="name", hide_value=False)
        self.add_exec_out("success")
        self.add_exec_out("failed")

    def execute(self):
        in_objectId = self.get_input_value("object Id")
        in_name = self.get_input_value("name")

        object_data = bpy.data.objects.get(in_objectId)

        if object_data:
            object_data.name = in_name
            self.execute_next("success")

        else:
            self.execute_next("failed")


class EGN_RenameData(EG_Node):
    """Rename object's data"""
    
    bl_idname = "egn_object_rename_data"
    bl_label = "Rename Data"
    bl_icon = "RNA"

    def init(self, context):
        self.add_exec_in("exec")
        self.add_in(socket="NodeSocketString", name="object Id", hide_value=False)
        self.add_in(socket="NodeSocketString", name="name", hide_value=False)
        self.add_exec_out("success")
        self.add_exec_out("failed")

    def execute(self):
        in_objectId = self.get_input_value("object Id")
        in_name = self.get_input_value("name")

        object_data = bpy.data.objects.get(in_objectId)

        if object_data and object_data.data:
            object_data.data.name = in_name
            self.execute_next("success")

        else:
            self.execute_next("failed")


class EGN_DeleteObject(EG_Node):
    """Delete an object"""
    
    bl_idname = "egn_object_delete"
    bl_label = "Delete Object"
    bl_icon = "OBJECT_ORIGIN"

    def init(self, context):
        self.add_exec_in("exec")
        self.add_in("NodeSocketString", "object Id")
        self.add_exec_out("success")
        self.add_exec_out("failed")

    def execute(self):
        in_objectId = self.get_input_value("object Id")
        object_data = bpy.data.objects.get(in_objectId)

        if object_data:
            bpy.data.objects.remove(object_data, do_unlink=True)
            bpy.ops.ed.undo_push()
            self.execute_next("success")
            
        else:
            self.execute_next("failed")


class EGN_DuplicateObject(EG_Node):
    """Duplicate an object"""
    
    bl_idname = "egn_object_duplicate"
    bl_label = "Duplicate Object"
    bl_icon = "OBJECT_ORIGIN"

    prop_objectId: StringProperty(name="object Id") # type: ignore

    def init(self, context):
        self.add_exec_in("exec")
        self.add_in("NodeSocketString", "object Id")
        self.add_exec_out("success")
        self.add_exec_out("failed")
        self.add_out("NodeSocketString", "object Id") # bind: object Id -> on_object_Id

    def on_object_Id(self):
        return self.prop_objectId

    def execute(self):
        try:
            self.prop_objectId = ""

            in_objectId = self.get_input_value("object Id")
            object_data = bpy.data.objects.get(in_objectId)

            if not object_data:
                raise Exception("Object not found")
            
            new_object = object_data.copy()
            new_object.data = object_data.data.copy()

            bpy.context.collection.objects.link(new_object)
            bpy.ops.ed.undo_push()

            self.prop_objectId = new_object.name
            self.execute_next("success")

        except Exception as e:
            print(e)
            self.execute_next("failed")


class EGN_SetParent(EG_Node):
    """Assign a parent to an object"""
    
    bl_idname = "egn_object_set_parent"
    bl_label = "Set Parent"
    bl_icon = "LINKED"

    def init(self, context):
        self.add_exec_in("exec")
        self.add_in("NodeSocketString", "object Id")
        self.add_in("NodeSocketString", "parent Id")
        self.add_exec_out("success")
        self.add_exec_out("failed")
    
    def execute(self):
        in_objectId = self.get_input_value("object Id")
        in_parentId = self.get_input_value("parent Id")

        object_data = bpy.data.objects.get(in_objectId)
        parent_data = bpy.data.objects.get(in_parentId)

        if object_data and parent_data:
            object_data.parent = parent_data
            self.execute_next("success")
            
        else:
            self.execute_next("failed")


class EGN_ClearParent(EG_Node):
    """Remove a parent from an object"""
    
    bl_idname = "egn_object_clear_parent"
    bl_label = "Clear Parent"
    bl_icon = "UNLINKED"

    def init(self, context):
        self.add_exec_in("exec")
        self.add_in("NodeSocketString", "object Id")
        self.add_exec_out("success")
        self.add_exec_out("failed")
    
    def execute(self):
        in_objectId = self.get_input_value("object Id")
        object_data = bpy.data.objects.get(in_objectId)

        if object_data:
            object_data.parent = None
            self.execute_next("success")
            
        else:
            self.execute_next("failed")


classes = [
    EGN_RenameObject,
    EGN_RenameData,
    EGN_DeleteObject,
    EGN_DuplicateObject,
    EGN_SetParent,
    EGN_ClearParent,
]