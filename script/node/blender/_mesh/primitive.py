import bpy
from bpy.ops import mesh
from bpy.props import ( BoolProperty, FloatProperty, EnumProperty, StringProperty, IntProperty, PointerProperty, CollectionProperty, FloatVectorProperty )

from ....base.node import EG_Node
from ....base.library import get_linked_cache, remove_linked_cache, add_linked_cache, is_vector

from ....socket.derived import EGS_Array
from ....socket.primitive import EGS_Value


class EGN_CreateMeshBase(EG_Node):
    """Creates a primitive mesh and returns the object Id"""
    
    bl_icon = "MESH_DATA"
    bl_width_default = 200

    prop_align: EnumProperty(
        name="Align", 
        items=[("VIEW", "View", ""), ("WORLD", "World", ""), ("CURSOR", "Cursor", "")],
        default="WORLD"
    ) # type: ignore
    prop_dataId: StringProperty(name="data Id") # type: ignore
    prop_objectId: StringProperty(name="object Id") # type: ignore

    def add_custom_sockets(self):
        pass
    
    def init(self, context):
        self.add_exec_in("exec")
        self.add_in(socket="NodeSocketVector", name="location", hide_value=False)
        self.add_in(socket="NodeSocketVectorEuler", name="rotation", hide_value=False)
        self.add_in(socket="NodeSocketVector", name="scale", hide_value=False, default=(1.0, 1.0, 1.0))
        self.add_custom_sockets()

        self.add_exec_out("exec")
        self.add_out("NodeSocketString", "data Id") # bind: dataId -> on_data_Id
        self.add_out("NodeSocketString", "object Id") # bind: objectId -> on_object_Id

    def draw_buttons(self, context, layout):
        layout.prop(self, "prop_align")

    def on_data_Id(self):
        return self.prop_dataId
    
    def on_object_Id(self):
        return self.prop_objectId

    def execute(self):
        bpy.context.view_layer.update()
        bpy.ops.ed.undo_push()

        self.prop_dataId = bpy.context.object.data.name
        self.prop_objectId = bpy.context.object.name
        self.execute_next("exec")


class EGN_CreateCube(EGN_CreateMeshBase):
    """Creates a primitive cube and returns its data and object Ids"""
    
    bl_idname = "egn.mesh.create_cube"
    bl_label = "Create Cube"
    bl_icon = "CUBE"

    def add_custom_sockets(self):
        self.add_in(socket="NodeSocketFloat", name="size", hide_value=False, default=1.0)

    def execute(self):
        in_location = self.get_input_value("location")
        in_rotation = self.get_input_value("rotation")
        in_scale = self.get_input_value("scale")
        in_size = float(self.get_input_value("size"))

        mesh.primitive_cube_add(
            size=in_size,
            location=in_location,
            rotation=in_rotation,
            scale=in_scale,
            align=self.prop_align,
        )
        super().execute()


class EGN_CreateSphere(EGN_CreateMeshBase):
    """Creates a primitive sphere and returns its data and object Ids"""
    
    bl_idname = "egn.mesh.create_sphere"
    bl_label = "Create Sphere"
    bl_icon = "SPHERE"

    def add_custom_sockets(self):
        self.add_in("NodeSocketFloat", "radius", hide_value=False, default=1.0)
        self.add_in("NodeSocketFloat", "segments", hide_value=False, default=32.0)

    def execute(self):
        in_location = self.get_input_value("location")
        in_rotation = self.get_input_value("rotation")
        in_scale = self.get_input_value("scale")
        in_radius = float(self.get_input_value("radius"))
        in_segments = int(self.get_input_value("segments"))

        mesh.primitive_uv_sphere_add(
            location=in_location,
            rotation=in_rotation,
            scale=in_scale,
            align=self.prop_align,
            radius=in_radius,
            segments=in_segments
        )
        super().execute()


classes = [
    EGN_CreateCube,
    EGN_CreateSphere,
]