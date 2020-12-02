import bpy
from RenderStackNode.node_tree import RenderStackNode


class RSNodeSettingsMergeNode(RenderStackNode):
    '''A simple input node'''
    bl_idname = 'RSNodeSettingsMergeNode'
    bl_label = 'Merge Settings'

    def init(self, context):
        self.inputs.new('RSNodeSocketOutputSettings', "Output Settings")
        self.outputs.new('RSNodeSocketTaskSettings', "Settings")
        self.width = 180

    def draw_buttons(self, context, layout):
        pass

    def draw_buttons_ext(self, context, layout):
        add = layout.operator("rsnode.edit_input", text="Add Output Settings")
        add.remove = False
        add.socket_type = "RSNodeSocketOutputSettings"
        add.socket_name  = "Output Settings"

        remove = layout.operator("rsnode.edit_input", text="Remove Unused")
        remove.remove = True


def register():
    bpy.utils.register_class(RSNodeSettingsMergeNode)

def unregister():
    bpy.utils.unregister_class(RSNodeSettingsMergeNode)