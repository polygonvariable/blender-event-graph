import uuid
import bpy
from bpy.props import ( StringProperty )
from ..socket.derived import EGS_Execute

class EG_Node(bpy.types.Node):
    """Event Node"""

    bl_idname = "EG_Node"
    bl_label = "Event Node"
    bl_icon = "SYSTEM"
    bl_width_default = 180


    node_uuid: StringProperty(name="Node UUID", default=str(uuid.uuid4())) # type: ignore
    node_is_pure = False


    def add_in(self, socket_type, name = "in", limit = 1, hide_value=True):
        pin = self.inputs.new(socket_type, name)
        pin.link_limit = limit
        pin.hide_value = hide_value


    def add_out(self, socket_type, name = "out", limit = 100):
        pin = self.outputs.new(socket_type, name)
        pin.link_limit = limit


    def add_exec_in(self, name = "in", hide_value=True):
        self.add_in(EGS_Execute.bl_idname, name, 100, hide_value)


    def add_exec_out(self, name = "out"):
        self.add_out(EGS_Execute.bl_idname, name, 1)


    def init(self, context):
        self.default_in()
        self.default_out()


    def validate_sockets(self, node_tree, sockets):
        for socket in sockets:
            if socket.is_linked:
                for link in list(socket.links):
                    if link.from_socket.bl_idname != link.to_socket.bl_idname:
                        node_tree.links.remove(link)


    def validate_links(self):

        node_tree = self.id_data

        self.validate_sockets(node_tree, self.inputs)
        self.validate_sockets(node_tree, self.outputs)


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

