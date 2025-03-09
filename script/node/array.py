import uuid
import bpy
from bpy.props import ( BoolProperty, FloatProperty, EnumProperty, StringProperty, IntProperty, PointerProperty, CollectionProperty, FloatVectorProperty )

from ..base.node import EG_PureNode, EG_Node
from ..base.library import create_enum, add_variable, get_variable

from ..socket.derived import EGS_Array
from ..socket.primitive import EGS_Value



class EGN_MakeArray(EG_PureNode):
    """Make a new array"""
    
    bl_idname = "EGN_Array"
    bl_label = "Make Array"

    def init(self, context):
        self.add_in(EGS_Value.bl_idname, "item", 100)
        self.add_out(EGS_Array.bl_idname, "array")

    def on_array(self):
        return self.get_input_values("item")


class EGN_ArrayMerge(EG_PureNode):
    """Node to merge two arrays"""
    
    bl_idname = "EGN_ArrayMerge"
    bl_label = "Merge"
    
    def init(self, context):
        self.add_in(EGS_Array.bl_idname, "a")
        self.add_in(EGS_Array.bl_idname, "b")
        self.add_out(EGS_Array.bl_idname, "array") # bind: array -> on_array

    def on_array(self):
        list_a = self.get_input_value("a")
        list_b = self.get_input_value("b")
        return list_a + list_b
        

class EGN_ArrayAppend(EG_PureNode):
    """Node to append an item to an array"""
    
    bl_idname = "EGN_ArrayAppend"
    bl_label = "Append"
    
    def init(self, context):
        self.add_in(EGS_Array.bl_idname, "array")
        self.add_in(EGS_Value.bl_idname, "item")
        self.add_out(EGS_Array.bl_idname, "array")

    def on_array(self):
        item = self.get_input_value("item")
        items = self.get_input_value("array")
        items.append(item)
        return items


class EGN_ArrayClear(EG_PureNode):
    """Node to clear an array"""
    
    bl_idname = "EGN_ArrayClear"
    bl_label = "Clear"
    
    def init(self, context):
        self.add_in(EGS_Array.bl_idname, "array")
        self.add_out(EGS_Array.bl_idname, "array")

    def on_array(self):
        items = self.get_input_value("array")
        items.clear()
        return items


class EGN_ArrayCount(EG_PureNode):
    """Node count certain item in an array"""
    
    bl_idname = "EGN_ArrayCount"
    bl_label = "Count"
    
    def init(self, context):
        self.add_in(EGS_Array.bl_idname, "array")
        self.add_in(EGS_Value.bl_idname, "item")
        self.add_out("NodeSocketInt", "count") # bind: count -> on_count

    def on_count(self):
        item = self.get_input_value("item")
        items = self.get_input_value("array")
        return items.count(item)


class EGN_ArrayIndex(EG_PureNode):
    """Get index of an item in an array"""
    
    bl_idname = "EGN_ArrayIndex"
    bl_label = "Index"
    
    def init(self, context):
        self.add_in(EGS_Array.bl_idname, "array")
        self.add_in(EGS_Value.bl_idname, "item")
        self.add_out("NodeSocketInt", "index") # bind: index -> on_index

    def on_index(self):
        item = self.get_input_value("item")
        items = self.get_input_value("array")
        return items.index(item)


class EGN_ArrayInsert(EG_PureNode):
    """Insert an item in an array at a specific index"""
    
    bl_idname = "EGN_ArrayInsert"
    bl_label = "Insert"
    
    def init(self, context):
        self.add_in(EGS_Array.bl_idname, "array")
        self.add_in(EGS_Value.bl_idname, "item")
        self.add_in("NodeSocketInt", "index", 1, False)
        self.add_out(EGS_Array.bl_idname, "array") # bind: array -> on_array

    def on_array(self):
        item = self.get_input_value("item")
        items = self.get_input_value("array")
        index = int(self.get_input_value("index"))
        items.insert(index, item)
        return items


