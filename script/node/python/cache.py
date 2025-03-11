import uuid
import bpy
from bpy.props import ( BoolProperty, FloatProperty, EnumProperty, StringProperty, IntProperty, PointerProperty, CollectionProperty, FloatVectorProperty )

from ...base.node import EG_Node, EG_PureNode
from ...base.library import add_cache, get_cache, remove_cache, flush_cache, cache_map
from ...socket.primitive import EGS_Value


class EGN_SetCache(EG_Node):
    """Store or update a cache"""
    
    bl_idname = "egn.python.cache_set"
    bl_label = "Set Cache"
    bl_icon = "PACKAGE"

    def init(self, context):
        self.add_exec_in("exec")
        self.add_in("NodeSocketString", "name", 1, False)
        self.add_in(EGS_Value.bl_idname, "value")
        self.add_exec_out("exec")

    def execute(self):
        in_name = self.get_input_value("name")
        in_value = self.get_input_value("value")
        add_cache(in_name, in_value)
        self.execute_next("exec")


class EGN_GetCache(EG_PureNode):
    """Get the cached value"""
    
    bl_idname = "egn.python.cache_get"
    bl_label = "Get Cache"
    bl_icon = "PACKAGE"

    def init(self, context):
        self.add_in("NodeSocketString", "name", 1, False)
        self.add_out(EGS_Value.bl_idname, "value")

    def on_value(self):
        in_name = self.get_input_value("name")
        return get_cache(in_name)


class EGN_RemoveCache(EG_Node):
    """Remove the cached value"""
    
    bl_idname = "egn.python.cache_remove"
    bl_label = "Remove Cache"
    bl_icon = "PACKAGE"

    name: StringProperty(name="Name") # type: ignore

    def init(self, context):
        self.add_exec_in("exec")
        self.add_exec_out("exec")

    def draw_buttons(self, context, layout):
        layout.prop(self, "name")

    def execute(self):
        remove_cache(self.name)
        self.execute_next("exec")


class EGN_FlushCache(EG_Node):
    """Clear all runtime stored variables"""
    
    bl_idname = "egn.python.cache_flush"
    bl_label = "Flush Cache"
    bl_icon = "PACKAGE"

    def init(self, context):
        self.add_exec_in("exec")
        self.add_exec_out("exec")

    def execute(self):
        flush_cache()
        self.execute_next("exec")


class EGN_DumpCache(EG_Node):
    """Display all runtime stored in console"""
    
    bl_idname = "egn.python.cache_dump"
    bl_label = "Dump Cache"
    bl_icon = "PACKAGE"

    def init(self, context):
        self.add_exec_in("exec")
        self.add_exec_out("exec")

    def execute(self):
        print(cache_map)
        self.execute_next("exec")


classes = [
    EGN_SetCache,
    EGN_GetCache,
    EGN_RemoveCache,
    EGN_FlushCache,
    EGN_DumpCache
]