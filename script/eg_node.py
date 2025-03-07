import bpy

from .node import base
from .node import literal

classes = []
classes += base.classes + literal.classes

def register():
    for cls in classes:
        print(cls.bl_idname)
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)