import bpy
from bpy.props import ( BoolProperty, FloatProperty, EnumProperty, StringProperty, IntProperty, PointerProperty, CollectionProperty, FloatVectorProperty )

from ....base.node import EG_Node, EG_PureNode
from ....base.library import create_enum, add_linked_cache, remove_linked_cache, get_linked_cache

from ....socket.derived import EGS_Array
from ....socket.primitive import EGS_Value


class EGN_GetObjectId(EG_PureNode):
    """Get the object id"""
    
    bl_idname = "egn_object_get_id"
    bl_label = "Get Object Id"
    bl_icon = "OBJECT_ORIGIN"

    target_object: PointerProperty(name="Object", type=bpy.types.Object) # type: ignore

    def init(self, context):
        self.add_out("NodeSocketString", "object Id") # bind: object Id -> on_object_Id

    def draw_buttons(self, context, layout):
        layout.prop(self, "target_object")

    def on_object_Id(self):
        return self.target_object.name if self.target_object else ""


class EGN_GetDataId(EG_PureNode):
    """Get the data id by object id"""
    
    bl_idname = "egn_object_get_data_id"
    bl_label = "Get Data Id"
    bl_icon = "RNA"

    def init(self, context):
        self.add_in("NodeSocketString", "object Id")
        self.add_out("NodeSocketString", "data Id") # bind: data Id -> on_data_Id

    def on_data_Id(self):
        in_objectId = str(self.get_input_value("object Id"))
        bl_object = bpy.data.objects.get(in_objectId)

        return bl_object.data.name if bl_object and bl_object.data else ""


class EGN_GetAllObjects(EG_Node):
    """Gets a list of all objects. This node may be unreliable if objects are modified externally, as the cached list will not reflect those changes"""
    
    bl_idname = "egn_object_get_all"
    bl_label = "Get All Objects"
    bl_icon = "OBJECT_ORIGIN"

    def init(self, context):
        self.add_exec_in("exec")
        self.add_exec_out("exec")
        self.add_out(EGS_Array.bl_idname, "object Ids") # bind: object Ids -> on_object_Id

    def on_object_Ids(self):
        cache_value = get_linked_cache(self, "object Ids")
        return cache_value if cache_value else []

    def execute(self):
        object_Ids = [obj.name for obj in bpy.data.objects]
        add_linked_cache(self, "object Ids", object_Ids)
        self.execute_next("exec")

    def free(self):
        remove_linked_cache(self, "object Ids")


class EGN_FilterObjects(EG_Node):
    """Filter a list of objects by its type"""
    
    bl_idname = "egn_object_filter"
    bl_label = "Filter Objects"
    bl_icon = "FILTER"

    prop_type: EnumProperty(
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
        layout.prop(self, "prop_type")

    def on_object_Ids(self):
        cache_value = get_linked_cache(self, "object Ids")
        return cache_value if cache_value else []

    def execute(self):
        objects_Ids = self.get_input_value("object Ids")

        if not isinstance(objects_Ids, list):
            objects_Ids = []

        filtered_Ids = [obj for obj in objects_Ids if obj in bpy.data.objects and bpy.data.objects[obj].type == self.prop_type]

        add_linked_cache(self, "object Ids", filtered_Ids)
        self.execute_next("exec")

    def free(self):
        remove_linked_cache(self, "object Ids")


class EGN_IsObjectValid(EG_Node):
    """Checks if an object is valid"""
    
    bl_idname = "egn_object_is_valid"
    bl_label = "Is Object Valid"
    bl_icon = "OBJECT_DATA"

    def init(self, context):
        self.add_exec_in("exec")
        self.add_in("NodeSocketString", "object Id")
        self.add_exec_out("valid")
        self.add_exec_out("invalid")
    
    def execute(self):
        in_objectId = str(self.get_input_value("object Id"))
        if bpy.data.objects.get(in_objectId):
            self.execute_next("valid")

        else:
            self.execute_next("invalid")


class EGN_GetParent(EG_PureNode):
    """Get the parent of an object"""
    
    bl_idname = "egn_object_get_parent"
    bl_label = "Get Parent"
    bl_icon = "OBJECT_ORIGIN"

    def init(self, context):
        self.add_in(socket="NodeSocketString", name="object Id")
        self.add_out(socket="NodeSocketString", name="parent Id") # bind: parent Id -> on_parent_Id
    
    def on_parent_Id(self):
        in_objectId = str(self.get_input_value("object Id"))
        bl_object = bpy.data.objects.get(in_objectId)

        return bl_object.parent.name if bl_object and bl_object.parent else ""


class EGN_GetChildren(EG_PureNode):
    """Get the children of an object"""
    
    bl_idname = "egn_object_get_children"
    bl_label = "Get Children"
    bl_icon = "OBJECT_ORIGIN"

    def init(self, context):
        self.add_in(socket="NodeSocketString", name="object Id")
        self.add_out(socket=EGS_Array.bl_idname, name="children Ids") # bind: children Ids -> on_children_Ids
    
    def on_children_Ids(self):
        in_objectId = str(self.get_input_value("object Id"))
        bl_object = bpy.data.objects.get(in_objectId)

        if bl_object and bl_object.children:
            return [child.name for child in bl_object.children]
        
        return []


classes = [
    EGN_GetObjectId,
    EGN_GetDataId,
    EGN_GetAllObjects,
    EGN_FilterObjects,
    EGN_IsObjectValid,
    EGN_GetParent,
    EGN_GetChildren
]