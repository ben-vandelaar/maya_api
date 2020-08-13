import maya.OpenMaya as om
import maya.OpenMayaMPx as ompx
import maya.cmds as cmds


class BasicDeformerNode(ompx.MPxDeformerNode):

    TYPE_NAME = "basicdeformernode"
    TYPE_ID = om.MTypeId(0x0007F7FC)

    def __init__(self):
        super(BasicDeformerNode, self).__init__()

    def deform(self, data_block, geo_iter, matrix, multi_index):

        envelope = data_block.inputValue(self.envelope).asFloat()

        if envelope == 0:
            return

        geo_iter.reset()
        while not geo_iter.isDone():

            if geo_iter.index() % 2 == 0:
                pt = geo_iter.position()
                #pt.y += (2 * envelope)
                pt = pt * matrix

                geo_iter.setPosition(pt)

            geo_iter.next()

    @classmethod
    def creator(cls):
        return BasicDeformerNode()

    @classmethod
    def initialize(cls):
        pass


def initializePlugin(plugin):
    vendor = "Ben"
    version = "1.0.0"

    plugin_fn = ompx.MFnPlugin(plugin, vendor, version)

    plugin_fn.registerNode(BasicDeformerNode.TYPE_NAME,
                           BasicDeformerNode.TYPE_ID,
                           BasicDeformerNode.creator,
                           BasicDeformerNode.initialize,
                           ompx.MPxNode.kDeformerNode)


def uninitializePlugin(plugin):
    plugin_fn = ompx.MFnPlugin(plugin)
    plugin_fn.deregisterNode(BasicDeformerNode.TYPE_ID)


if __name__ == "__main__":

    cmds.file(new=True, force=True)

    plugin_name = "basic_deformer_node.py"
    cmds.evalDeferred('if cmds.pluginInfo("{0}", q=True, loaded=True): cmds.unloadPlugin("{0}")'.format(plugin_name))
    cmds.evalDeferred('if not cmds.pluginInfo("{0}", q=True, loaded=True): cmds.loadPlugin("{0}")'.format(plugin_name))

    cmds.evalDeferred('cmds.file("C:/Users/benva/Desktop/study/Maya/mayaFiles/basicDeformer.ma",open=True,force=True)')
    cmds.evalDeferred('cmds.select("nurbsPlane1"); cmds.deformer(type="basicdeformernode")')