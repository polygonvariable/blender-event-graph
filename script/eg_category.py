from nodeitems_utils import NodeCategory, NodeItem, register_node_categories, unregister_node_categories

from .base import tree
from .node.python import base as n_base
from .node.python import cast as n_cast
from .node.python import literal as n_literal
from .node.python import string as n_string
from .node.python import operator as n_operator
from .node.python import flow as n_flow
from .node.python import array as n_array
from .node.python import set as n_set
from .node.python import map as n_map
from .node.python import utility as n_utility
from .node.python import cache as n_cache

from .node.blender import object as n_object
from .node.blender import mesh as n_mesh
from .node.blender import light as n_light


class EG_Category(NodeCategory):
    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == tree.EG_NodeTree.bl_idname


def create_categories(classes):
    categories = []
    categories_sorted = sorted(classes, key=lambda cls: cls.bl_label)

    for cls in categories_sorted:
        categories.append(NodeItem(cls.bl_idname))

    return categories


def register():
    python_categories = [
        
        EG_Category("egc_py_array", "Array", items=create_categories(n_array.classes)),
        EG_Category("egc_py_base", "Base", items=create_categories(n_base.classes)),
        EG_Category("egc_py_cache", "Cache", items=create_categories(n_cache.classes)),
        EG_Category("egc_py_cast", "Cast", items=create_categories(n_cast.classes)),
        EG_Category("egc_py_flow", "Flow", items=create_categories(n_flow.classes)),
        EG_Category("egc_py_literal", "Literal", items=create_categories(n_literal.classes)),
        EG_Category("egc_py_map", "Map", items=create_categories(n_map.classes)),
        EG_Category("egc_py_operator", "Operator", items=create_categories(n_operator.classes)),
        EG_Category("egc_py_set", "Set", items=create_categories(n_set.classes)),
        EG_Category("egc_py_string", "String", items=create_categories(n_string.classes)),
        EG_Category("egc_py_utility", "Utility", items=create_categories(n_utility.classes)),
        
    ]
    blender_categories = [
        
        EG_Category("egc_npy_light", "* Light", items=create_categories(n_light.classes)),
        EG_Category("egc_npy_object", "* Object", items=create_categories(n_object.classes)),
        EG_Category("egc_npy_mesh", "* Mesh", items=create_categories(n_mesh.classes)),
        
    ]
    register_node_categories("egc_py", python_categories)
    register_node_categories("egc_bpy", blender_categories)


def unregister():
    unregister_node_categories("egc_py")
    unregister_node_categories("egc_bpy")