class EGN_ArrayPop(EG_PureNode):
    """Event Array Pop Node"""
    
    bl_idname = "EGN_ArrayPop"
    bl_label = "Pop"
    
    def init(self, context):
        self.add_in(EGS_Array.bl_idname, "array")
        self.add_out(EGS_Array.bl_idname, "array") # bind: array -> on_array

    def on_array(self):
        items = self.get_input_value("array")
        items.pop()
        return items


class EGN_ArrayRemove(EG_PureNode):
    """Remove an item from an array"""
    
    bl_idname = "EGN_ArrayRemove"
    bl_label = "Remove"
    
    def init(self, context):
        self.add_in(EGS_Array.bl_idname, "array")
        self.add_in(EGS_Value.bl_idname, "item")
        self.add_out(EGS_Array.bl_idname, "array") # bind: array -> on_array

    def on_array(self):
        item = self.get_input_value("item")
        items = self.get_input_value("array")
        items.remove(item)
        return items


class EGN_ArrayReverse(EG_PureNode):
    """Reverse an array"""
    
    bl_idname = "EGN_ArrayReverse"
    bl_label = "Reverse"
    
    def init(self, context):
        self.add_in(EGS_Array.bl_idname, "array")
        self.add_out(EGS_Array.bl_idname, "array") # bind: array -> on_array

    def on_array(self):
        items = self.get_input_value("array")
        items.reverse()
        return items


class EGN_ArraySort(EG_PureNode):
    """Sort an array"""
    
    bl_idname = "EGN_ArraySort"
    bl_label = "Sort"

    reverse = bpy.props.BoolProperty(name="Reverse", default=False)
    
    def init(self, context):
        self.add_in(EGS_Array.bl_idname, "array")
        self.add_out(EGS_Array.bl_idname, "array") # bind: array -> on_array

    def draw_buttons(self, context, layout):
        layout.prop(self, "reverse")

    def on_array(self):
        items = self.get_input_value("array")
        items.sort(reverse=self.reverse)
        return items


class EGN_ArrayGet(EG_PureNode):
    """Get an item from an array at a specific index"""
    
    bl_idname = "EGN_ArrayGet"
    bl_label = "Get"
    
    def init(self, context):
        self.add_in(EGS_Array.bl_idname, "array")
        self.add_in("NodeSocketInt", "index", 1, False)
        self.add_out(EGS_Value.bl_idname, "item") # bind: item -> on_item

    def on_item(self):
        items = self.get_input_value("array")
        index = int(self.get_input_value("index"))
        return items[index]


class EGN_ArraySet(EG_PureNode):
    """Update an item from an array at a specific index if it exists"""
    
    bl_idname = "EGN_ArraySet"
    bl_label = "Set"
    
    def init(self, context):
        self.add_in(EGS_Array.bl_idname, "array")
        self.add_in(EGS_Value.bl_idname, "item")
        self.add_in("NodeSocketInt", "index", 1, False)
        self.add_out(EGS_Array.bl_idname, "array") # bind: array -> on_array

    def on_array(self):
        item = self.get_input_value("item")
        items = self.get_input_value("array")
        index = int(self.get_input_value("index"))

        if index < len(items):
            items[index] = item
        
        return items


class EGN_ArrayLength(EG_PureNode):
    """Get the length of an array"""
    
    bl_idname = "EGN_ArrayLength"
    bl_label = "Length"
    
    def init(self, context):
        self.add_in(EGS_Array.bl_idname, "array")
        self.add_out("NodeSocketInt", "length") # bind: length -> on_length

    def on_length(self):
        items = self.get_input_value("array")
        return len(items)


classes = [
    EGN_MakeArray,
    EGN_ArrayMerge,
    EGN_ArrayAppend,
    EGN_ArrayClear,
    EGN_ArrayCount,
    EGN_ArrayIndex,
    EGN_ArrayInsert,
    EGN_ArrayPop,
    EGN_ArrayRemove,
    EGN_ArrayReverse,
    EGN_ArraySort,
    EGN_ArrayGet,
    EGN_ArraySet,
    EGN_ArrayLength
]