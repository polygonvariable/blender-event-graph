from ..base.socket import EG_Socket


class EGS_Execute(EG_Socket):
    """Event Socket Execute"""
    
    bl_idname = "EGS_Execute"
    bl_label = "Execute"

    socket_title = "exec"
    socket_color = (0.9, 0.9, 0.9, 1.0)

    def __init__(self):
        super().__init__()
        self.display_shape = "DIAMOND"


class EGS_Array(EG_Socket):
    """Event Socket Array"""
    
    bl_idname = "EGS_Array"
    bl_label = "Array"
    
    socket_title = "array"
    socket_color = (0.98, 0.54, 0.40, 1.0)


classes = [
    EGS_Execute,
    EGS_Array
]