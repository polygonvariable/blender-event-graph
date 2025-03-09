import bpy


def get_package_name():
    return __package__.replace(".script.base", "")

def get_preference():
    preferences = bpy.context.preferences
    return preferences.addons[get_package_name()].preferences

def create_enum(items = []):
    enum_items = []
    index = 0
    for item in items:
        enum_items.append((item, item, ""))
        index += 1
    return enum_items


variable_map = {}

def flush_variables():
    variable_map.clear()
    print("Variables flushed")

def add_variable(name, value):
    variable_map[name] = value

def get_variable(name):
    return variable_map.get(name, None)

def remove_variable(name):
    if name in variable_map:
        del variable_map[name]

def add_linked_value(node, name, value):
    add_variable(f"{node.node_uuid}_{name}", value)

def get_linked_value(node, name):
    return get_variable(f"{node.node_uuid}_{name}")

def remove_linked_value(node, name):
    remove_variable(f"{node.node_uuid}_{name}")