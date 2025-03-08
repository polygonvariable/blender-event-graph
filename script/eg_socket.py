import bpy

from .socket import derived, primitive, user

classes = []
classes += derived.classes + primitive.classes + user.classes

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)