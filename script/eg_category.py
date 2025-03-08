from nodeitems_utils import NodeCategory, NodeItem, register_node_categories, unregister_node_categories

from .base import tree
from .node import base, cast, literal, string as n_string, light


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
        EG_Category("EGC_BASE", "Base", items=create_categories(base.classes)),
        EG_Category("EGC_CAST", "Cast", items=create_categories(cast.classes)),
        EG_Category("EGC_LITERAL", "Literal", items=create_categories(literal.classes)),
        EG_Category("EGC_STRING", "String", items=create_categories(n_string.classes)),
        EG_Category("EGC_LIGHT", "Light", items=create_categories(light.classes)),
    ]
    register_node_categories("EG_NODES", node_categories)


def unregister():
    unregister_node_categories("EG_NODES")