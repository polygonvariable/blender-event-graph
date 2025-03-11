import bpy
from bpy.props import ( BoolProperty, FloatProperty, EnumProperty, StringProperty, IntProperty, PointerProperty, CollectionProperty, FloatVectorProperty )

from ...base.node import EG_Node, EG_PureNode
from ...base.library import create_enum, add_linked_cache, remove_linked_cache, get_linked_cache, is_objectId_valid

from ...socket.derived import EGS_Array
from ...socket.primitive import EGS_Value

# event_nodes = set()
# def on_frame_change(scene):
#     for node in event_nodes:
#         node.execute_previous("callback")
# class EGN_OnFrameChangePost(EG_Node):
#     """A Callback Node to execute on frame change, delete node to remove handler"""
#     bl_idname = "EGN_OnFrameChangePost"
#     bl_label = "On Frame Change"
#     bl_icon = "FF"
#     prop_registered: BoolProperty(default=False) # type: ignore
#     def init(self, context):
#         self.add_exec_in("exec")
#         self.add_exec_in("callback", 1)
#         self.add_exec_out("exec")
#     def execute(self):
#         if not self.prop_registered:
#             event_nodes.add(self)
#             if on_frame_change not in bpy.app.handlers.frame_change_post:
#                 bpy.app.handlers.frame_change_post.append(on_frame_change)
#             self.prop_registered = True
#         self.execute_next("exec")
#     def free(self):
#         if self in event_nodes:
#             event_nodes.remove(self)
#         if not event_nodes and on_frame_change in bpy.app.handlers.frame_change_post:
#             bpy.app.handlers.frame_change_post.remove(on_frame_change)
#             self.prop_registered = False