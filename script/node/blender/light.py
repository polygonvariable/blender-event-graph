import bpy
from bpy.props import ( BoolProperty, FloatProperty, EnumProperty, StringProperty, IntProperty, PointerProperty, CollectionProperty, FloatVectorProperty )

from ...base.node import EG_Node
from ...base.library import get_linked_cache, remove_linked_cache, add_linked_cache

from ...socket.primitive import EGS_Value


class EGN_CreateLight(EG_Node):
    """Creates a Light and returns its data and object Ids"""
    
    bl_idname = "egn.light.create"
    bl_label = "Create Light"
    bl_icon = "LIGHT"
    bl_width_default = 200

    enable_shadow: BoolProperty(name="Enable Shadow", default=True) # type: ignore
    light_type: EnumProperty(
        name="Type", 
        items=[("POINT", "Point", ""), ("SPOT", "Spot", ""), ("AREA", "Area", ""), ("SUN", "Sun", "")],
        default="POINT"
    ) # type: ignore
    

    def init(self, context):
        self.add_exec_in("exec")
        self.add_in("NodeSocketString", "name", 1, False)
        self.add_in("NodeSocketFloat", "intensity", 1, False)
        self.add_in("NodeSocketColor", "color", 1, False)
        self.add_in("NodeSocketVector", "location", 1, False)

        self.add_exec_out("exec")
        self.add_out("NodeSocketString", "data Id") # bind: dataId -> on_data_Id
        self.add_out("NodeSocketString", "object Id") # bind: objectId -> on_object_Id

        self.inputs["name"].default_value = "Light"
        self.inputs["intensity"].default_value = 1.0
        self.inputs["color"].default_value = (1.0, 1.0, 1.0, 1.0)
        self.inputs["location"].default_value = (0.0, 0.0, 0.0)


    def draw_buttons(self, context, layout):
        super().draw_buttons(context, layout)
        layout.prop(self, "enable_shadow")
        layout.prop(self, "light_type")


    def on_data_Id(self):
        return str(self.get_input_value("name"))


    def on_object_Id(self):
        return str(self.get_input_value("name"))


    def execute(self):

        try:

            in_name = str(self.get_input_value("name"))
            if not in_name:
                in_name = "Light"

            in_type = self.light_type
            in_color = self.get_input_value("color")
            in_location = self.get_input_value("location")
            in_intensity = float(self.get_input_value("intensity"))

            light_data = bpy.data.lights.get(in_name)
            if not light_data:
                light_data = bpy.data.lights.new(in_name, in_type)
                print("New light data created")
            else:
                print("Light data already exists")
            
            light_data.energy = in_intensity
            light_data.color = in_color[:3]
            light_data.use_shadow = self.enable_shadow

            light_object = bpy.data.objects.get(in_name)
            if not light_object:
                light_object = bpy.data.objects.new(in_name, light_data)
            
            if light_object.name not in bpy.context.scene.collection.objects:
                bpy.context.scene.collection.objects.link(light_object)
                light_object.location = in_location

            bpy.context.view_layer.update()

            self.execute_next("exec")

        except Exception as e:
            print(e)


class EGN_GetIntensity(EG_Node):
    """Get the intensity of a light"""
    
    bl_idname = "egn.light.get_intensity"
    bl_label = "Get Intensity"
    bl_icon = "LIGHT"

    def init(self, context):
        self.add_in("NodeSocketString", "data Id", 1, False)
        self.add_out("NodeSocketFloat", "intensity") # bind: intensity -> on_intensity

    def on_intensity(self):
        in_dataId = self.get_input_value("data Id")
        light_data = bpy.data.lights.get(in_dataId)

        if light_data:
            return light_data.energy
        
        return -1


class EGN_SetIntensity(EG_Node):
    """Set the intensity of a light"""
    
    bl_idname = "egn.light.set_intensity"
    bl_label = "Set Intensity"
    bl_icon = "LIGHT"

    def init(self, context):
        self.add_exec_in("exec")
        self.add_in("NodeSocketString", "data Id", 1, False)
        self.add_in("NodeSocketFloat", "intensity", 1, False)
        self.add_exec_out("exec")
        self.add_out("NodeSocketBool", "changed") # bind: changed -> on_changed

        self.inputs["intensity"].default_value = 1.0

    def on_changed(self):
        return get_linked_cache(self, "changed")

    def execute(self):
        in_dataId = self.get_input_value("data Id")
        in_intensity = self.get_input_value("intensity")
        out_changed = False

        light_data = bpy.data.lights.get(in_dataId)

        if light_data:
            light_data.energy = in_intensity
            out_changed = True

        add_linked_cache(self, "changed", out_changed)
        self.execute_next("exec")

    def free(self):
        remove_linked_cache(self, "changed")


class EGN_GetColor(EG_Node):
    """Get the color of a light"""
    
    bl_idname = "egn.light.get_color"
    bl_label = "Get Color"
    bl_icon = "LIGHT"

    def init(self, context):
        self.add_in("NodeSocketString", "data Id", 1, False)
        self.add_out("NodeSocketColor", "color") # bind: color -> on_color

    def on_color(self):
        in_dataId = self.get_input_value("data Id")
        light_data = bpy.data.lights.get(in_dataId)

        if light_data:
            return light_data.color
        
        return (0.0, 0.0, 0.0)


class EGN_SetColor(EG_Node):
    """Set the color of a light"""
    
    bl_idname = "egn.light.set_color"
    bl_label = "Set Color"
    bl_icon = "LIGHT"

    def init(self, context):
        self.add_exec_in("exec")
        self.add_in("NodeSocketString", "data Id", 1, False)
        self.add_in("NodeSocketColor", "color", 1, False)
        self.add_exec_out("exec")
        self.add_out("NodeSocketBool", "changed") # bind: changed -> on_changed

    def on_changed(self):
        return get_linked_cache(self, "changed")

    def execute(self):
        in_dataId = self.get_input_value("data Id")
        in_color = self.get_input_value("color")
        out_changed = False

        light_data = bpy.data.lights.get(in_dataId)

        if light_data:
            light_data.color = in_color[:3]
            out_changed = True

        add_linked_cache(self, "changed", out_changed)
        self.execute_next("exec")

    def free(self):
        remove_linked_cache(self, "changed")

classes = [
    EGN_CreateLight,
    EGN_GetIntensity,
    EGN_SetIntensity,
    EGN_GetColor,
    EGN_SetColor
]