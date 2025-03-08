import bpy
from bpy.props import ( BoolProperty, FloatProperty, EnumProperty, StringProperty, IntProperty, PointerProperty, CollectionProperty, FloatVectorProperty )

from ..base.node import EG_Node
from ..base.library import create_enum

from ..socket.user import EGS_Object, EGS_Reference
from ..socket.primitive import EGS_Value


class EGN_CreateLight(EG_Node):
    """Creates a Light"""
    
    bl_idname = "EGN_CreateLight"
    bl_label = "Create Light"
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

            light_name = str(self.get_input_value("name"))
            if not light_name:
                light_name = "Light"

            light_type = self.light_type
            light_color = self.get_input_value("color")
            light_location = self.get_input_value("location")
            light_intensity = float(self.get_input_value("intensity"))

            light_data = bpy.data.lights.get(light_name)
            if not light_data:
                light_data = bpy.data.lights.new(light_name, light_type)
                print("New light data created")
            else:
                print("Light data already exists")
            
            light_data.energy = light_intensity
            light_data.color = (light_color[0], light_color[1], light_color[2])
            light_data.use_shadow = self.enable_shadow

            light_object = bpy.data.objects.get(light_name)
            if not light_object:
                light_object = bpy.data.objects.new(light_name, light_data)
            
            if light_object.name not in bpy.context.scene.collection.objects:
                bpy.context.scene.collection.objects.link(light_object)
                light_object.location = light_location

            bpy.context.view_layer.update()

            self.execute_next("exec")

        except Exception as e:
            print(e)

classes = [
    EGN_CreateLight
]