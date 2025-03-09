import uuid
import bpy
from bpy.props import ( BoolProperty, FloatProperty, EnumProperty, StringProperty, IntProperty, PointerProperty, CollectionProperty, FloatVectorProperty )

from ...base.node import EG_PureNode, EG_Node
from ...base.library import create_enum, add_variable, get_variable

from ...socket.derived import EGS_Set
from ...socket.primitive import EGS_Value



class EGN_MakeSet(EG_PureNode):
    """Make a new set"""
    
    bl_idname = "EGN_MakeSet"
    bl_label = "Make Set"

    def init(self, context):
        self.add_in(EGS_Value.bl_idname, "item", 100)
        self.add_out(EGS_Set.bl_idname, "set") # bind: set -> on_set

    def on_set(self):
        items = self.get_input_values("item")
        return set(items)


class EGN_SetAdd(EG_PureNode):
    """Add an item to a set"""
    
    bl_idname = "EGN_SetAdd"
    bl_label = "Add"
    
    def init(self, context):
        self.add_in(EGS_Set.bl_idname, "set")
        self.add_in(EGS_Value.bl_idname, "item")
        self.add_out(EGS_Set.bl_idname, "set") # bind: set -> on_set

    def on_set(self):
        item = self.get_input_value("item")
        items = self.get_input_value("set")
        items.add(item)
        return items


class EGN_SetClear(EG_PureNode):
    """Clear a set"""
    
    bl_idname = "EGN_SetClear"
    bl_label = "Clear"
    
    def init(self, context):
        self.add_in(EGS_Set.bl_idname, "set")
        self.add_out(EGS_Set.bl_idname, "set") # bind: set -> on_set

    def on_set(self):
        items = self.get_input_value("set")
        items.clear()
        return items


class EGN_SetDifference(EG_PureNode):
    """Difference between two sets"""
    
    bl_idname = "EGN_SetDifference"
    bl_label = "Difference"
    
    def init(self, context):
        self.add_in(EGS_Set.bl_idname, "a")
        self.add_in(EGS_Set.bl_idname, "b")
        self.add_out(EGS_Set.bl_idname, "set") # bind: set -> on_set

    def on_set(self):
        set_a = self.get_input_value("a")
        set_b = self.get_input_value("b")
        return set_a.difference(set_b)


class EGN_SetDiscard(EG_PureNode):
    """Remove an item from a set"""
    
    bl_idname = "EGN_SetDiscard"
    bl_label = "Discard"
    
    def init(self, context):
        self.add_in(EGS_Set.bl_idname, "set")
        self.add_in(EGS_Value.bl_idname, "item")
        self.add_out(EGS_Set.bl_idname, "set") # bind: set -> on_set

    def on_set(self):
        item = self.get_input_value("item")
        items = self.get_input_value("set")
        items.discard(item)
        return items


class EGN_SetIntersection(EG_PureNode):
    """Intersection between two sets"""
    
    bl_idname = "EGN_SetIntersection"
    bl_label = "Intersection"
    
    def init(self, context):
        self.add_in(EGS_Set.bl_idname, "a")
        self.add_in(EGS_Set.bl_idname, "b")
        self.add_out(EGS_Set.bl_idname, "set") # bind: set -> on_set

    def on_set(self):
        set_a = self.get_input_value("a")
        set_b = self.get_input_value("b")
        return set_a.intersection(set_b)


class EGN_SetIsDisjoint(EG_PureNode):
    """Check if two sets are disjoint"""
    
    bl_idname = "EGN_SetIsDisjoint"
    bl_label = "Is Disjoint"
    
    def init(self, context):
        self.add_in(EGS_Set.bl_idname, "a")
        self.add_in(EGS_Set.bl_idname, "b")
        self.add_out("NodeSocketBool", "result") # bind: result -> on_result

    def on_result(self):
        set_a = self.get_input_value("a")
        set_b = self.get_input_value("b")
        return set_a.isdisjoint(set_b)


class EGN_SetIsSubset(EG_PureNode):
    """Check if a set is a subset of another set"""
    
    bl_idname = "EGN_SetIsSubset"
    bl_label = "Is Subset"
    
    def init(self, context):
        self.add_in(EGS_Set.bl_idname, "a")
        self.add_in(EGS_Set.bl_idname, "b")
        self.add_out("NodeSocketBool", "result") # bind: result -> on_result

    def on_result(self):
        set_a = self.get_input_value("a")
        set_b = self.get_input_value("b")
        return set_a.issubset(set_b)


class EGN_SetIsSuperSet(EG_PureNode):
    """Check if a set is a superset of another set"""
    
    bl_idname = "EGN_SetIsSuperSet"
    bl_label = "Is Superset"
    
    def init(self, context):
        self.add_in(EGS_Set.bl_idname, "a")
        self.add_in(EGS_Set.bl_idname, "b")
        self.add_out("NodeSocketBool", "result") # bind: result -> on_result

    def on_result(self):
        set_a = self.get_input_value("a")
        set_b = self.get_input_value("b")
        return set_a.issuperset(set_b)


class EGN_SetPop(EG_PureNode):
    """Remove last item from a set"""
    
    bl_idname = "EGN_SetPop"
    bl_label = "Pop"
    
    def init(self, context):
        self.add_in(EGS_Set.bl_idname, "set")
        self.add_out(EGS_Set.bl_idname, "set") # bind: set -> on_set

    def on_set(self):
        items = self.get_input_value("set")
        items.pop()
        return items


class EGN_SetSymmetricDifference(EG_PureNode):
    """Get the symmetric difference between two sets"""
    
    bl_idname = "EGN_SetSymmetricDifference"
    bl_label = "Symmetric Difference"
    
    def init(self, context):
        self.add_in(EGS_Set.bl_idname, "a")
        self.add_in(EGS_Set.bl_idname, "b")
        self.add_out(EGS_Set.bl_idname, "set") # bind: set -> on_set

    def on_set(self):
        set_a = self.get_input_value("a")
        set_b = self.get_input_value("b")
        return set_a.symmetric_difference(set_b)


class EGN_SetUnion(EG_PureNode):
    """Union between two sets"""
    
    bl_idname = "EGN_SetUnion"
    bl_label = "Union"
    
    def init(self, context):
        self.add_in(EGS_Set.bl_idname, "a")
        self.add_in(EGS_Set.bl_idname, "b")
        self.add_out(EGS_Set.bl_idname, "set") # bind: set -> on_set

    def on_set(self):
        set_a = self.get_input_value("a")
        set_b = self.get_input_value("b")
        return set_a.union(set_b)


class EGN_SetLength(EG_PureNode):
    """Get the length of a set"""
    
    bl_idname = "EGN_SetLength"
    bl_label = "Length"
    
    def init(self, context):
        self.add_in(EGS_Set.bl_idname, "set")
        self.add_out("NodeSocketInt", "length") # bind: length -> on_length

    def on_length(self):
        items = self.get_input_value("set")
        return len(items)


classes = [
    EGN_MakeSet,
    EGN_SetAdd,
    EGN_SetClear,
    EGN_SetDifference,
    EGN_SetDiscard,
    EGN_SetIntersection,
    EGN_SetIsDisjoint,
    EGN_SetIsSubset,
    EGN_SetIsSuperSet,
    EGN_SetPop,
    EGN_SetSymmetricDifference,
    EGN_SetUnion,
    EGN_SetLength
]