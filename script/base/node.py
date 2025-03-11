import uuid
import bpy
from bpy.props import ( StringProperty )
from enum import Enum

from ..socket.derived import EGS_Execute, EGS_Callback


class EG_NodeType(Enum):
    PURE = 0
    IMPURE = 1


class EG_PureNode(bpy.types.Node):
    """Pure node doesnt have execute socket"""

    bl_idname = "eg_purenode"
    bl_label = "Pure Node"
    bl_icon = "MOD_PHYSICS"
    bl_width_default = 180
    
    node_type = EG_NodeType.PURE

    def add_in(self, socket, name = "in", limit = 1, hide_value=True, default=None):
        pin = self.inputs.new(socket, name)
        pin.link_limit = limit
        pin.hide_value = hide_value
        if default is not None:
            pin.default_value = default

    def rem_in(self, name):
        self.inputs.remove(self.inputs[name])

    def rem_out(self, name):
        self.outputs.remove(self.outputs[name])

    def add_out(self, socket, name = "out", limit = 100):
        pin = self.outputs.new(socket, name)
        pin.link_limit = limit

    def get_input_value(self, name):
        
        # Get socket and check if its valid
        # else return None
        input_socket = self.inputs.get(name)
        if input_socket:

            # Check if socket is linked and get its value
            # else get default value
            if input_socket.is_linked and input_socket.links[0]:

                # Get source node and its name
                # and create binding method name
                source_node = input_socket.links[0].from_node
                source_method = f"on_{input_socket.links[0].from_socket.name.replace(' ', '_')}"

                # If source node have its binding method then
                # return its value
                if hasattr(source_node, source_method):

                    method = getattr(source_node, source_method)
                    if callable(method):

                        return method()
                
            else:
                return input_socket.default_value
            
        return None

    def get_input_values(self, name):
        
        values = []
        
        # Get socket and check if its valid
        # and return list
        input_socket = self.inputs.get(name)
        if input_socket:
            
            # If socket is linked then get its values
            # else return default value in list
            if input_socket.is_linked:
                
                # Iterate through all socket links and
                # get source node and its value
                links = input_socket.links
                for link in links:

                    # Get source node and its name
                    # and create binding method name
                    source_node = link.from_node
                    source_method = f"on_{link.from_socket.name.replace(' ', '_')}"

                    # If source node have its binding method then
                    # return its value
                    if hasattr(source_node, source_method):

                        method = getattr(source_node, source_method)
                        if callable(method):

                            values.append(method())

            else:
                return values.append(input_socket.default_value)

        return values
    

class EG_Node(EG_PureNode):
    """Event Node"""

    bl_idname = "eg_node"
    bl_label = "Impure Node"
    bl_icon = "SYSTEM"

    node_type = EG_NodeType.IMPURE
    node_uuid: StringProperty(name="UUID", default=str(uuid.uuid4()), options={"HIDDEN"}) # type: ignore

    def raid(self):
        self.node_uuid = str(uuid.uuid4())

    def init(self, context):
        self.raid()

    def draw_buttons(self, context, layout):
        layout.prop(self, "node_uuid")

    def add_exec_in(self, name = "in", is_callback = False):
        if not is_callback:
            self.add_in(EGS_Execute.bl_idname, name, 100, True)
        else:
            self.add_in(EGS_Callback.bl_idname, name, 1, True)

    def add_exec_out(self, name = "out", is_callback = False):
        if not is_callback:
            self.add_out(EGS_Execute.bl_idname, name, 1)
        else:
            self.add_out(EGS_Callback.bl_idname, name, 100)

    def execute_next(self, name):

        # Get output socket and check if its valid
        # and linked
        output_socket = self.outputs.get(name)
        if output_socket and output_socket.is_linked:

            # Get first linked node and check if it
            # have execute method and call it
            target_node = output_socket.links[0].to_node
            if hasattr(target_node, "__execute__"):

                target_node.__execute__()
    
    def execute_previous(self, name):

        # Get input socket and check if its valid
        # and linked
        input_socket = self.inputs.get(name)
        if input_socket and input_socket.is_linked:

            # Get first linked node and check if it
            # have execute method and call it
            source_node = input_socket.links[0].from_node
            if hasattr(source_node, "__execute__"):

                source_node.__execute__()

    def __execute__(self):

        try:

            if self.before_execute():
                self.execute()
            else:
                print("Node execution failed or terminated")

        except Exception as e:
            print(e)

    def before_execute(self):

        # Generate unique node uuid when its about to be executed
        # to prevent sharing of data between similar nodes
        self.raid()

        return True

    def execute(self):
        return ""
    