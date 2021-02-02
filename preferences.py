import bpy
import rna_keymap_ui
from bpy.props import *

from . import __folder_name__


def get_pref():
    return bpy.context.preferences.addons.get(__folder_name__).preferences


class NodeSmtpProps(bpy.types.PropertyGroup):
    show: BoolProperty(name="Dropdown")

    server: StringProperty(
        name="SMTP Server",
        description="Something Like 'smtp.qq.com' or 'smtp.gmail.com'",
        default="")
    password: StringProperty(
        name="SMTP Password",
        description="The SMTP Password for your receiver email",
        subtype='PASSWORD')


class NodeViewerProps(bpy.types.PropertyGroup):
    show: BoolProperty(name="Dropdown")

    update_scripts: BoolProperty(name='Update Scripts ',
                                 description="Update scripts node when using viewer node",
                                 default=False)
    update_path: BoolProperty(name='Update File Path',
                              description="Update File Path node when using viewer node",
                              default=True)
    update_view_layer_passes: BoolProperty(name='Update ViewLayer Passes',
                                           description="Update ViewLayer Passes node when using viewer node",
                                           default=False)


class NodeFilePathProps(bpy.types.PropertyGroup):
    show: BoolProperty(name="Dropdown")

    file_path_separator: EnumProperty(items=[
        ('.', 'Dot', ''),
        ('_', 'Underscore', ''),
        (' ', 'Space', ''), ],
        default='.',
        name='File Path Separator',
        description='Character between $')

    frame_complement: EnumProperty(items=[
        ('None', 'No Complement', ''),
        ('04d', '0001', ''),
        ('_>4d', '___1', '')],
        default='04d',
        name='Frame Complement',
        description='Frame complement(frame 1 for example)')


class RSN_Preference(bpy.types.AddonPreferences):
    bl_idname = __package__

    option: EnumProperty(items=[
        ('PROPERTIES', 'Properties', ''),
        ('NODES', 'Nodes', ''), ],
        default='NODES')

    log_level: EnumProperty(items=[
        ('10', 'Debug', ''),
        ('20', 'Info', ''),
        ('30', 'Warning', ''),
        ('40', 'Error', '')],
        default='30', name='Log Level')

    need_update: BoolProperty(name='Need Update')
    latest_version: IntProperty()

    node_smtp: PointerProperty(type=NodeSmtpProps)
    node_viewer: PointerProperty(type=NodeViewerProps)
    node_file_path: PointerProperty(type=NodeFilePathProps)

    def draw(self, context):
        row = self.layout.row(align=1)
        row.prop(self, "option", expand=1)
        if self.option == "PROPERTIES":
            self.draw_properties()
        elif self.option == "NODES":
            self.draw_nodes()

    def draw_nodes(self):
        layout = self.layout
        col = layout.column(align=1)

        box = col.box().split().column(align=1)
        self.viewer_node(box)

        col.separator(factor=0.2)
        box = col.box().split().column(align=1)
        self.filepath_node(box)

        col.separator(factor=0.2)
        box = col.box().split().column(align=1)
        self.smtp_node(box)

    def draw_properties(self):
        layout = self.layout
        layout.use_property_split = True

        layout.prop(self, 'log_level', text='Debug')

        row = layout.split(factor=0.7)
        row.separator()
        row.operator('rsn.check_update', icon='URL',
                     text='Check Update' if not self.need_update else f"New Version {''.join(str(self.latest_version).split())}!")

    def filepath_node(self, box):
        box.prop(self.node_file_path, 'show', text="File Path Node", emboss=False,
                 icon='TRIA_DOWN' if self.node_file_path.show else 'TRIA_RIGHT')
        if self.node_file_path.show:
            box.use_property_split = True
            box.prop(self.node_file_path, "file_path_separator")
            box.prop(self.node_file_path, "frame_complement")

    def smtp_node(self, box):
        box.prop(self.node_smtp, 'show', text="SMTP Email Node", emboss=False,
                 icon='TRIA_DOWN' if self.node_smtp.show else 'TRIA_RIGHT')
        if self.node_smtp.show:
            box.use_property_split = True
            box.prop(self.node_smtp, "server", text='Server')
            box.prop(self.node_smtp, "password", text='Password')

    def viewer_node(self, box):
        box.prop(self.node_viewer, 'show', text="Viewer Node", emboss=False,
                 icon='TRIA_DOWN' if self.node_viewer.show else 'TRIA_RIGHT')
        if self.node_viewer.show:
            box.use_property_split = True
            box.prop(self.node_viewer, 'update_scripts')
            box.prop(self.node_viewer, 'update_path')
            box.prop(self.node_viewer, 'update_view_layer_passes')


addon_keymaps = []

classes = [
    NodeSmtpProps,
    NodeFilePathProps,
    NodeViewerProps,
    # pref
    RSN_Preference,
]


def add_keybind():
    wm = bpy.context.window_manager
    if wm.keyconfigs.addon:
        km = wm.keyconfigs.addon.keymaps.new(name='Node Editor', space_type='NODE_EDITOR')
        # viewer node
        kmi = km.keymap_items.new('rsn.add_viewer_node', 'V', 'PRESS')
        addon_keymaps.append((km, kmi))
        # mute node
        kmi = km.keymap_items.new('rsn.mute_nodes', 'M', 'PRESS')
        addon_keymaps.append((km, kmi))
        # helper pie
        kmi = km.keymap_items.new('wm.call_menu_pie', 'F', 'PRESS')
        kmi.properties.name = "RSN_MT_PieMenu"
        addon_keymaps.append((km, kmi))


def remove_keybind():
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        for km, kmi in addon_keymaps:
            km.keymap_items.remove(kmi)

    addon_keymaps.clear()


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    add_keybind()


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    remove_keybind()
