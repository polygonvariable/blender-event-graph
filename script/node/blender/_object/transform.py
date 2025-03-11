import bpy
from bpy.props import ( BoolProperty, FloatProperty, EnumProperty, StringProperty, IntProperty, PointerProperty, CollectionProperty, FloatVectorProperty )

from ....base.node import EG_Node, EG_PureNode
from ....base.library import add_linked_cache, remove_linked_cache, get_linked_cache
from ....socket.derived import EGS_Array
from ....socket.primitive import EGS_Value


class EGN_GetLocation(EG_PureNode):
    """Get the location of an object"""
    
    bl_idname = "egn.object.get_location"
    bl_label = "Get Location"
    bl_icon = "OBJECT_ORIGIN"

    def init(self, context):
        self.add_in("NodeSocketString", "object Id", 1, False)
        self.add_out("NodeSocketVector", "location") # bind: location -> on_location

    def on_location(self):
        if not self.target_object:
            return (0.0, 0.0, 0.0)
        return self.target_object.location


class EGN_SetLocation(EG_Node):
    """Set the location of an object"""
    
    bl_idname = "egn.object.set_location"
    bl_label = "Set Location"
    bl_icon = "OBJECT_ORIGIN"

    def init(self, context):
        self.add_exec_in("exec")
        self.add_in("NodeSocketString", "object Id", 1, False)
        self.add_in("NodeSocketVector", "location", 1, False)
        self.add_exec_out("exec")
        self.add_out("NodeSocketBool", "changed") # bind: changed -> on_changed

    def on_changed(self):
        return get_linked_cache(self, "changed")

    def execute(self):
        in_objectId = self.get_input_value("object Id")
        in_location = self.get_input_value("location")
        out_changed = False

        object_data = bpy.data.objects.get(in_objectId)

        if object_data:
            object_data.location = in_location
            out_changed = True

        add_linked_cache(self, "changed", out_changed)
        self.execute_next("exec")

    def free(self):
        remove_linked_cache(self, "changed")


class EGN_GetRotation(EG_PureNode):
    """Get the rotation of an object"""
    
    bl_idname = "egn.object.get_rotation"
    bl_label = "Get Rotation"
    bl_icon = "OBJECT_ORIGIN"

    def init(self, context):
        self.add_in("NodeSocketString", "object Id", 1, False)
        self.add_out("NodeSocketVector", "rotation") # bind: rotation -> on_rotation

    def on_rotation(self):
        if not self.target_object:
            return (0.0, 0.0, 0.0)
        return self.target_object.rotation_euler


class EGN_SetRotation(EG_Node):
    """Set the rotation of an object"""
    
    bl_idname = "egn.object.set_rotation"
    bl_label = "Set Rotation"
    bl_icon = "OBJECT_ORIGIN"

    def init(self, context):
        self.add_exec_in("exec")
        self.add_in("NodeSocketString", "object Id", 1, False)
        self.add_in("NodeSocketVector", "rotation", 1, False)
        self.add_exec_out("exec")
        self.add_out("NodeSocketBool", "changed") # bind: changed -> on_changed

    def on_changed(self):
        return get_linked_cache(self, "changed")

    def execute(self):
        in_objectId = self.get_input_value("object Id")
        in_rotation = self.get_input_value("rotation")
        out_changed = False

        object_data = bpy.data.objects.get(in_objectId)

        if object_data:
            object_data.rotation_euler = in_rotation
            out_changed = True

        add_linked_cache(self, "changed", out_changed)
        self.execute_next("exec")

    def free(self):
        remove_linked_cache(self, "changed")


class EGN_GetScale(EG_PureNode):
    """Get the scale of an object"""
    
    bl_idname = "egn.object.get_scale"
    bl_label = "Get Scale"
    bl_icon = "OBJECT_ORIGIN"

    def init(self, context):
        self.add_in("NodeSocketString", "object Id", 1, False)
        self.add_out("NodeSocketVector", "scale") # bind: scale -> on_scale

    def on_scale(self):
        if not self.target_object:
            return (0.0, 0.0, 0.0)
        return self.target_object.scale


class EGN_SetScale(EG_Node):
    """Set the scale of an object"""
    
    bl_idname = "egn.object.set_scale"
    bl_label = "Set Scale"
    bl_icon = "OBJECT_ORIGIN"

    def init(self, context):
        self.add_exec_in("exec")
        self.add_in("NodeSocketString", "object Id", 1, False)
        self.add_in("NodeSocketVector", "scale", 1, False)
        self.add_exec_out("exec")
        self.add_out("NodeSocketBool", "changed") # bind: changed -> on_changed

        self.inputs["scale"].default_value = (1.0, 1.0, 1.0)

    def on_changed(self):
        return get_linked_cache(self, "changed")
    
    def execute(self):
        in_objectId = self.get_input_value("object Id")
        in_scale = self.get_input_value("scale")
        out_changed = False

        object_data = bpy.data.objects.get(in_objectId)

        if object_data:
            object_data.scale = in_scale
            out_changed = True

        add_linked_cache(self, "changed", out_changed)
        self.execute_next("exec")

    def free(self):
        remove_linked_cache(self, "changed")


class EGN_GetDimension(EG_PureNode):
    """Get the dimension of an object"""
    
    bl_idname = "egn.object.get_dimension"
    bl_label = "Get Dimension"
    bl_icon = "OBJECT_ORIGIN"

    def init(self, context):
        self.add_in("NodeSocketString", "object Id", 1, False)
        self.add_out("NodeSocketVector", "dimension") # bind: dimension -> on_dimension

    def on_dimension(self):
        if not self.target_object:
            return (0.0, 0.0, 0.0)
        return self.target_object.dimensions


class EGN_SetDimension(EG_Node):
    """Set the dimension of an object"""
    
    bl_idname = "egn.object.set_dimension"
    bl_label = "Set Dimension"
    bl_icon = "OBJECT_ORIGIN"

    def init(self, context):
        self.add_exec_in("exec")
        self.add_in("NodeSocketString", "object Id", 1, False)
        self.add_in("NodeSocketVector", "dimension", 1, False)
        self.add_exec_out("exec")
        self.add_out("NodeSocketBool", "changed") # bind: changed -> on_changed

        self.inputs["dimension"].default_value = (1.0, 1.0, 1.0)

    def on_changed(self):
        return get_linked_cache(self, "changed")
    
    def execute(self):
        in_objectId = self.get_input_value("object Id")
        in_dimension = self.get_input_value("dimension")
        out_changed = False

        object_data = bpy.data.objects.get(in_objectId)

        if object_data:
            object_data.dimensions = in_dimension
            out_changed = True

        add_linked_cache(self, "changed", out_changed)
        self.execute_next("exec")

    def free(self):
        remove_linked_cache(self, "changed")


classes = [
    EGN_GetLocation,
    EGN_SetLocation,
    EGN_GetRotation,
    EGN_SetRotation,
    EGN_GetScale,
    EGN_SetScale,
    EGN_GetDimension,
    EGN_SetDimension,
]