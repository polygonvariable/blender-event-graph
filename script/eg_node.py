import bpy

from .node import base
from .node import cast
from .node import literal

classes = []
classes += base.classes + cast.classes + literal.classes

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)