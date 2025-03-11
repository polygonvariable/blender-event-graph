import bpy
from bpy.props import ( BoolProperty, FloatProperty, EnumProperty, StringProperty, IntProperty, PointerProperty, CollectionProperty )

from ...base.node import EG_Node, EG_PureNode
from ...base.library import create_enum

from ...socket.derived import EGS_Array
from ...socket.primitive import EGS_Value


class EGN_AppendString(EG_PureNode):
    """Node to append strings"""
    
    bl_idname = "egn.python.append_string"
    bl_label = "Append"

    def init(self, context):
        self.add_in("NodeSocketString", "a", 1, False)
        self.add_in("NodeSocketString", "b", 1, False)
        self.add_out("NodeSocketString", "result") # bind: result -> on_result

    def on_result(self):
        return str(self.get_input_value("a")) + str(self.get_input_value("b"))


class EGN_ContainString(EG_PureNode):
    """Node to check if a string contains another string"""
    
    bl_idname = "egn.python.contain_string"
    bl_label = "Contains"

    def init(self, context):
        self.add_in("NodeSocketString", "source", 1, False)
        self.add_in("NodeSocketString", "match", 1, False)
        self.add_out("NodeSocketBool", "result") # bind: result -> on_result

    def on_result(self):
        source = str(self.get_input_value("source"))
        match = str(self.get_input_value("match"))
        return match in source


class EGN_SliceString(EG_PureNode):
    """Node to slice a string"""
    
    bl_idname = "egn.python.slice_string"
    bl_label = "Slice"

    def init(self, context):
        self.add_in("NodeSocketString", "source", 1, False)
        self.add_in("NodeSocketInt", "start", 1, False)
        self.add_in("NodeSocketInt", "end", 1, False)
        self.add_out("NodeSocketString", "result") # bind: result -> on_result

    def on_result(self):
        source = str(self.get_input_value("source"))
        start = int(self.get_input_value("start"))
        end = int(self.get_input_value("end"))
        return source[start:end]


class EGN_SliceFromStartString(EG_PureNode):
    """Node to slice a string from start"""
    
    bl_idname = "egn.python.slice_from_start_string"
    bl_label = "Slice From Start"

    def init(self, context):
        self.add_in("NodeSocketString", "source", 1, False)
        self.add_in("NodeSocketInt", "start", 1, False)
        self.add_out("NodeSocketString", "result") # bind: result -> on_result

    def on_result(self):
        source = str(self.get_input_value("source"))
        start = int(self.get_input_value("start"))
        return source[:start]


class EGN_SliceFromEndString(EG_PureNode):
    """Node to slice a string from end"""
    
    bl_idname = "egn.python.slice_from_end_string"
    bl_label = "Slice From End"

    def init(self, context):
        self.add_in("NodeSocketString", "source", 1, False)
        self.add_in("NodeSocketInt", "end", 1, False)
        self.add_out("NodeSocketString", "result") # bind: result -> on_result

    def on_result(self):
        source = str(self.get_input_value("source"))
        end = int(self.get_input_value("end"))
        return source[end:]


class EGN_ToUpperString(EG_PureNode):
    """Node to convert a string to upper case"""
    
    bl_idname = "egn.python.to_upper_string"
    bl_label = "To Upper"

    def init(self, context):
        self.add_in("NodeSocketString", "source", 1, False)
        self.add_out("NodeSocketString", "result") # bind: result -> on_result

    def on_result(self):
        source = str(self.get_input_value("source"))
        return source.upper()


class EGN_ToLowerString(EG_PureNode):
    """Node to convert a string to lower case"""
    
    bl_idname = "egn.python.to_lower_string"
    bl_label = "To Lower"

    def init(self, context):
        self.add_in("NodeSocketString", "source", 1, False)
        self.add_out("NodeSocketString", "result") # bind: result -> on_result

    def on_result(self):
        source = str(self.get_input_value("source"))
        return source.lower()


class EGN_CapitalizeString(EG_PureNode):
    """Node to capitalize a string"""
    
    bl_idname = "egn.python.capitalize_string"
    bl_label = "Capitalize"

    def init(self, context):
        self.add_in("NodeSocketString", "source", 1, False)
        self.add_out("NodeSocketString", "result") # bind: result -> on_result

    def on_result(self):
        source = str(self.get_input_value("source"))
        return source.capitalize()


class EGN_CasefoldString(EG_PureNode):
    """Node to casefold a string"""
    
    bl_idname = "egn.python.casefold_string"
    bl_label = "Casefold"

    def init(self, context):
        self.add_in("NodeSocketString", "source", 1, False)
        self.add_out("NodeSocketString", "result") # bind: result -> on_result

    def on_result(self):
        source = str(self.get_input_value("source"))
        return source.casefold()


class EGN_CountString(EG_PureNode):
    """Node to count a string"""
    
    bl_idname = "egn.python.count_string"
    bl_label = "Count"

    def init(self, context):
        self.add_in("NodeSocketString", "source", 1, False)
        self.add_in("NodeSocketString", "match", 1, False)
        self.add_out("NodeSocketInt", "result") # bind: result -> on_result

    def on_result(self):
        source = str(self.get_input_value("source"))
        match = str(self.get_input_value("match"))
        return source.count(match)


