import bpy
from bpy.props import ( BoolProperty, FloatProperty, EnumProperty, StringProperty, IntProperty, PointerProperty, CollectionProperty, FloatVectorProperty )

from ...base.node import EG_Node, EG_PureNode
from ...base.library import create_enum, add_linked_value, remove_linked_value, get_linked_value, is_objectId_valid

from ...socket.derived import EGS_Array
from ...socket.primitive import EGS_Value



class EGN_GetObjectId(EG_PureNode):
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


class EGN_GetDataId(EG_PureNode):
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
    """Gets a list of all objects. This node may be unreliable if objects are modified externally, as the cached list will not reflect those changes"""
    
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


class EGN_FilterObjects(EG_Node):
    """Filter a list of objects by its type"""
    
    bl_idname = "EGN_FilterObjects"
    bl_label = "Filter Objects"
    bl_icon = "OBJECT_ORIGIN"

    object_type: EnumProperty(
        name="Type",
        items=[
            ("ARMATURE", "Armature", ""),
            ("CAMERA", "Camera", ""),
            ("CURVE", "Curve", ""),
            ("CURVES", "Curves", ""),
            ("EMPTY", "Empty", ""),
            ("FONT", "Font", ""),
            ("GREASEPENCIL", "Grease Pencil", ""),
            ("LATTICE", "Lattice", ""),
            ("LIGHT", "Light", ""),
            ("LIGHT_PROBE", "Light Probe", ""),
            ("MESH", "Mesh", ""),
            ("META", "Meta", ""),
            ("POINTCLOUD", "Point Cloud", ""),
            ("SPEAKER", "Speaker", ""),
            ("SURFACE", "Surface", ""),
            ("VOLUME", "Volume", ""),
        ]
    ) # type: ignore

    def init(self, context):
        self.add_exec_in("exec")
        self.add_in(EGS_Array.bl_idname, "object Ids")
        self.add_exec_out("exec")
        self.add_out(EGS_Array.bl_idname, "object Ids") # bind: object Ids -> on_object_Id

    def draw_buttons(self, context, layout):
        layout.prop(self, "object_type")

    def on_object_Ids(self):
        return get_linked_value(self, "object Ids")

    def execute(self):
        objects_Ids = self.get_input_value("object Ids")
        filtered_Ids = [obj for obj in objects_Ids if bpy.data.objects[obj].type == self.object_type]

        add_linked_value(self, "object Ids", filtered_Ids)
        self.execute_next("exec")

    def free(self):
        remove_linked_value(self, "object Ids")




class EGN_IsObjectValid(EG_Node):
    """Checks if an object is valid"""
    
    bl_idname = "EGN_IsObjectValid"
    bl_label = "Is Object Valid"
    bl_icon = "OBJECT_DATA"

    def init(self, context):
        self.add_exec_in("exec")
        self.add_in("NodeSocketString", "object Id")
        self.add_exec_out("exec")
        self.add_out("NodeSocketBool", "valid") # bind: is valid -> on_valid

    def on_valid(self):
        return get_linked_value(self, "valid")

    def execute(self):
        in_objectId = self.get_input_value("object Id")
        out_valid = False

        if is_objectId_valid(in_objectId):
            out_valid = True

        add_linked_value(self, "valid", out_valid)
        self.execute_next("exec")

    def free(self):
        remove_linked_value(self, "valid")


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
            object_data.type = ""
            out_changed = True
        else:
            print("Object not found")

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


class EGN_GetLocation(EG_PureNode):
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

        add_linked_value(self, "changed", out_changed)
        self.execute_next("exec")

    def free(self):
        remove_linked_value(self, "changed")


class EGN_GetRotation(EG_PureNode):
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

        add_linked_value(self, "changed", out_changed)
        self.execute_next("exec")

    def free(self):
        remove_linked_value(self, "changed")


class EGN_GetScale(EG_PureNode):
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

        add_linked_value(self, "changed", out_changed)
        self.execute_next("exec")

    def free(self):
        remove_linked_value(self, "changed")


