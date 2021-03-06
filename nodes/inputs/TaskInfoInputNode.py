import bpy
import json
from bpy.props import PointerProperty
from ...nodes.BASE.node_tree import RenderStackNode


def update_node(self, context):
    self.update_parms()


class RSNodeTaskInfoInputsNode(RenderStackNode):
    '''A simple input node'''
    bl_idname = 'RSNodeTaskInfoInputsNode'
    bl_label = 'Task Info'

    file: PointerProperty(type=bpy.types.Text, name="Task Info File", update=update_node)

    def init(self, context):
        self.outputs.new('RSNodeSocketTaskSettings', "Settings")
        self.width = 200

    def draw_buttons(self, context, layout):
        layout.prop(self, "file", text="")

    def get_data(self):
        task_data = {}
        try:
            data = json.loads(self.file.as_string())
            task_data.update(data)
        except Exception:
            self.use_custom_color = 1
            self.color = (1, 0, 0)
        return task_data

def register():
    bpy.utils.register_class(RSNodeTaskInfoInputsNode)


def unregister():
    bpy.utils.unregister_class(RSNodeTaskInfoInputsNode)
