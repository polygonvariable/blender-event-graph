from nodeitems_utils import NodeCategory, NodeItem, register_node_categories, unregister_node_categories

from .base import tree
from .node import base as n_base
from .node import cast as n_cast
from .node import literal as n_literal
from .node import string as n_string
from .node import light as n_light
from .node import operator as n_operator
from .node import iterator as n_iterator
from .node import array as n_array


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
    node_categories = [
        EG_Category("EGC_ARRAY", "Array", items=create_categories(n_array.classes)),
        EG_Category("EGC_BASE", "Base", items=create_categories(n_base.classes)),
        EG_Category("EGC_CAST", "Cast", items=create_categories(n_cast.classes)),
        EG_Category("EGC_ITERATOR", "Iterator", items=create_categories(n_iterator.classes)),
        EG_Category("EGC_LITERAL", "Literal", items=create_categories(n_literal.classes)),
        EG_Category("EGC_LIGHT", "Light", items=create_categories(n_light.classes)),
        EG_Category("EGC_OPERATOR", "Operator", items=create_categories(n_operator.classes)),
        EG_Category("EGC_STRING", "String", items=create_categories(n_string.classes)),
    ]
    register_node_categories("EG_NODES", node_categories)


def unregister():
    unregister_node_categories("EG_NODES")