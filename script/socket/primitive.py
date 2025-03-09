from ..base.socket import EG_Socket


class EGS_Value(EG_Socket):
    """Event Value Socket"""
    
    bl_idname = "EGS_Value"
    bl_label = "Value"
    
    socket_color = (0.3, 0.3, 0.3, 1.0)


classes = [
    EGS_Value,
]