import bpy
from bpy.props import ( BoolProperty, FloatProperty, EnumProperty, StringProperty, IntProperty, PointerProperty, CollectionProperty )
from bpy_extras.io_utils import ImportHelper

from ..base.library import flush_cache

class EGOP_ExecuteMain(bpy.types.Operator):
    """Execute Main Operator"""
    bl_idname = "egop.execute_main"
    bl_label = "Execute Main"

    def execute(self, context):
        node = context.active_node
        if node and node.bl_idname == "egn_python_function":

            # clear the old variables before executing
            # to prevent duplication
            flush_cache()
            result = node.execute()
            
            self.report({"INFO"}, f"Output Node Result: {result}")
            
        else:
            self.report({"WARNING"}, "Active node is not an define node")

        return {"FINISHED"}


classes = [ EGOP_ExecuteMain ]