import bpy
from bpy.types import AddonPreferences
from bpy.props import ( StringProperty, BoolProperty )

from .base.library import get_package_name

class EG_Preference(AddonPreferences):
    bl_idname = get_package_name()

def register():
    bpy.utils.register_class(EG_Preference)

def unregister():
    bpy.utils.unregister_class(EG_Preference)