import bpy
from bpy.props import ( BoolProperty, FloatProperty, EnumProperty, StringProperty, IntProperty, PointerProperty, CollectionProperty )

from ..base.node import EG_Node, EG_PureNode
from ..base.library import create_enum

from ..socket.primitive import EGS_Value


class PNY_AppendString(EG_PureNode):
    """Node to append strings"""
    
    bl_idname = "PNY_AppendString"
    bl_label = "Append"

    def init(self, context):
        self.add_in("NodeSocketString", "a", 1, False)
        self.add_in("NodeSocketString", "b", 1, False)
        self.add_out("NodeSocketString", "result") # bind: result -> on_result

    def on_result(self):
        return str(self.get_input_value("a")) + str(self.get_input_value("b"))


class PNY_ContainString(EG_PureNode):
    """Node to check if a string contains another string"""
    
    bl_idname = "PNY_ContainString"
    bl_label = "Contains"

    def init(self, context):
        self.add_in("NodeSocketString", "source", 1, False)
        self.add_in("NodeSocketString", "match", 1, False)
        self.add_out("NodeSocketBool", "result") # bind: result -> on_result

    def on_result(self):
        source = str(self.get_input_value("source"))
        match = str(self.get_input_value("match"))
        return match in source


class PNY_SliceString(EG_PureNode):
    """Node to slice a string"""
    
    bl_idname = "PNY_SliceString"
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


class PNY_SliceFromStart(EG_PureNode):
    """Node to slice a string from start"""
    
    bl_idname = "PNY_SliceFromStart"
    bl_label = "Slice From Start"

    def init(self, context):
        self.add_in("NodeSocketString", "source", 1, False)
        self.add_in("NodeSocketInt", "start", 1, False)
        self.add_out("NodeSocketString", "result") # bind: result -> on_result

    def on_result(self):
        source = str(self.get_input_value("source"))
        start = int(self.get_input_value("start"))
        return source[:start]


class PNY_SliceFromEnd(EG_PureNode):
    """Node to slice a string from end"""
    
    bl_idname = "PNY_SliceFromEnd"
    bl_label = "Slice From End"

    def init(self, context):
        self.add_in("NodeSocketString", "source", 1, False)
        self.add_in("NodeSocketInt", "end", 1, False)
        self.add_out("NodeSocketString", "result") # bind: result -> on_result

    def on_result(self):
        source = str(self.get_input_value("source"))
        end = int(self.get_input_value("end"))
        return source[end:]


class PNY_ToUpper(EG_PureNode):
    """Node to convert a string to upper case"""
    
    bl_idname = "PNY_ToUpper"
    bl_label = "To Upper"

    def init(self, context):
        self.add_in("NodeSocketString", "source", 1, False)
        self.add_out("NodeSocketString", "result") # bind: result -> on_result

    def on_result(self):
        source = str(self.get_input_value("source"))
        return source.upper()


class PNY_ToLower(EG_PureNode):
    """Node to convert a string to lower case"""
    
    bl_idname = "PNY_ToLower"
    bl_label = "To lower"

    def init(self, context):
        self.add_in("NodeSocketString", "source", 1, False)
        self.add_out("NodeSocketString", "result") # bind: result -> on_result

    def on_result(self):
        source = str(self.get_input_value("source"))
        return source.lower()


class PNY_CapitalizeString(EG_PureNode):
    """Node to capitalize a string"""
    
    bl_idname = "PNY_CapitalizeString"
    bl_label = "Capitalize"

    def init(self, context):
        self.add_in("NodeSocketString", "source", 1, False)
        self.add_out("NodeSocketString", "result") # bind: result -> on_result

    def on_result(self):
        source = str(self.get_input_value("source"))
        return source.capitalize()


class PNY_CasefoldString(EG_PureNode):
    """Node to casefold a string"""
    
    bl_idname = "PNY_CasefoldString"
    bl_label = "Casefold"

    def init(self, context):
        self.add_in("NodeSocketString", "source", 1, False)
        self.add_out("NodeSocketString", "result") # bind: result -> on_result

    def on_result(self):
        source = str(self.get_input_value("source"))
        return source.casefold()


