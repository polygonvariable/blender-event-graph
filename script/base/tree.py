import bpy

class EG_NodeTree(bpy.types.NodeTree):
    """Event Event Graph"""
    bl_idname = "eg.node_tree"
    bl_label = "Event Graph"
    bl_icon = "EXPERIMENTAL"