class EGN_GetDimension(EG_PureNode):
    """Get the dimension of an object"""
    
    bl_idname = "EGN_GetDimension"
    bl_label = "Get Dimension"
    bl_icon = "OBJECT_ORIGIN"

    def init(self, context):
        self.add_in("NodeSocketString", "object Id", 1, False)
        self.add_out("NodeSocketVector", "dimension") # bind: dimension -> on_dimension

    def on_dimension(self):
        if not self.target_object:
            return (0.0, 0.0, 0.0)
        return self.target_object.dimensions


class EGN_SetDimension(EG_Node):
    """Set the dimension of an object"""
    
    bl_idname = "EGN_SetDimension"
    bl_label = "Set Dimension"
    bl_icon = "OBJECT_ORIGIN"

    def init(self, context):
        self.add_exec_in("exec")
        self.add_in("NodeSocketString", "object Id", 1, False)
        self.add_in("NodeSocketVector", "dimension", 1, False)
        self.add_exec_out("exec")
        self.add_out("NodeSocketBool", "changed") # bind: changed -> on_changed

        self.inputs["dimension"].default_value = (1.0, 1.0, 1.0)

    def on_changed(self):
        return get_linked_value(self, "changed")
    
    def execute(self):
        in_objectId = self.get_input_value("object Id")
        in_dimension = self.get_input_value("dimension")
        out_changed = False

        object_data = bpy.data.objects.get(in_objectId)

        if object_data:
            object_data.dimensions = in_dimension
            out_changed = True

        add_linked_value(self, "changed", out_changed)
        self.execute_next("exec")

    def free(self):
        remove_linked_value(self, "changed")


class EGN_GetActiveObject(EG_PureNode):
    """Set the object to active"""
    
    bl_idname = "EGN_GetActiveObject"
    bl_label = "Get Active Object"
    bl_icon = "OBJECT_ORIGIN"

    def init(self, context):
        self.add_out("NodeSocketString", "object Id") # bind: object Id -> on_object_Id

    def on_object_Id(self):
        object_Id = bpy.context.view_layer.objects.active
        return object_Id.name if object_Id else None


class EGN_SetActiveObject(EG_Node):
    """Set the object to active"""
    
    bl_idname = "EGN_SetActiveObject"
    bl_label = "Set Active Object"
    bl_icon = "OBJECT_ORIGIN"

    def init(self, context):
        self.add_exec_in("exec")
        self.add_in("NodeSocketString", "object Id", 1, False)
        self.add_exec_out("exec")
        self.add_out("NodeSocketBool", "success") # bind: success -> on_success

    def on_success(self):
        return get_linked_value(self, "success")
    
    def execute(self):
        in_objectId = self.get_input_value("object Id")
        out_success = False

        object_data = bpy.data.objects.get(in_objectId)

        if object_data:
            bpy.context.view_layer.objects.active = object_data
            object_data.select_set(True)
            out_success = True

        add_linked_value(self, "success", out_success)
        self.execute_next("exec")

    def free(self):
        remove_linked_value(self, "success")


class EGN_ClearActiveObject(EG_Node):
    """Clear the active object"""
    
    bl_idname = "EGN_ClearActiveObject"
    bl_label = "Clear Active Object"
    bl_icon = "OBJECT_ORIGIN"

    def init(self, context):
        self.add_exec_in("exec")
        self.add_exec_out("exec")

    def execute(self):
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = None
        self.execute_next("exec")


class EGN_GetViewportVisibility(EG_PureNode):
    """Get the viewport visibility of an object"""
    
    bl_idname = "EGN_GetViewportVisibility"
    bl_label = "Get Viewport Visibility"
    bl_icon = "OBJECT_ORIGIN"

    def init(self, context):
        self.add_in("NodeSocketString", "object Id")
        self.add_out("NodeSocketBool", "visible") # bind: visible -> on_visible

    def on_visible(self):
        in_objectId = self.get_input_value("object Id")
        object_data = bpy.data.objects.get(in_objectId)

        if object_data:
            return not object_data.hide_viewport

        return False


class EGN_SetViewportVisibility(EG_Node):
    """Set viewport visibility of an object"""
    
    bl_idname = "EGN_SetViewportVisibility"
    bl_label = "Set Viewport Visibility"
    bl_icon = "OBJECT_ORIGIN"

    def init(self, context):
        self.add_exec_in("exec")
        self.add_in("NodeSocketString", "object Id")
        self.add_in("NodeSocketBool", "visible", 1, False)
        self.add_exec_out("exec")

    def execute(self):
        in_objectId = self.get_input_value("object Id")
        in_visible = self.get_input_value("visible")

        object_data = bpy.data.objects.get(in_objectId)

        if object_data:
            object_data.hide_viewport = not in_visible

        self.execute_next("exec")


