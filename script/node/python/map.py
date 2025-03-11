import uuid
import bpy
from bpy.props import ( BoolProperty, FloatProperty, EnumProperty, StringProperty, IntProperty, PointerProperty, CollectionProperty, FloatVectorProperty )

from ...base.node import EG_PureNode
from ...socket.derived import EGS_Map, EGS_Array
from ...socket.primitive import EGS_Value


class EGN_MakeMap(EG_PureNode):
    """Make a new map"""
    
    bl_idname = "egn.python.make_map"
    bl_label = "Make Map"
    bl_icon = "PRESET"

    def init(self, context):
        self.add_in("NodeSocketString", "key", 1, False)
        self.add_in(EGS_Value.bl_idname, "value")
        self.add_out(EGS_Map.bl_idname, "map") # bind: map -> on_map

    def on_map(self):
        key = self.get_input_value("key")
        value = self.get_input_value("value")
        return {key: value}


class EGN_MapMerge(EG_PureNode):
    """Merge multiple maps into one"""
    
    bl_idname = "egn.python.map_merge"
    bl_label = "Merge"
    bl_icon = "PRESET"

    def init(self, context):
        self.add_in(EGS_Map.bl_idname, "maps", 100)
        self.add_out(EGS_Map.bl_idname, "map") # bind: map -> on_map

    def on_map(self):
        maps = self.get_input_values("maps")
        merged_map = {}

        for item in maps:
            merged_map.update(item)

        return merged_map


class EGN_MapClear(EG_PureNode):
    """Clear a map"""
    
    bl_idname = "egn.python.map_clear"
    bl_label = "Clear"
    bl_icon = "PRESET"

    def init(self, context):
        self.add_in(EGS_Map.bl_idname, "map")
        self.add_out(EGS_Map.bl_idname, "map") # bind: map -> on_map

    def on_map(self):
        in_map = self.get_input_value("map")
        in_map.clear()
        return in_map


class EGN_MapGet(EG_PureNode):
    """Get value from a map by key"""
    
    bl_idname = "egn.python.map_get"
    bl_label = "Get"
    bl_icon = "PRESET"

    def init(self, context):
        self.add_in(EGS_Map.bl_idname, "map")
        self.add_in("NodeSocketString", "key", 1, False)
        self.add_out(EGS_Value.bl_idname, "value") # bind: value -> on_value

    def on_value(self):
        in_map = self.get_input_value("map")
        in_key = self.get_input_value("key")
        return in_map.get(in_key)


class EGN_MapSet(EG_PureNode):
    """Set or update value in a map by key"""
    
    bl_idname = "egn.python.map_set"
    bl_label = "Set"
    bl_icon = "PRESET"

    def init(self, context):
        self.add_in(EGS_Map.bl_idname, "map")
        self.add_in("NodeSocketString", "key", 1, False)
        self.add_in(EGS_Value.bl_idname, "value")
        self.add_out(EGS_Map.bl_idname, "map") # bind: map -> on_map

    def on_map(self):
        in_map = self.get_input_value("map")
        in_key = self.get_input_value("key")
        in_value = self.get_input_value("value")

        in_map[in_key] = in_value
        return in_map


class EGN_MapKeys(EG_PureNode):
    """Get an array of map keys"""
    
    bl_idname = "egn.python.map_keys"
    bl_label = "Keys"
    bl_icon = "PRESET"

    def init(self, context):
        self.add_in(EGS_Map.bl_idname, "map")
        self.add_out(EGS_Array.bl_idname, "keys") # bind: keys -> on_keys

    def on_keys(self):
        in_map = self.get_input_value("map")
        return list(in_map.keys())


class EGN_MapValues(EG_PureNode):
    """Get an array of map values"""
    
    bl_idname = "egn.python.map_values"
    bl_label = "Values"
    bl_icon = "PRESET"

    def init(self, context):
        self.add_in(EGS_Map.bl_idname, "map")
        self.add_out(EGS_Array.bl_idname, "values") # bind: values -> on_values

    def on_values(self):
        in_map = self.get_input_value("map")
        return list(in_map.values())


class EGN_MapItems(EG_PureNode):
    """Get an array of map items"""
    
    bl_idname = "egn.python.map_items"
    bl_label = "Items"
    bl_icon = "PRESET"

    def init(self, context):
        self.add_in(EGS_Map.bl_idname, "map")
        self.add_out(EGS_Array.bl_idname, "items") # bind: items -> on_items

    def on_items(self):
        in_map = self.get_input_value("map")
        return list(in_map.items())


class EGN_MapPop(EG_PureNode):
    """Remove value from a map by key"""
    
    bl_idname = "egn.python.map_pop"
    bl_label = "Pop"
    bl_icon = "PRESET"

    def init(self, context):
        self.add_in(EGS_Map.bl_idname, "map")
        self.add_in("NodeSocketString", "key", 1, False)
        self.add_out(EGS_Map.bl_idname, "map") # bind: map -> on_map

    def on_map(self):
        in_map = self.get_input_value("map")
        in_key = self.get_input_value("key")
        in_map.pop(in_key)
        return in_map


classes = [
    EGN_MakeMap,
    EGN_MapMerge,
    EGN_MapClear,
    EGN_MapGet,
    EGN_MapSet,
    EGN_MapKeys,
    EGN_MapItems,
    EGN_MapValues,
    EGN_MapPop
]