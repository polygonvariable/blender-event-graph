bl_info = {
    "name": "Blender Event Graph",
    "author": "polygonvariable",
    "version": (1, 0),
    "blender": (4, 2, 0),
    "location": "Editor Type > Event Graph",
    "description": "Perform blender python operations using node",
    "warning": "",
    "doc_url": "https://github.com/polygonvariable/event-graph",
    "category": "Utility",
}

from .script import eg_app

def register():
    eg_app.register()

def unregister():
    eg_app.unregister()

if __name__ == "__main__":
    eg_app.register()