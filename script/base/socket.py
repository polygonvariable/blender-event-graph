import bpy
from bpy.types import NodeSocket
from bpy.props import ( BoolProperty, FloatProperty, EnumProperty, StringProperty, IntProperty, PointerProperty )


class EG_Socket(NodeSocket):
    """Event Socket"""

    bl_idname = "EG_Socket"
    bl_label = "Event Socket"

    socket_color = (1.0, 1.0, 1.0, 1.0)

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def draw_color(self, context, node):
        return self.socket_color
    