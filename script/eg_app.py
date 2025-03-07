from .eg_tree import register as register_tree, unregister as unregister_tree
from .eg_node import register as register_node, unregister as unregister_node
from .eg_operator import register as register_operator, unregister as unregister_operator
from .eg_category import register as register_category, unregister as unregister_category
from .eg_preference import register as register_preference, unregister as unregister_preference
from .eg_socket import register as register_socket, unregister as unregister_socket

def register():
    register_tree()
    register_socket()
    register_node()
    register_operator()
    register_category()
    register_preference()

def unregister():
    unregister_tree()
    unregister_socket()
    unregister_node()
    unregister_operator()
    unregister_category()
    unregister_preference()