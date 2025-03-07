from ..base.socket import EG_Socket

class EGS_Execute(EG_Socket):
    """Event Socket Execute"""
    
    bl_idname = "EGS_Execute"
    bl_label = "Execute"
    
    socket_title = "exec"
    socket_color = (0.66, 0.09, 1.0, 1.0)

class EGS_Value(EG_Socket):
    """Event Socket Value"""
    
    bl_idname = "EGS_Value"
    bl_label = "Value"
    
    socket_limit = 100
    socket_title = "value"
    socket_color = (0.25, 0.52, 0.52, 1.0)


class EGS_Integer(EG_Socket):
    """Event Integer Socket"""
    
    bl_idname = "EGS_Integer"
    bl_label = "Integer"
    
    socket_limit = 100
    socket_title = "int"
    socket_color = (0.267, 0.722, 0.588, 1.0)


class EGS_Float(EG_Socket):
    """Event Float Socket"""
    
    bl_idname = "EGS_Float"
    bl_label = "Float"
    
    socket_limit = 100
    socket_title = "float"
    socket_color = (0.133, 1, 0.11, 1.0)


class EGS_String(EG_Socket):
    """Event String Socket"""
    
    bl_idname = "EGS_String"
    bl_label = "String"
    
    socket_limit = 100
    socket_title = "string"
    socket_color = (1, 0.263, 0.929, 1.0)


class EGS_Boolean(EG_Socket):
    """Event Boolean Socket"""
    
    bl_idname = "EGS_Boolean"
    bl_label = "Boolean"
    
    socket_limit = 100
    socket_title = "bool"
    socket_color = (1, 0.314, 0.263, 1.0)


class EGS_Array(EG_Socket):
    """Event Socket Array"""
    
    bl_idname = "EGS_Array"
    bl_label = "Array"
    
    socket_limit = 100
    socket_title = "array"
    socket_color = (0.98, 0.54, 0.40, 1.0)


classes = [
    EGS_Execute,
    EGS_Value,
    EGS_Integer,
    EGS_Float,
    EGS_String,
    EGS_Boolean,
    EGS_Array
]