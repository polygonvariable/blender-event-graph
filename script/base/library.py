import mathutils
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

def is_vector(vec, size):
    return isinstance(vec, tuple) and len(vec) == size


cache_map = {}

def flush_cache():
    cache_map.clear()
    print("Cache flushed")

def add_cache(name, value):
    cache_map[name] = value

def get_cache(name):
    return cache_map.get(name, None)

def remove_cache(name):
    if name in cache_map:
        del cache_map[name]

def add_linked_cache(node, name, value):
    add_cache(f"{node.node_uuid}_{name}", value)

def get_linked_cache(node, name):
    return get_cache(f"{node.node_uuid}_{name}")

def remove_linked_cache(node, name):
    remove_cache(f"{node.node_uuid}_{name}")