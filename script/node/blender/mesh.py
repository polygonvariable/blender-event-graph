from ._mesh.active import classes as active_classes
from ._mesh.primitive import classes as primitive_classes
from ._mesh.operation import classes as operation_classes

classes = []
classes += active_classes
classes += primitive_classes
classes += operation_classes