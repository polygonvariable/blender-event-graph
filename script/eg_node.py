import bpy

from .node import base, cast, literal, string as n_string, light

classes = []
classes += base.classes + cast.classes + literal.classes + n_string.classes + light.classes

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)