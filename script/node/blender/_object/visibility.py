import bpy
from bpy.props import ( BoolProperty, FloatProperty, EnumProperty, StringProperty, IntProperty, PointerProperty, CollectionProperty, FloatVectorProperty )

from ....base.node import EG_Node, EG_PureNode

from ....socket.derived import EGS_Array
from ....socket.primitive import EGS_Value


class EGN_GetViewportVisibility(EG_PureNode):
    """Get the viewport visibility of an object"""
    
    bl_idname = "egn.object.get_viewport_visibility"
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
    
    bl_idname = "egn.object.set_viewport_visibility"
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
    
    bl_idname = "egn.object.get_render_visibility"
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
    
    bl_idname = "egn.object.set_render_visibility"
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


classes = [
    EGN_GetViewportVisibility,
    EGN_SetViewportVisibility,
    EGN_GetRenderVisibility,
    EGN_SetRenderVisibility,
]