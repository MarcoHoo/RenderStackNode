import bpy
from bpy.props import *
from ...nodes.BASE.node_tree import RenderStackNode


def active_version(self, context):
    if self.active > len(self.inputs):
        self.active = len(self.inputs)
    elif self.active < 1:
        self.active = 1

    for i, input in enumerate(self.inputs):
        if input.is_linked:
            node = input.links[0].from_node
            node.mute = 0 if self.active == i + 1 else 1

    dg = context.evaluated_depsgraph_get()
    dg.update()


class RSNodeSettingsMergeNode(RenderStackNode):
    """A simple input node"""
    bl_idname = 'RSNodeSettingsMergeNode'
    bl_label = 'Merge'

    node_type: EnumProperty(name='node type', items=[
        ('SWITCH', 'Switch', ''),
        ('MERGE', 'Merge', ''),
        ('VERSION', 'Version', ''),
    ], default='MERGE')

    active: IntProperty(name='Active Version', default=1, update=active_version)

    def init(self, context):
        self.inputs.new('RSNodeSocketTaskSettings', "Input")
        self.outputs.new('RSNodeSocketTaskSettings', "Output")

    def draw_buttons(self, context, layout):
        if self.node_type in {'MERGE', 'VERSION'}:
            if self.node_type == 'VERSION':
                layout.prop(self, 'active')
        else:
            layout.operator('rsn.switch_setting').node = self.name

    def update(self):
        self.auto_update_inputs()

    def auto_update_inputs(self):
        if self.node_type != 'SWITCH':
            i = 0
            for input in self.inputs:
                if not input.is_linked:
                    # keep one input for links with py commands
                    if i == 0:
                        i += 1
                    else:
                        self.inputs.remove(input)
            # auto add inputs
            if i != 1:
                self.inputs.new('RSNodeSocketTaskSettings', "Input")
        else:
            if len(self.inputs) < 2:
                self.inputs.new('RSNodeSocketTaskSettings', "Input")


def register():
    bpy.utils.register_class(RSNodeSettingsMergeNode)


def unregister():
    bpy.utils.unregister_class(RSNodeSettingsMergeNode)
