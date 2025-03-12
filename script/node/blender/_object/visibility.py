import bpy
from bpy.props import ( BoolProperty, FloatProperty, EnumProperty, StringProperty, IntProperty, PointerProperty, CollectionProperty, FloatVectorProperty )

from ....base.node import EG_Node, EG_PureNode

from ....socket.derived import EGS_Array
from ....socket.primitive import EGS_Value


class EGN_GetViewportVisibility(EG_PureNode):
    """Get the viewport visibility of an object"""
    
    bl_idname = "egn_object_get_viewport_visibility"
    bl_label = "Get Viewport Visibility"
    bl_icon = "HIDE_OFF"

    def init(self, context):
        self.add_in("NodeSocketString", "object Id")
        self.add_out("NodeSocketBool", "visible") # bind: visible -> on_visible

    def on_visible(self):
        in_objectId = str(self.get_input_value("object Id"))
        bl_object = bpy.data.objects.get(in_objectId)

        if bl_object:
            return not bl_object.hide_viewport

        return False


class EGN_SetViewportVisibility(EG_Node):
    """Set viewport visibility of an object"""
    
    bl_idname = "egn_object_set_viewport_visibility"
    bl_label = "Set Viewport Visibility"
    bl_icon = "HIDE_OFF"

    def init(self, context):
        self.add_exec_in("exec")
        self.add_in("NodeSocketString", "object Id")
        self.add_in(socket="NodeSocketBool", name="visible", hide_value=False)
        self.add_exec_out("success")
        self.add_exec_out("failed")

    def execute(self):
        in_objectId = str(self.get_input_value("object Id"))
        in_visible = bool(self.get_input_value("visible"))

        bl_object = bpy.data.objects.get(in_objectId)

        if bl_object:
            bl_object.hide_viewport = not in_visible
            self.execute_next("success")

        else:
            self.execute_next("failed")


class EGN_GetRenderVisibility(EG_PureNode):
    """Get the render visibility of an object"""
    
    bl_idname = "egn_object_get_render_visibility"
    bl_label = "Get Render Visibility"
    bl_icon = "RESTRICT_RENDER_OFF"

    def init(self, context):
        self.add_in("NodeSocketString", "object Id")
        self.add_out("NodeSocketBool", "visible") # bind: visible -> on_visible

    def on_visible(self):
        in_objectId = str(self.get_input_value("object Id"))
        bl_object = bpy.data.objects.get(in_objectId)

        if bl_object:
            return not bl_object.hide_render

        return False


class EGN_SetRenderVisibility(EG_Node):
    """Set Render visibility of an object"""
    
    bl_idname = "egn_object_set_render_visibility"
    bl_label = "Set Render Visibility"
    bl_icon = "RESTRICT_RENDER_OFF"

    def init(self, context):
        self.add_exec_in("exec")
        self.add_in("NodeSocketString", "object Id")
        self.add_in(socket="NodeSocketBool", name="visible", hide_value=False)
        self.add_exec_out("success")
        self.add_exec_out("failed")

    def execute(self):
        in_objectId = str(self.get_input_value("object Id"))
        in_visible = bool(self.get_input_value("visible"))

        bl_object = bpy.data.objects.get(in_objectId)

        if bl_object:
            bl_object.hide_render = not in_visible
            self.execute_next("success")

        else:
            self.execute_next("failed")


classes = [
    EGN_GetViewportVisibility,
    EGN_SetViewportVisibility,
    EGN_GetRenderVisibility,
    EGN_SetRenderVisibility,
]