class PNY_CountString(EG_PureNode):
    """Node to count a string"""
    
    bl_idname = "PNY_CountString"
    bl_label = "Count"

    def init(self, context):
        self.add_in("NodeSocketString", "source", 1, False)
        self.add_in("NodeSocketString", "match", 1, False)
        self.add_out("NodeSocketInt", "result") # bind: result -> on_result

    def on_result(self):
        source = str(self.get_input_value("source"))
        match = str(self.get_input_value("match"))
        return source.count(match)


class PNY_EndsWithString(EG_PureNode):
    """Node to check if a string ends with another string"""
    
    bl_idname = "PNY_EndsWithString"
    bl_label = "Ends With"

    def init(self, context):
        self.add_in("NodeSocketString", "source", 1, False)
        self.add_in("NodeSocketString", "match", 1, False)
        self.add_out("NodeSocketBool", "result") # bind: result -> on_result

    def on_result(self):
        source = str(self.get_input_value("source"))
        match = str(self.get_input_value("match"))
        return source.endswith(match)


class PNY_FindString(EG_PureNode):
    """Node to get index of a string"""
    
    bl_idname = "PNY_FindString"
    bl_label = "Find"

    def init(self, context):
        self.add_in("NodeSocketString", "source", 1, False)
        self.add_in("NodeSocketString", "match", 1, False)
        self.add_out("NodeSocketInt", "result") # bind: result -> on_result

    def on_result(self):
        source = str(self.get_input_value("source"))
        match = str(self.get_input_value("match"))
        return source.find(match)


class PNY_IndexString(EG_PureNode):
    """Node to get index of a string"""
    
    bl_idname = "PNY_IndexString"
    bl_label = "Index Of"

    def init(self, context):
        self.add_in("NodeSocketString", "source", 1, False)
        self.add_in("NodeSocketString", "match", 1, False)
        self.add_out("NodeSocketInt", "result") # bind: result -> on_result

    def on_result(self):
        source = str(self.get_input_value("source"))
        match = str(self.get_input_value("match"))
        return source.index(match)


class PNY_IsAString(EG_PureNode):
    """Node to check if a string is an instance of another string"""
    
    bl_idname = "PNY_IsAString"
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

class PNY_StripString(EG_PureNode):
    """Node to remove spaces from a string"""
    
    bl_idname = "PNY_StripString"
    bl_label = "Strip"

    def init(self, context):
        self.add_in("NodeSocketString", "source", 1, False)
        self.add_out("NodeSocketString", "result") # bind: result -> on_result

    def on_result(self):
        source = str(self.get_input_value("source"))
        return source.strip()


class PNY_SplitString(EG_PureNode):
    """Node to split a string"""
    
    bl_idname = "PNY_SplitString"
    bl_label = "Split"

    def init(self, context):
        self.add_in("NodeSocketString", "source", 1, False)
        self.add_in("NodeSocketString", "separator", 1, False)
        self.add_out("NodeSocketString", "result") # bind: result -> on_result

    def on_result(self):
        source = str(self.get_input_value("source"))
        separator = str(self.get_input_value("separator"))
        return source.split(separator)


class PNY_ReplaceString(EG_PureNode):
    """Node to replace strings"""
    
    bl_idname = "PNY_ReplaceString"
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
    PNY_AppendString,
    PNY_ReplaceString,
    PNY_ContainString,
    PNY_ToUpper,
    PNY_ToLower,
    PNY_SliceString,
    PNY_SliceFromStart,
    PNY_SliceFromEnd,
    PNY_CapitalizeString,
    PNY_CasefoldString,
    PNY_CountString,
    PNY_EndsWithString,
    PNY_FindString,
    PNY_IndexString,
    PNY_IsAString,
    PNY_StripString,
    PNY_SplitString,
]