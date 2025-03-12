import bpy
from bpy.props import ( BoolProperty, FloatProperty, EnumProperty, StringProperty, IntProperty, PointerProperty, CollectionProperty, FloatVectorProperty )

from ....base.node import EG_Node, EG_PureNode
from ....base.library import create_enum, add_linked_cache, remove_linked_cache, get_linked_cache

from ....socket.derived import EGS_Array
from ....socket.primitive import EGS_Value


class EGN_GetActiveObject(EG_PureNode):
    """Set the object to active"""
    
    bl_idname = "egn_object_get_active"
    bl_label = "Get Active Object"
    bl_icon = "OBJECT_ORIGIN"

    def init(self, context):
        self.add_out("NodeSocketString", "object Id") # bind: object Id -> on_object_Id

    def on_object_Id(self):
        active_object = bpy.context.view_layer.objects.active
        return active_object.name if active_object else ""


class EGN_SetActiveObject(EG_Node):
    """Set the object to active"""
    
    bl_idname = "egn_object_set_active"
    bl_label = "Set Active Object"
    bl_icon = "OBJECT_ORIGIN"

    def init(self, context):
        self.add_exec_in("exec")
        self.add_in("NodeSocketString", "object Id")
        self.add_exec_out("success")
        self.add_exec_out("failed")
    
    def execute(self):
        in_objectId = str(self.get_input_value("object Id"))
        object_data = bpy.data.objects.get(in_objectId)

        if object_data:
            bpy.context.view_layer.objects.active = object_data
            object_data.select_set(True)

            self.execute_next("success")
            
        else:
            self.execute_next("failed")


class EGN_ObjectSelectAll(EG_Node):
    """Select all action for objects in object mode"""
    
    bl_idname = "egn_object_select_all"
    bl_label = "Object Select All"
    bl_icon = "OBJECT_DATA"

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
        self.add_exec_out("exec")

    def draw_buttons(self, context, layout):
        layout.prop(self, "prop_action")

    def execute(self):
        bpy.ops.object.select_all(action=self.prop_action)

        if self.prop_action == "DESELECT":
            bpy.context.view_layer.objects.active = None

        self.execute_next("exec")


class EGN_GetObjectMode(EG_PureNode):
    """Get object mode"""
    
    bl_idname = "egn_object_get_mode"
    bl_label = "Get Object Mode"
    bl_icon = "TOOL_SETTINGS"

    def init(self, context):
        self.add_out("NodeSocketString", "mode") # bind: mode -> on_mode

    def on_mode(self):
        if bpy.context.object and bpy.context.object.mode:
            return bpy.context.object.mode
        else:
            return ""


class EGN_SetObjectMode(EG_Node):
    """Set object mode"""
    
    bl_idname = "egn_object_set_mode"
    bl_label = "Set Object Mode"
    bl_icon = "TOOL_SETTINGS"

    prop_mode: EnumProperty(
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
        self.add_exec_out("success")
        self.add_exec_out("failed")

    def execute(self):
        try:
            if not bpy.context.view_layer.objects.active:
                raise Exception("No active object")
            
            bpy.ops.object.mode_set(mode=self.prop_mode)
            self.execute_next("success")
            
        except Exception as e:
            print(e)
            self.execute_next("failed")


class EGN_SwitchObjectMode(EG_Node):
    """Switch on the object mode"""
    
    bl_idname = "egn_object_switch_mode"
    bl_label = "Switch Object Mode"
    bl_icon = "TOOL_SETTINGS"

    def init(self, context):
        self.add_exec_in("exec")
        self.add_exec_out("object")
        self.add_exec_out("edit")
        self.add_exec_out("sculpt")
        self.add_exec_out("vertex paint")
        self.add_exec_out("weight paint")
        self.add_exec_out("texture paint")
        self.add_exec_out("pose")
        self.add_exec_out("default")

    def execute(self):
        bl_object = bpy.context.object

        if bl_object and bl_object.mode:
            mode = bl_object.mode

            if mode == "OBJECT":
                self.execute_next("object")
            elif mode == "EDIT":
                self.execute_next("edit")
            elif mode == "SCULPT":
                self.execute_next("sculpt")
            elif mode == "VERTEX_PAINT":
                self.execute_next("vertex paint")
            elif mode == "WEIGHT_PAINT":
                self.execute_next("weight paint")
            elif mode == "TEXTURE_PAINT":
                self.execute_next("texture paint")
            elif mode == "POSE":
                self.execute_next("pose")
            else:
                self.execute_next("default")

        else:
            self.execute_next("default")
        


classes = [
    EGN_GetActiveObject,
    EGN_SetActiveObject,
    EGN_ObjectSelectAll,
    EGN_GetObjectMode,
    EGN_SetObjectMode,
    EGN_SwitchObjectMode
]