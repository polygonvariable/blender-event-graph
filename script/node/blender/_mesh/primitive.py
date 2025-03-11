import bpy
from bpy.ops import mesh
from bpy.props import ( BoolProperty, FloatProperty, EnumProperty, StringProperty, IntProperty, PointerProperty, CollectionProperty, FloatVectorProperty )

from ....base.node import EG_Node
from ....base.library import get_linked_cache, remove_linked_cache, add_linked_cache

from ....socket.derived import EGS_Array
from ....socket.primitive import EGS_Value


class EGN_CreateMeshBase(EG_Node):
    """Creates a primitive mesh and returns the object Id"""
    
    bl_icon = "MESH_DATA"
    bl_width_default = 200

    mesh_align: EnumProperty(
        name="Align", 
        items=[("VIEW", "View", ""), ("WORLD", "World", ""), ("CURSOR", "Cursor", "")],
        default="WORLD"
    ) # type: ignore

    def add_custom_sockets(self):
        pass
    
    def init(self, context):
        self.add_exec_in("exec")
        self.add_in(socket="NodeSocketVector", name="location", hide_value=False)
        self.add_in(socket="NodeSocketVector", name="rotation", hide_value=False)
        self.add_in(socket="NodeSocketVector", name="scale", hide_value=False, default=(1.0, 1.0, 1.0))
        self.add_custom_sockets()

        self.add_exec_out("exec")
        self.add_out("NodeSocketString", "data Id") # bind: dataId -> on_data_Id
        self.add_out("NodeSocketString", "object Id") # bind: objectId -> on_object_Id

    def draw_buttons(self, context, layout):
        layout.prop(self, "mesh_align")

    def on_data_Id(self):
        return get_linked_cache(self, "data Id")
    
    def on_object_Id(self):
        return get_linked_cache(self, "object Id")

    def execute(self):
        bpy.context.view_layer.update()
        bpy.ops.ed.undo_push()

        out_dataId = bpy.context.object.data.name
        out_objectId = bpy.context.object.name

        add_linked_cache(self, "data Id", out_dataId)
        add_linked_cache(self, "object Id", out_objectId)

        self.execute_next("exec")

    def free(self):
        remove_linked_cache(self, "data Id")
        remove_linked_cache(self, "object Id")


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
        in_mesh_align = self.mesh_align

        mesh.primitive_cube_add(
            size=in_size,
            location=in_location,
            rotation=in_rotation,
            scale=in_scale,
            align=in_mesh_align,
        )
        super().execute()

    def free(self):
        remove_linked_cache(self, "data Id")
        remove_linked_cache(self, "object Id")


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
        in_mesh_align = self.mesh_align

        mesh.primitive_uv_sphere_add(
            location=in_location,
            rotation=in_rotation,
            scale=in_scale,
            align=in_mesh_align,
            radius=in_radius,
            segments=in_segments
        )
        super().execute()

    def free(self):
        remove_linked_cache(self, "data Id")
        remove_linked_cache(self, "object Id")


classes = [
    EGN_CreateCube,
    EGN_CreateSphere,
]