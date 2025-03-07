import bpy
from bpy.types import NodeSocket
from bpy.props import ( BoolProperty, FloatProperty, EnumProperty, StringProperty, IntProperty, PointerProperty )


class EG_Socket(NodeSocket):
    """Event Socket"""

    bl_idname = "EG_Socket"
    bl_label = "Event Socket"

    socket_limit = 1
    socket_title = ""
    socket_color = (1.0, 1.0, 1.0, 1.0)

    def __init__(self):
        self.link_limit = self.socket_limit

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def draw_color(self, context, node):
        return self.socket_color