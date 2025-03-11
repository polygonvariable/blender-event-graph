from ._object.fetch import classes as fetch_classes
from ._object.modify import classes as modify_classes
from ._object.active import classes as active_classes
from ._object.visibility import classes as visibility_classes
from ._object.transform import classes as transform_classes

classes = []
classes += fetch_classes
classes += modify_classes
classes += active_classes
classes += visibility_classes
classes += transform_classes