class EGN_EndsWithString(EG_PureNode):
    """Node to check if a string ends with another string"""
    
    bl_idname = "egn.python.ends_with_string"
    bl_label = "Ends With"

    def init(self, context):
        self.add_in("NodeSocketString", "source", 1, False)
        self.add_in("NodeSocketString", "match", 1, False)
        self.add_out("NodeSocketBool", "result") # bind: result -> on_result

    def on_result(self):
        source = str(self.get_input_value("source"))
        match = str(self.get_input_value("match"))
        return source.endswith(match)


class EGN_FindString(EG_PureNode):
    """Node to get index of a string"""
    
    bl_idname = "egn.python.find_string"
    bl_label = "Find"

    def init(self, context):
        self.add_in("NodeSocketString", "source", 1, False)
        self.add_in("NodeSocketString", "match", 1, False)
        self.add_out("NodeSocketInt", "result") # bind: result -> on_result

    def on_result(self):
        source = str(self.get_input_value("source"))
        match = str(self.get_input_value("match"))
        return source.find(match)


class EGN_IndexString(EG_PureNode):
    """Node to get index of a string"""
    
    bl_idname = "egn.python.index_string"
    bl_label = "Index Of"

    def init(self, context):
        self.add_in("NodeSocketString", "source", 1, False)
        self.add_in("NodeSocketString", "match", 1, False)
        self.add_out("NodeSocketInt", "result") # bind: result -> on_result

    def on_result(self):
        source = str(self.get_input_value("source"))
        match = str(self.get_input_value("match"))
        return source.index(match)


class EGN_IsAString(EG_PureNode):
    """Node to check if a string is an instance of another string"""
    
    bl_idname = "egn.python.is_a_string"
    bl_label = "Is A"

    condition: EnumProperty(
        name="Operator",
        items=create_enum(["alnum", "alpha", "ascii", "decimal", "digit", "lower", "numeric", "space", "title", "upper"]),
        default="alnum"
    ) # type: ignore

    def init(self, context):
        self.add_in("NodeSocketString", "source", 1, False)
        self.add_out("NodeSocketBool", "result") # bind: result -> on_result

    def draw_buttons(self, context, layout):
        layout.prop(self, "condition")

    def on_result(self):
        source = str(self.get_input_value("source"))
        result = False

        if self.condition == "alnum":
            result = source.isalnum()
        elif self.condition == "alpha":
            result = source.isalpha()
        elif self.condition == "ascii":
            result = source.isascii()
        elif self.condition == "decimal":
            result = source.isdecimal()
        elif self.condition == "digit":
            result = source.isdigit()
        elif self.condition == "lower":
            result = source.islower()
        elif self.condition == "numeric":
            result = source.isnumeric()
        elif self.condition == "space":
            result = source.isspace()
        elif self.condition == "title":
            result = source.istitle()
        elif self.condition == "upper":
            result = source.isupper()

        return result


class EGN_StripString(EG_PureNode):
    """Node to remove spaces from a string"""
    
    bl_idname = "egn.python.strip_string"
    bl_label = "Strip"

    def init(self, context):
        self.add_in("NodeSocketString", "source", 1, False)
        self.add_out("NodeSocketString", "result") # bind: result -> on_result

    def on_result(self):
        source = str(self.get_input_value("source"))
        return source.strip()


class EGN_SplitString(EG_PureNode):
    """Node to split a string"""
    
    bl_idname = "egn.python.split_string"
    bl_label = "Split"

    def init(self, context):
        self.add_in("NodeSocketString", "source", 1, False)
        self.add_in("NodeSocketString", "separator", 1, False)
        self.add_out(EGS_Array.bl_idname, "array") # bind: array -> on_array

    def on_array(self):
        source = str(self.get_input_value("source"))
        separator = str(self.get_input_value("separator"))
        return source.split(separator)


class EGN_ReplaceString(EG_PureNode):
    """Node to replace strings"""
    
    bl_idname = "egn.python.replace_string"
    bl_label = "Replace"

    def init(self, context):
        self.add_in("NodeSocketString", "source", 1, False)
        self.add_in("NodeSocketString", "match", 1, False)
        self.add_in("NodeSocketString", "replace", 1, False)
        self.add_out("NodeSocketString", "result") # bind: result -> on_result

    def on_result(self):
        source = str(self.get_input_value("source"))
        match = str(self.get_input_value("match"))
        replace = str(self.get_input_value("replace"))
        return source.replace(match, replace)


classes = [
    EGN_AppendString,
    EGN_ReplaceString,
    EGN_ContainString,
    EGN_ToUpperString,
    EGN_ToLowerString,
    EGN_SliceString,
    EGN_SliceFromStartString,
    EGN_SliceFromEndString,
    EGN_CapitalizeString,
    EGN_CasefoldString,
    EGN_CountString,
    EGN_EndsWithString,
    EGN_FindString,
    EGN_IndexString,
    EGN_IsAString,
    EGN_StripString,
    EGN_SplitString,
]