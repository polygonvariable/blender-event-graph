import bpy
from bpy.props import ( BoolProperty, FloatProperty, EnumProperty, StringProperty, IntProperty, PointerProperty, CollectionProperty, FloatVectorProperty )

from ...base.node import EG_Node
from ...base.library import create_enum, add_linked_value, remove_linked_value, get_linked_value, variable_map

from ...socket.derived import EGS_Array
from ...socket.primitive import EGS_Value


class EGN_GetObjectId(EG_Node):
    """Get the object id"""
    
    bl_idname = "EGN_GetObjectId"
    bl_label = "Get Object Id"
    bl_icon = "OBJECT_ORIGIN"

    target_object: PointerProperty(name="Object", type=bpy.types.Object) # type: ignore

    def init(self, context):
        self.add_out("NodeSocketString", "object Id") # bind: object Id -> on_object_Id

    def draw_buttons(self, context, layout):
        layout.prop(self, "target_object")

    def on_object_Id(self):
        if not self.target_object:
            return ""
        return str(self.target_object.name)


class EGN_GetDataId(EG_Node):
    """Get the data id by object id"""
    
    bl_idname = "EGN_GetDataId"
    bl_label = "Get Data Id"
    bl_icon = "RNA"

    def init(self, context):
        self.add_in("NodeSocketString", "object Id")
        self.add_out("NodeSocketString", "data Id") # bind: data Id -> on_data_Id

    def on_data_Id(self):
        in_objectId = self.get_input_value("object Id")
        object_data = bpy.data.objects.get(in_objectId)

        if object_data:
            return str(object_data.data.name)
        
        return None


class EGN_GetAllObjects(EG_Node):
    """Gets a list of all objects. This node may be unreliable if objects are modified externally, as the cached list will not reflect those changes."""
    
    bl_idname = "EGN_GetAllObjects"
    bl_label = "Get All Objects"
    bl_icon = "OBJECT_ORIGIN"

    def init(self, context):
        self.add_exec_in("exec")
        self.add_exec_out("exec")
        self.add_out(EGS_Array.bl_idname, "object Ids") # bind: object Ids -> on_object_Id

    def on_object_Ids(self):
        return get_linked_value(self, "object_Ids")

    def execute(self):
        object_ids = [obj.name for obj in bpy.data.objects]
        add_linked_value(self, "object_Ids", object_ids)
        self.execute_next("exec")

    def free(self):
        remove_linked_value(self, "object_Ids")


class EGN_GetLocation(EG_Node):
    """Get the location of an object"""
    
    bl_idname = "EGN_GetLocation"
    bl_label = "Get Location"
    bl_icon = "OBJECT_ORIGIN"

    def init(self, context):
        self.add_in("NodeSocketString", "object Id", 1, False)
        self.add_out("NodeSocketVector", "location") # bind: location -> on_location

    def on_location(self):
        if not self.target_object:
            return (0.0, 0.0, 0.0)
        return self.target_object.location


class EGN_SetLocation(EG_Node):
    """Set the location of an object"""
    
    bl_idname = "EGN_SetLocation"
    bl_label = "Set Location"
    bl_icon = "OBJECT_ORIGIN"

    def init(self, context):
        self.add_exec_in("exec")
        self.add_in("NodeSocketString", "object Id", 1, False)
        self.add_in("NodeSocketVector", "location", 1, False)
        self.add_exec_out("exec")
        self.add_out("NodeSocketBool", "changed") # bind: changed -> on_changed

    def on_changed(self):
        return get_linked_value(self, "changed")

    def execute(self):
        in_objectId = self.get_input_value("object Id")
        in_location = self.get_input_value("location")
        out_changed = False

        object_data = bpy.data.objects.get(in_objectId)

        if object_data:
            object_data.location = in_location
            out_changed = True
        else:
            print("Object data not found")

        add_linked_value(self, "changed", out_changed)
        self.execute_next("exec")

    def free(self):
        remove_linked_value(self, "changed")


class EGN_GetRotation(EG_Node):
    """Get the rotation of an object"""
    
    bl_idname = "EGN_GetRotation"
    bl_label = "Get Rotation"
    bl_icon = "OBJECT_ORIGIN"

    def init(self, context):
        self.add_in("NodeSocketString", "object Id", 1, False)
        self.add_out("NodeSocketVector", "rotation") # bind: rotation -> on_rotation

    def on_rotation(self):
        if not self.target_object:
            return (0.0, 0.0, 0.0)
        return self.target_object.rotation_euler


