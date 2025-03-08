from ..base.socket import EG_Socket


class EGS_Object(EG_Socket):
    """Event Object Socket"""
    
    bl_idname = "EGS_Object"
    bl_label = "Object"
    
    socket_color = (1.0, 0.30, 0.60, 1.0)


class EGS_Reference(EG_Socket):
    """Event Reference Socket"""
    
    bl_idname = "EGS_Reference"
    bl_label = "Reference"
    
    socket_color = (0.71, 0.32, 1.0, 1.0)


classes = [
    EGS_Object,
    EGS_Reference
]