from ..base.socket import EG_Socket


class EGS_Object(EG_Socket):
    """Event Object Socket"""
    
    bl_idname = "egs_object"
    bl_label = "Object"
    
    socket_color = (1.0, 0.30, 0.60, 1.0)


class EGS_Reference(EG_Socket):
    """Event Reference Socket"""
    
    bl_idname = "egs_reference"
    bl_label = "Reference"
    
    socket_color = (0.71, 0.32, 1.0, 1.0)

class EGS_Modifier(EG_Socket):
    """Blender's Modifier Socket"""
    
    bl_idname = "egs_bl_modifier"
    bl_label = "Modifier"
    
    socket_color = (0.549, 0.349, 0.71, 1.0)

classes = [
    EGS_Object,
    EGS_Reference,
    EGS_Modifier
]