import bpy
from bpy.props import ( BoolProperty, FloatProperty, EnumProperty, StringProperty, IntProperty, PointerProperty, CollectionProperty, FloatVectorProperty )

from ...base.node import EG_Node
from ...base.library import get_linked_cache, remove_linked_cache, add_linked_cache, is_vector

from ...socket.primitive import EGS_Value


class EGN_CreateLight(EG_Node):
    """Creates a Light and returns its data and object Ids"""
    
    bl_idname = "egn_light_create"
    bl_label = "Create Light"
    bl_icon = "LIGHT"

    light_type: EnumProperty(
        name="Type", 
        items=[("POINT", "Point", ""), ("SPOT", "Spot", ""), ("AREA", "Area", ""), ("SUN", "Sun", "")],
        default="POINT"
    ) # type: ignore

    prop_dataId: StringProperty(name="data Id") # type: ignore
    prop_objectId: StringProperty(name="object Id") # type: ignore
    
    def init(self, context):
        self.add_exec_in("exec")
        self.add_in(socket="NodeSocketString", name="name", hide_value=False, default="Light")
        self.add_in(socket="NodeSocketFloat", name="intensity", hide_value=False, default=1.0)
        self.add_in(socket="NodeSocketColor", name="color", hide_value=False, default=(1.0, 1.0, 1.0, 1.0))
        self.add_in(socket="NodeSocketVector", name="location", hide_value=False, default=(0.0, 0.0, 0.0))
        self.add_in(socket="NodeSocketBool", name="enable shadow", hide_value=False, default=True)

        self.add_exec_out("success")
        self.add_exec_out("failed")
        self.add_out("NodeSocketString", "data Id") # bind: dataId -> on_data_Id
        self.add_out("NodeSocketString", "object Id") # bind: objectId -> on_object_Id

    def draw_buttons(self, context, layout):
        layout.prop(self, "light_type")

    def on_data_Id(self):
        return self.prop_dataId

    def on_object_Id(self):
        return self.prop_objectId

    def execute(self):
        try:

            self.prop_dataId = ""
            self.prop_objectId = ""

            in_name = str(self.get_input_value("name"))
            if not in_name:
                raise Exception("Name cannot be empty")

            in_type = self.light_type
            in_color = tuple(self.get_input_value("color"))
            in_location = tuple(self.get_input_value("location"))
            in_intensity = float(self.get_input_value("intensity"))
            in_shadow = bool(self.get_input_value("shadow"))

            light_data = bpy.data.lights.get(in_name)
            if light_data:
                raise Exception("Light already exists")

            light_data = bpy.data.lights.new(in_name, in_type)
            light_data.color = in_color[:3]
            light_data.energy = in_intensity
            light_data.use_shadow = in_shadow

            light_object = bpy.data.objects.get(in_name)
            if in_name in bpy.data.objects:
                raise Exception("Light object already exists")
            
            light_object = bpy.data.objects.new(in_name, light_data)
            
            if light_object.name not in bpy.context.scene.collection.objects:
                bpy.context.scene.collection.objects.link(light_object)
                light_object.location = in_location

            bpy.context.view_layer.update()

            self.prop_dataId = light_data.name
            self.prop_objectId = light_data.name

            self.execute_next("success")

        except Exception as e:
            print(e)
            self.execute_next("failed")


class EGN_GetIntensity(EG_Node):
    """Get the intensity of a light"""
    
    bl_idname = "egn_light_get_intensity"
    bl_label = "Get Intensity"
    bl_icon = "LIGHT"

    def init(self, context):
        self.add_in("NodeSocketString", "data Id")
        self.add_out("NodeSocketFloat", "intensity") # bind: intensity -> on_intensity

    def on_intensity(self):
        in_dataId = float(self.get_input_value("data Id"))
        light_data = bpy.data.lights.get(in_dataId)

        if light_data:
            return light_data.energy
        
        return -1


class EGN_SetIntensity(EG_Node):
    """Set the intensity of a light"""
    
    bl_idname = "egn_light_set_intensity"
    bl_label = "Set Intensity"
    bl_icon = "LIGHT"

    def init(self, context):
        self.add_exec_in("exec")
        self.add_in("NodeSocketString", "data Id")
        self.add_in(socket="NodeSocketFloat", name="intensity", hide_value=False, default=1.0)
        self.add_exec_out("success")
        self.add_exec_out("failed")

    def execute(self):
        in_dataId = str(self.get_input_value("data Id"))
        in_intensity = float(self.get_input_value("intensity"))

        light_data = bpy.data.lights.get(in_dataId)

        if light_data:
            light_data.energy = in_intensity
            self.execute_next("success")
        
        else:
            self.execute_next("failed")


class EGN_GetColor(EG_Node):
    """Get the color of a light"""
    
    bl_idname = "egn_light_get_color"
    bl_label = "Get Color"
    bl_icon = "LIGHT"

    def init(self, context):
        self.add_in("NodeSocketString", "data Id")
        self.add_out("NodeSocketColor", "color") # bind: color -> on_color

    def on_color(self):
        in_dataId = str(self.get_input_value("data Id"))
        light_data = bpy.data.lights.get(in_dataId)

        if not light_data:
            return tuple((0.0, 0.0, 0.0))
        
        return tuple(light_data.color)
        

class EGN_SetColor(EG_Node):
    """Set the color of a light"""
    
    bl_idname = "egn_light_set_color"
    bl_label = "Set Color"
    bl_icon = "LIGHT"

    def init(self, context):
        self.add_exec_in("exec")
        self.add_in("NodeSocketString", "data Id")
        self.add_in(socket="NodeSocketColor", name="color", hide_value=False)
        self.add_exec_out("success")
        self.add_exec_out("failed")

    def execute(self):
        in_dataId = str(self.get_input_value("data Id"))
        in_color = tuple(self.get_input_value("color"))

        light_data = bpy.data.lights.get(in_dataId)

        if light_data:
            light_data.color = in_color[:3]
            self.execute_next("success")

        else:
            self.execute_next("failed")


classes = [
    EGN_CreateLight,
    EGN_GetIntensity,
    EGN_SetIntensity,
    EGN_GetColor,
    EGN_SetColor
]