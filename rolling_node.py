import maya.api.OpenMaya as om

import maya.cmds as cmds


def maya_useNewAPI():
    pass


class RollingNode(om.MPxNode):

    TYPE_NAME = "rollingnode"
    TYPE_ID = om.MTypeId(0x0007F7F9)

    distance_obj = None
    radius_obj = None
    rotation_obj = None

    def __init__(self):
        super(RollingNode, self).__init__()

    def compute(self, plug, data):
        if plug == self.rotation_obj:

            distance = data.inputValue(RollingNode.distance_obj).asDouble()
            radius = data.inputValue(RollingNode.radius_obj).asDouble()

            if radius == 0:
                rotation = 0
            else:
                rotation = distance / radius

            rotation_data_handle = data.outputValue(RollingNode.rotation_obj)
            rotation_data_handle.setDouble(rotation)

            data.setClean(plug)

    @classmethod
    def creator(cls):
        return RollingNode()

    @classmethod
    def initialize(cls):
        numeric_attr = om.MFnNumericAttribute()

        cls.distance_obj = numeric_attr.create("distance", "dist", om.MFnNumericData.kDouble, 0.0)
        numeric_attr.readable = False
        numeric_attr.keyable = True

        cls.radius_obj = numeric_attr.create("radius", "rad", om.MFnNumericData.kDouble, 0.0)
        numeric_attr.readable = False
        numeric_attr.keyable = True

        unit_attr = om.MFnUnitAttribute()

        cls.rotation_obj = unit_attr.create("rotation", "rot", om.MFnUnitAttribute.kAngle, 0.0)

        cls.addAttribute(cls.distance_obj)
        cls.addAttribute(cls.radius_obj)
        cls.addAttribute(cls.rotation_obj)

        cls.attributeAffects(cls.distance_obj, cls.rotation_obj)
        cls.attributeAffects(cls.radius_obj, cls.rotation_obj)


def initializePlugin(plugin):
    vendor = "Ben van de Laar"
    version = "1.0.0"

    plugin_fn = om.MFnPlugin(plugin, vendor, version)

    try:
        plugin_fn.registerNode(RollingNode.TYPE_NAME,
                               RollingNode.TYPE_ID,
                               RollingNode.creator,
                               RollingNode.initialize,
                               om.MPxNode.kDependNode)
    except:
        om.MGlobal.displayError("Failed to register node: {0}".format(RollingNode.TYPE_NAME))


def uninitializePlugin(plugin):

    plugin_fn = om.MFnPlugin(plugin)

    try:
        plugin_fn.deregisterNode(RollingNode.TYPE_ID)
    except:
        om.MGlobal.displayError("Failed to deregister node: {0}".format(RollingNode.TYPE_NAME))


if __name__ == "__main__":
    """
    For Development Only
    """
    cmds.file(new=True, force=True)

    plugin_name = "rolling_node.py"

    cmds.evalDeferred('if cmds.pluginInfo("{0}", q=True, loaded=True): cmds.unloadPlugin("{0}")'.format(plugin_name))
    cmds.evalDeferred('if not cmds.pluginInfo("{0}", q=True, loaded=True): cmds.loadPlugin("{0}")'.format(plugin_name))

    cmds.evalDeferred('cmds.file("C:/Users/benva/Desktop/study/Maya/mayaFiles/rolling.ma", open=True, force=True)')