class EGN_GetRenderVisibility(EG_PureNode):
    """Get the render visibility of an object"""
    
    bl_idname = "EGN_GetRenderVisibility"
    bl_label = "Get Render Visibility"
    bl_icon = "OBJECT_ORIGIN"

    def init(self, context):
        self.add_in("NodeSocketString", "object Id")
        self.add_out("NodeSocketBool", "visible") # bind: visible -> on_visible

    def on_visible(self):
        in_objectId = self.get_input_value("object Id")
        object_data = bpy.data.objects.get(in_objectId)

        if object_data:
            return not object_data.hide_render

        return False


class EGN_SetRenderVisibility(EG_Node):
    """Set Render visibility of an object"""
    
    bl_idname = "EGN_SetRenderVisibility"
    bl_label = "Set Render Visibility"
    bl_icon = "OBJECT_ORIGIN"

    def init(self, context):
        self.add_exec_in("exec")
        self.add_in("NodeSocketString", "object Id")
        self.add_in("NodeSocketBool", "visible", 1, False)
        self.add_exec_out("exec")

    def execute(self):
        in_objectId = self.get_input_value("object Id")
        in_visible = self.get_input_value("visible")

        object_data = bpy.data.objects.get(in_objectId)

        if object_data:
            object_data.hide_render = not in_visible

        self.execute_next("exec")


class EGN_DeleteObject(EG_Node):
    """Delete an object"""
    
    bl_idname = "EGN_DeleteObject"
    bl_label = "Delete Object"
    bl_icon = "OBJECT_ORIGIN"

    def init(self, context):
        self.add_exec_in("exec")
        self.add_in("NodeSocketString", "object Id")
        self.add_exec_out("exec")
        self.add_out("NodeSocketBool", "success") # bind: success -> on_success

    def on_success(self):
        return get_linked_value(self, "success")

    def execute(self):
        in_objectId = self.get_input_value("object Id")
        out_success = False

        object_data = bpy.data.objects.get(in_objectId)

        if object_data:
            bpy.data.objects.remove(object_data, do_unlink=True)
            bpy.ops.ed.undo_push()

            out_success = True

        add_linked_value(self, "success", out_success)

        self.execute_next("exec")

    def free(self):
        remove_linked_value(self, "success")


class EGN_DuplicateObject(EG_Node):
    """Duplicate an object"""
    
    bl_idname = "EGN_DuplicateObject"
    bl_label = "Duplicate Object"
    bl_icon = "OBJECT_ORIGIN"

    def init(self, context):
        self.add_exec_in("exec")
        self.add_in("NodeSocketString", "object Id")
        self.add_exec_out("exec")
        self.add_out("NodeSocketString", "object Id") # bind: object Id -> on_object_Id
        self.add_out("NodeSocketBool", "success") # bind: success -> on_success

    def on_object_Id(self):
        return get_linked_value(self, "object Id")

    def on_success(self):
        return get_linked_value(self, "success")

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

        add_linked_value(self, "object Id", out_objectId)
        add_linked_value(self, "success", out_success)

        self.execute_next("exec")

    def free(self):
        remove_linked_value(self, "object Id")
        remove_linked_value(self, "success")


classes = [
    EGN_GetObjectId,
    EGN_GetDataId,
    EGN_GetAllObjects,
    EGN_FilterObjects,
    
    EGN_IsObjectValid,

    EGN_RenameObject,
    EGN_RenameData,

    EGN_GetLocation,
    EGN_SetLocation,
    EGN_GetRotation,
    EGN_SetRotation,
    EGN_GetScale,
    EGN_SetScale,
    EGN_GetDimension,
    EGN_SetDimension,

    EGN_GetActiveObject,
    EGN_SetActiveObject,
    EGN_ClearActiveObject,

    EGN_GetViewportVisibility,
    EGN_SetViewportVisibility,
    EGN_GetRenderVisibility,
    EGN_SetRenderVisibility,

    EGN_DeleteObject,
    EGN_DuplicateObject
]