class EGN_SetRotation(EG_Node):
    """Set the rotation of an object"""
    
    bl_idname = "EGN_SetRotation"
    bl_label = "Set Rotation"
    bl_icon = "OBJECT_ORIGIN"

    def init(self, context):
        self.add_exec_in("exec")
        self.add_in("NodeSocketString", "object Id", 1, False)
        self.add_in("NodeSocketVector", "rotation", 1, False)
        self.add_exec_out("exec")
        self.add_out("NodeSocketBool", "changed") # bind: changed -> on_changed

    def on_changed(self):
        return get_linked_value(self, "changed")

    def execute(self):
        in_objectId = self.get_input_value("object Id")
        in_rotation = self.get_input_value("rotation")
        out_changed = False

        object_data = bpy.data.objects.get(in_objectId)

        if object_data:
            object_data.rotation_euler = in_rotation
            out_changed = True
        else:
            print("Object data not found")

        add_linked_value(self, "changed", out_changed)
        self.execute_next("exec")

    def free(self):
        remove_linked_value(self, "changed")


class EGN_GetScale(EG_Node):
    """Get the scale of an object"""
    
    bl_idname = "EGN_GetScale"
    bl_label = "Get Scale"
    bl_icon = "OBJECT_ORIGIN"

    def init(self, context):
        self.add_in("NodeSocketString", "object Id", 1, False)
        self.add_out("NodeSocketVector", "scale") # bind: scale -> on_scale

    def on_scale(self):
        if not self.target_object:
            return (0.0, 0.0, 0.0)
        return self.target_object.scale


class EGN_SetScale(EG_Node):
    """Set the scale of an object"""
    
    bl_idname = "EGN_SetScale"
    bl_label = "Set Scale"
    bl_icon = "OBJECT_ORIGIN"

    def init(self, context):
        self.add_exec_in("exec")
        self.add_in("NodeSocketString", "object Id", 1, False)
        self.add_in("NodeSocketVector", "scale", 1, False)
        self.add_exec_out("exec")
        self.add_out("NodeSocketBool", "changed") # bind: changed -> on_changed

        self.inputs["scale"].default_value = (1.0, 1.0, 1.0)

    def on_changed(self):
        return get_linked_value(self, "changed")
    
    def execute(self):
        in_objectId = self.get_input_value("object Id")
        in_scale = self.get_input_value("scale")
        out_changed = False

        object_data = bpy.data.objects.get(in_objectId)

        if object_data:
            object_data.scale = in_scale
            out_changed = True
        else:
            print("Object data not found")

        add_linked_value(self, "changed", out_changed)
        self.execute_next("exec")

    def free(self):
        remove_linked_value(self, "changed")


class EGN_RenameObject(EG_Node):
    """Rename an object"""
    
    bl_idname = "EGN_RenameObject"
    bl_label = "Rename Object"
    bl_icon = "OBJECT_ORIGIN"

    def init(self, context):
        self.add_exec_in("exec")
        self.add_in("NodeSocketString", "object Id", 1, False)
        self.add_in("NodeSocketString", "name", 1, False)
        self.add_exec_out("exec")
        self.add_out("NodeSocketBool", "changed") # bind: changed -> on_changed

    def on_changed(self):
        return get_linked_value(self, "changed")

    def execute(self):
        in_objectId = self.get_input_value("object Id")
        in_name = self.get_input_value("name")
        out_changed = False

        object_data = bpy.data.objects.get(in_objectId)

        if object_data:
            object_data.name = in_name
            out_changed = True
        else:
            print("Object data not found")

        add_linked_value(self, "changed", out_changed)

        self.execute_next("exec")

    def free(self):
        remove_linked_value(self, "changed")


class EGN_RenameData(EG_Node):
    """Rename object's data"""
    
    bl_idname = "EGN_RenameData"
    bl_label = "Rename Data"
    bl_icon = "RNA"

    def init(self, context):
        self.add_exec_in("exec")
        self.add_in("NodeSocketString", "object Id", 1, False)
        self.add_in("NodeSocketString", "name", 1, False)
        self.add_exec_out("exec")
        self.add_out("NodeSocketBool", "changed") # bind: changed -> on_changed

    def on_changed(self):
        return get_linked_value(self, "changed")

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

        add_linked_value(self, "changed", out_changed)
        self.execute_next("exec")

    def free(self):
        remove_linked_value(self, "changed")


classes = [
    EGN_GetObjectId,
    EGN_GetDataId,
    EGN_GetAllObjects,
    
    EGN_GetLocation,
    EGN_SetLocation,
    EGN_GetRotation,
    EGN_SetRotation,
    EGN_GetScale,
    EGN_SetScale,

    EGN_RenameObject,
    EGN_RenameData
]