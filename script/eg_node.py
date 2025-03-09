import bpy

from .node.python import base as n_base
from .node.python import cast as n_cast
from .node.python import literal as n_literal
from .node.python import string as n_string
from .node.python import operator as n_operator
from .node.python import iterator as n_iterator
from .node.python import array as n_array
from .node.python import set as n_set
from .node.python import map as n_map
from .node.python import debug as n_debug

from .node.blender import object as n_object
from .node.blender import light as n_light


classes = []
classes += n_base.classes
classes += n_cast.classes
classes += n_literal.classes
classes += n_string.classes
classes += n_operator.classes
classes += n_iterator.classes
classes += n_array.classes
classes += n_set.classes
classes += n_map.classes
classes += n_debug.classes

classes += n_object.classes
classes += n_light.classes


def register():
    count = 0
    for cls in classes:
        bpy.utils.register_class(cls)
        count += 1
    print("{} nodes registered".format(count))

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)