import maya.api.OpenMaya as om
import maya.cmds as cmds


def maya_useNewAPI():
    pass


def initializePlugin(plugin):

    vendor = "Ben van de Laar"
    version = "1.0.0"

    om.MFnPlugin(plugin, vendor, version)


def uninitializePlugin(plugin):
    pass


if __name__ == "__main__":

    plugin_name = "maya_plugin_template.py"

    cmds.evalDeferred(
        'if cmds.pluginInfo("{0}", q=True, loaded=True): cmds.unloadPlugin("{0}")'.format(plugin_name))
    cmds.evalDeferred(
        'if not cmds.pluginInfo("{0}", q=True, loaded=True): cmds.loadPlugin("{0}")'.format(plugin_name))
