import bpy

from .node import base as n_base
from .node import cast as n_cast
from .node import literal as n_literal
from .node import string as n_string
from .node import light as n_light
from .node import operator as n_operator
from .node import iterator as n_iterator
from .node import array as n_array


classes = []
classes += n_base.classes
classes += n_cast.classes
classes += n_literal.classes
classes += n_string.classes
classes += n_light.classes
classes += n_operator.classes
classes += n_iterator.classes
classes += n_array.classes


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)