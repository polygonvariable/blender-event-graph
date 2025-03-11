import bpy
from bpy.props import ( BoolProperty, FloatProperty, EnumProperty, StringProperty, IntProperty, PointerProperty, CollectionProperty, FloatVectorProperty )

from ....base.node import EG_Node, EG_PureNode
from ....base.library import create_enum, add_linked_cache, remove_linked_cache, get_linked_cache

from ....socket.derived import EGS_Array
from ....socket.primitive import EGS_Value


class EGN_GetActiveObject(EG_PureNode):
    """Set the object to active"""
    
    bl_idname = "egn.object.get_active"
    bl_label = "Get Active Object"
    bl_icon = "OBJECT_ORIGIN"

    def init(self, context):
        self.add_out("NodeSocketString", "object Id") # bind: object Id -> on_object_Id

    def on_object_Id(self):
        object_Id = bpy.context.view_layer.objects.active
        return object_Id.name if object_Id else None


class EGN_SetActiveObject(EG_Node):
    """Set the object to active"""
    
    bl_idname = "egn.object.set_active"
    bl_label = "Set Active Object"
    bl_icon = "OBJECT_ORIGIN"

    def init(self, context):
        self.add_exec_in("exec")
        self.add_in("NodeSocketString", "object Id", 1, False)
        self.add_exec_out("success")
        self.add_exec_out("failed")
    
    def execute(self):
        try:
            in_objectId = self.get_input_value("object Id")

            object_data = bpy.data.objects.get(in_objectId)
            if object_data:
                bpy.context.view_layer.objects.active = object_data
                object_data.select_set(True)

            self.execute_next("success")
            
        except Exception as e:
            print(e)
            self.execute_next("failed")


class EGN_SelectAllObjects(EG_Node):
    """Select all objects"""
    
    bl_idname = "egn.object.select_all"
    bl_label = "Select All Objects"
    bl_icon = "ADD"

    def init(self, context):
        self.add_exec_in("exec")
        self.add_exec_out("success")
        self.add_exec_out("failed")

    def execute(self):
        try:
            bpy.ops.object.select_all(action="SELECT")
            self.execute_next("success")
        except Exception as e:
            print(e)
            self.execute_next("failed")


class EGN_DeselectAllObjects(EG_Node):
    """Unselect all objects"""
    
    bl_idname = "egn.object.deselect_all"
    bl_label = "Deselect All Objects"
    bl_icon = "REMOVE"

    def init(self, context):
        self.add_exec_in("exec")
        self.add_exec_out("success")
        self.add_exec_out("failed")

    def execute(self):
        try:
            bpy.ops.object.select_all(action="DESELECT")
            bpy.context.view_layer.objects.active = None
            self.execute_next("success")
        except Exception as e:
            print(e)
            self.execute_next("failed")


class EGN_SetObjectMode(EG_Node):
    """Set object mode"""
    
    bl_idname = "egn.object.set_mode"
    bl_label = "Set Object Mode"
    bl_icon = "TOOL_SETTINGS"

    object_mode: EnumProperty(
        name="Mode",
        items=[
            ("OBJECT", "Object", ""),
            ("EDIT", "Edit", ""),
            ("SCULPT", "Sculpt", ""),
            ("VERTEX_PAINT", "Vertex Paint", ""),
            ("WEIGHT_PAINT", "Weight Paint", ""),
            ("TEXTURE_PAINT", "Texture Paint", ""),
            ("POSE", "Pose", ""),
        ],
        default="OBJECT",
    ) # type: ignore

    def init(self, context):
        self.add_exec_in("exec")
        self.add_exec_out("exec")
        self.add_out("NodeSocketBool", "changed") # bind: changed -> on_changed

    def draw_buttons(self, context, layout):
        layout.prop(self, "object_mode")

    def on_changed(self):
        return get_linked_cache(self, "changed")

    def execute(self):
        try:
            if not bpy.context.view_layer.objects.active:
                raise Exception("No active object")
            
            bpy.ops.object.mode_set(mode=self.object_mode)
            add_linked_cache(self, "changed", True)
            self.execute_next("exec")
            
        except Exception as e:
            print(e)
            add_linked_cache(self, "changed", False)
            self.execute_next("exec")


classes = [
    EGN_GetActiveObject,
    EGN_SetActiveObject,
    EGN_SelectAllObjects,
    EGN_DeselectAllObjects,
    EGN_SetObjectMode
]