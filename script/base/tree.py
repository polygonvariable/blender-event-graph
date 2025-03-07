import bpy

class EG_NodeTree(bpy.types.NodeTree):
    """Event Event Graph"""
    bl_idname = "EG_NodeTree"
    bl_label = "Event Graph"
    bl_icon = "EXPERIMENTAL"