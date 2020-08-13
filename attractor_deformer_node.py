import maya.OpenMaya as om
import maya.OpenMayaMPx as ommpx

import maya.cmds as cmds


class AttractorDeformerNode(ommpx.MPxDeformerNode):

    TYPE_NAME = "attractordeformernode"
    TYPE_ID = om.MTypeId(0x0007F7FE)

    MAX_ANGLE = 0.5 * 3.14159265  # 90 degrees

    def __init__(self):
        super(AttractorDeformerNode, self).__init__()

    def deform(self, data_block, geo_iter, world_matrix, multi_index):

        envelope = data_block.inputValue(self.envelope).asFloat()
        if envelope == 0:
            return

        max_distance = data_block.inputValue(AttractorDeformerNode.max_distance).asFloat()
        if max_distance == 0:
            return

        target_position = data_block.inputValue(AttractorDeformerNode.target_position).asFloatVector()
        target_position = om.MPoint(target_position) * world_matrix.inverse()
        target_position = om.MFloatVector(target_position)

        input_handle = data_block.outputArrayValue(self.input)
        input_handle.jumpToElement(multi_index)
        input_element_handle = input_handle.outputValue()

        input_geom = input_element_handle.child(self.inputGeom).asMesh()
        mesh_fn = om.MFnMesh(input_geom)

        normals = om.MFloatVectorArray()
        mesh_fn.getVertexNormals(False, normals)

        geo_iter.reset()
        while not geo_iter.isDone():

            pt_local = geo_iter.position()

            target_vector = target_position - om.MFloatVector(pt_local)

            distance = target_vector.length()
            if distance <= max_distance:

                normal = normals[geo_iter.index()]

                angle = normal.angle(target_vector)
                if angle <= AttractorDeformerNode.MAX_ANGLE:

                    offset = target_vector * ((max_distance - distance) / max_distance)

                    geo_iter.setPosition(pt_local + om.MVector(offset))

            geo_iter.next()

    def accessoryAttribute(self):
        return AttractorDeformerNode.target_position

    def accessoryNodeSetup(self, dag_modifier):

        locator = dag_modifier.createNode("locator")

        locator_fn = om.MFnDependencyNode(locator)

        locator_translate_plug = locator_fn.findPlug("translate", False)

        target_position_plug = om.MPlug(self.thisMObject(), AttractorDeformerNode.target_position)
        dag_modifier.connect(locator_translate_plug, target_position_plug)

    @classmethod
    def creator(cls):
        return AttractorDeformerNode()

    @classmethod
    def initialize(cls):
        numeric_attr = om.MFnNumericAttribute()

        cls.max_distance = numeric_attr.create("maximumDistance", "maxDist", om.MFnNumericData.kFloat, 1.0)
        numeric_attr.setKeyable(True)
        numeric_attr.setMin(0.0)
        numeric_attr.setMax(2.0)

        cls.target_position = numeric_attr.createPoint("targetPosition", "targetPos");
        numeric_attr.setKeyable(True)

        cls.addAttribute(cls.max_distance)
        cls.addAttribute(cls.target_position)

        output_geom = ommpx.cvar.MPxGeometryFilter_outputGeom
        cls.attributeAffects(cls.max_distance, output_geom)
        cls.attributeAffects(cls.target_position, output_geom)


def initializePlugin(plugin):
    vendor = "Ben van de Laar"
    version = "1.0.0"

    plugin_fn = ommpx.MFnPlugin(plugin, vendor, version)
    try:
        plugin_fn.registerNode(AttractorDeformerNode.TYPE_NAME,
                               AttractorDeformerNode.TYPE_ID,
                               AttractorDeformerNode.creator,
                               AttractorDeformerNode.initialize,
                               ommpx.MPxNode.kDeformerNode)
    except:
        om.MGlobal.displayError("Failed to register node: {0}".format(AttractorDeformerNode.TYPE_NAME))


def uninitializePlugin(plugin):
    plugin_fn = ommpx.MFnPlugin(plugin)
    try:
        plugin_fn.deregisterNode(AttractorDeformerNode.TYPE_ID)
    except:
        om.MGlobal.displayError("Failed to deregister node: {0}".format(AttractorDeformerNode.TYPE_NAME))


if __name__ == "__main__":
    cmds.file(new=True, force=True)

    plugin_name = "attractor_deformer_node.py"
    cmds.evalDeferred('if cmds.pluginInfo("{0}", q=True, loaded=True): cmds.unloadPlugin("{0}")'.format(plugin_name))
    cmds.evalDeferred('if not cmds.pluginInfo("{0}", q=True, loaded=True): cmds.loadPlugin("{0}")'.format(plugin_name))

    cmds.evalDeferred(
        'cmds.file("C:/Users/benva/Desktop/study/Maya/mayaFiles/accessory_node_test.ma",open=True, force=True)')

    cmds.evalDeferred('cmds.select(sourceSphere); cmds.deformer(type="attractordeformernode")')