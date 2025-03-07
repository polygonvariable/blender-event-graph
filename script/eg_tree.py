import bpy

from .base.tree import EG_NodeTree

def register():
    bpy.utils.register_class(EG_NodeTree)

def unregister():
    bpy.utils.unregister_class(EG_NodeTree)