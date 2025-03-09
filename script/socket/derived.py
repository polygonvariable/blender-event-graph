
from ..base.socket import EG_Socket


class EGS_Execute(EG_Socket):
    """Socket to handle flow of execution"""
    
    bl_idname = "EGS_Execute"
    bl_label = "Execute"

    socket_color = (0.9, 0.9, 0.9, 1.0)

    def __init__(self):
        super().__init__()
        self.display_shape = "DIAMOND"


class EGS_Vector2D(EG_Socket):
    """Vector 2D Socket"""
    
    bl_idname = "EGS_Vector2D"
    bl_label = "Vector 2D"
    
    socket_color = (0.18, 0.31, 1.0, 1.0)
    

class EGS_Vector4D(EG_Socket):
    """Vector 4D Socket"""
    
    bl_idname = "EGS_Vector4D"
    bl_label = "Vector 4D"
    
    socket_color = (0.45, 0.05, 1.0, 1.0)


class EGS_Array(EG_Socket):
    """Wildcard Array Socket"""
    
    bl_idname = "EGS_Array"
    bl_label = "Array"
    
    # socket_color = (0.4, 0.4, 0.4, 1.0)
    socket_color = (0.6, 0.2, 0.4, 1.0)

    def __init__(self):
        super().__init__()
        self.display_shape = "SQUARE"


class EGS_Set(EG_Socket):
    """Wildcard Set Socket"""
    
    bl_idname = "EGS_Set"
    bl_label = "Set"
    
    socket_color = (0.2, 0.4, 0.6, 1.0)

    def __init__(self):
        super().__init__()
        self.display_shape = "SQUARE"


class EGS_Map(EG_Socket):
    """Map Socket"""
    
    bl_idname = "EGS_Map"
    bl_label = "Map"
    
    socket_color = (0.4, 0.6, 0.2, 1.0)

    def __init__(self):
        super().__init__()
        self.display_shape = "SQUARE"


classes = [
    EGS_Execute,
    EGS_Array,
    EGS_Set,
    EGS_Map,
    EGS_Vector2D,
    EGS_Vector4D
]