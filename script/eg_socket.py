import bpy

from .socket import derived
from .socket import primitive

classes = []
classes += derived.classes + primitive.classes

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)