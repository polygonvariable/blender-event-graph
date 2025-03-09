from nodeitems_utils import NodeCategory, NodeItem, register_node_categories, unregister_node_categories

from .base import tree
from .node.python import base as n_base
from .node.python import cast as n_cast
from .node.python import literal as n_literal
from .node.python import string as n_string
from .node.python import operator as n_operator
from .node.python import iterator as n_iterator
from .node.python import array as n_array
from .node.python import set as n_set
from .node.python import map as n_map

from .node.blender import object as n_object
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
        
        EG_Category("EGC_PY_ARRAY", "Array", items=create_categories(n_array.classes)),
        EG_Category("EGC_PY_BASE", "Base", items=create_categories(n_base.classes)),
        EG_Category("EGC_PY_CAST", "Cast", items=create_categories(n_cast.classes)),
        EG_Category("EGC_PY_ITERATOR", "Iterator", items=create_categories(n_iterator.classes)),
        EG_Category("EGC_PY_LITERAL", "Literal", items=create_categories(n_literal.classes)),
        EG_Category("EGC_PY_MAP", "Map", items=create_categories(n_map.classes)),
        EG_Category("EGC_PY_OPERATOR", "Operator", items=create_categories(n_operator.classes)),
        EG_Category("EGC_PY_SET", "Set", items=create_categories(n_set.classes)),
        EG_Category("EGC_PY_STRING", "String", items=create_categories(n_string.classes)),
        
    ]
    blender_categories = [
        
        EG_Category("EGC_BPY_LIGHT", "* Light", items=create_categories(n_light.classes)),
        EG_Category("EGC_BPY_OBJECT", "* Object", items=create_categories(n_object.classes)),
        
    ]
    register_node_categories("EG_PYTHON_CATEGORIES", python_categories)
    register_node_categories("EG_BLENDER_CATEGORIES", blender_categories)


def unregister():
    unregister_node_categories("EG_PYTHON_CATEGORIES")
    unregister_node_categories("EG_BLENDER_CATEGORIES")
