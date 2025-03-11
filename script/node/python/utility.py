import math
import datetime
import time
import bpy
from bpy.props import ( BoolProperty, FloatProperty, EnumProperty, StringProperty, IntProperty, PointerProperty, CollectionProperty, FloatVectorProperty )

from ...base.node import EG_Node, EG_PureNode
from ...base.library import create_enum
from ...socket.primitive import EGS_Value


class EGN_Print(EG_Node):
    """Prints a value into console"""
    
    bl_idname = "egn.python.print"
    bl_label = "Print"

    def init(self, context):
        self.add_exec_in("exec")
        self.add_in(EGS_Value.bl_idname, "value")
        self.add_exec_out("exec")

    def execute(self):
        print(self.get_input_value("value"))
        self.execute_next("exec")


class EGN_SyncDelay(EG_Node):
    """Create a blocking delay for the next execution"""
    
    bl_idname = "egn.python.sync_delay"
    bl_label = "Sync Delay"
    bl_icon = "PREVIEW_RANGE"

    def init(self, context):
        self.add_exec_in("exec")
        self.add_in("NodeSocketFloat", "time", 1, False)
        self.add_exec_out("exec")

        self.inputs["time"].default_value = 5

    def execute(self):

        in_time = self.get_input_value("time")
        if in_time < 0.1:
            print("Minimum time is 0.1 seconds")
            return
        
        time.sleep(in_time)
        self.execute_next("exec")


class EGN_AsyncDelay(EG_Node):
    """Create a non-blocking delay for the next execution"""
    
    bl_idname = "egn.python.async_delay"
    bl_label = "Async Delay"
    bl_icon = "PREVIEW_RANGE"

    def init(self, context):
        self.add_exec_in("exec")
        self.add_in("NodeSocketFloat", "time", 1, False)
        self.add_exec_out("exec")

        self.inputs["time"].default_value = 5

    def execute(self):

        in_time = self.get_input_value("time")
        if in_time < 0.1:
            print("Minimum time is 0.1 seconds")
            return

        def delayed_execution():
            self.execute_next("exec")
            return None

        bpy.app.timers.register(delayed_execution, first_interval=in_time)


class EGN_Math(EG_PureNode):
    """Node with math methods"""
    
    bl_idname = "egn.python.math"
    bl_label = "Math"

    single_in = {
        "acos", "acosh", "asin", "asinh", "atan", "atanh", "ceil", "cos",
        "cosh", "degrees", "erf", "erfc", "exp", "expm1", "fabs",
        "floor", "frexp", "gamma", "lgamma", "log",
        "log10", "log1p", "log2", "radians", "sin", "sinh", "sqrt",
        "tan", "tanh", "trunc"
    }
    
    double_in = {
        "atan2", "copysign", "fmod", "hypot", "ldexp", "pow", "remainder"
    }

    integer_single_in = {
        "factorial"
    }
    integer_double_in = {
        "comb", "perm", "gcd", "prod"
    }

    def update_socket(self, context):
        """Dynamically update input sockets based on selected method"""
        if self.methods in self.double_in or self.methods in self.integer_double_in:
            if "b" not in self.inputs:
                self.add_in("NodeSocketFloat", "b", 1, False)
        else:
            if "b" in self.inputs:
                self.rem_in("b")

    methods: EnumProperty(
        name="Method",
        items=[(op, op, "") for op in single_in | double_in | integer_single_in | integer_double_in],
        default="acos",
        update=update_socket
    ) # type: ignore

    def draw_buttons(self, context, layout):
        layout.prop(self, "methods")

    def init(self, context):
        """Initialize node with inputs"""

        self.add_in("NodeSocketFloat", "a", 1, False)
        self.add_out("NodeSocketFloat", "result")  # bind: result -> on_result

    def on_result(self):
        """Perform selected math operation dynamically"""

        in_a = self.get_input_value("a")
        in_b = self.get_input_value("b") if self.methods in self.double_in or self.methods in self.integer_double_in else None

        if self.methods in self.integer_single_in:
            in_a = int(in_a)

        elif self.methods in self.integer_double_in:
            in_a = int(in_a)
            in_b = int(in_b) if in_b is not None else None

        math_method = getattr(math, self.methods, None)
        if callable(math_method):
            try:
                if self.methods in self.integer_single_in:
                    return math_method(in_a)
                
                elif self.methods in self.integer_double_in or self.methods in self.double_in:
                    return math_method(in_a, in_b) if in_b is not None else 0
                
                else:
                    return math_method(in_a)
                
            except ValueError as e:
                print(f"Math error in {self.methods}: {e}")
                return -1

        return -1


classes = [
    EGN_Print,
    EGN_SyncDelay,
    EGN_AsyncDelay,
    EGN_Math
]