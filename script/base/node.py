import uuid
import bpy
from bpy.props import ( StringProperty )

class EG_Node(bpy.types.Node):
    """Event Node"""

    bl_idname = "EG_Node"
    bl_label = "Event Node"
    bl_icon = "FILE_SCRIPT"
    bl_width_default = 180


    node_uuid: StringProperty(name="Node UUID", default=str(uuid.uuid4())) # type: ignore
    node_is_pure = False


    def add_in(self, socket_type, name = "in", hide_value=True):
        pin = self.inputs.new(socket_type, name)
        pin.hide_value = hide_value


    def add_out(self, socket_type, name = "out"):
        self.outputs.new(socket_type, name)


    def add_exec_in(self, name = "in", hide_value=True):
        self.add_in("EGS_Execute", name, hide_value)


    def add_exec_out(self, name = "out"):
        self.add_out("EGS_Execute", name)


    def init(self, context):
        self.default_in()
        self.default_out()


    def execute_next(self, name):
        output_socket = self.outputs.get(name)
        if output_socket and output_socket.is_linked:
            target_node = output_socket.links[0].to_node
            if hasattr(target_node, "execute"):
                target_node.execute()
    

    def execute_previous(self, name):
        input_socket = self.inputs.get(name)
        if input_socket and input_socket.is_linked:
            source_node = input_socket.links[0].from_node
            if hasattr(source_node, "execute"):
                source_node.execute()


    def get_input_value(self, name):
        input_socket = self.inputs.get(name)

        if input_socket and input_socket.is_linked:

            source_node = input_socket.links[0].from_node
            source_method = f"on_{input_socket.links[0].from_socket.name.replace(' ', '_')}"

            if hasattr(source_node, source_method):

                if hasattr(source_node, "execute") and source_node.node_is_pure:
                    source_node.execute()
                    
                method = getattr(source_node, source_method)
                if callable(method):
                    return method()

        return None


    def get_input_values(self, name):

        values = []
        input_socket = self.inputs.get(name)

        if input_socket and input_socket.is_linked:
            
            links = input_socket.links
            for link in links:

                source_node = link.from_node
                source_method = f"on_{link.from_socket.name.replace(' ', '_')}"

                if hasattr(source_node, source_method):
                    method = getattr(source_node, source_method)

                    if callable(method):
                        values.append(method())

        return values
    

    def execute(self):
        return ""

