import uuid
import bpy
from bpy.props import ( BoolProperty, FloatProperty, EnumProperty, StringProperty, IntProperty, PointerProperty, CollectionProperty, FloatVectorProperty )

from ...base.node import EG_Node
from ...base.library import flush_variables, variable_map

from ...socket.user import EGS_Object
from ...socket.primitive import EGS_Value

from ...operator.exec_main import EGOP_ExecuteMain


class EGN_FlushCache(EG_Node):
    """Clear all runtime stored variables"""
    
    bl_idname = "EGN_FlushCache"
    bl_label = "Flush Cache"

    def init(self, context):
        self.add_exec_in("exec")
        self.add_exec_out("exec")

    def execute(self):
        flush_variables()
        self.execute_next("exec")


class EGN_DumpCache(EG_Node):
    """Display all runtime stored variables"""
    
    bl_idname = "EGN_DumpCache"
    bl_label = "Dump Cache"

    def init(self, context):
        self.add_exec_in("exec")
        self.add_exec_out("exec")

    def execute(self):
        print(variable_map)
        self.execute_next("exec")


classes = [
    EGN_FlushCache,
    EGN_DumpCache
]