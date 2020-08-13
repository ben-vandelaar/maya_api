# Simple Attribute
# import maya.api.OpenMaya as om
#
# node_name = "pCube1"
# attribute_name = "translateY"
#
# selection_list = om.MSelectionList()
# selection_list.add(node_name)
#
# obj = selection_list.getDependNode(0)
#
# if obj.hasFn(om.MFn.kTransform):
#     transform_fn = om.MFnTransform(obj)
#
#     plug = transform_fn.findPlug(attribute_name, False)
#
#     attribute_value = plug.asDouble()
#
#     print("{0}: {1}".format(plug, attribute_value))
#
#     plug.setDouble(2.0)

# Compund Attribute
# import maya.api.OpenMaya as om
#
# node_name = "pCube1"
# attribute_name = "translate"
#
# selection_list = om.MSelectionList()
# selection_list.add(node_name)
#
# obj = selection_list.getDependNode(0)
#
# if obj.hasFn(om.MFn.kTransform):
#     transform_fn = om.MFnTransform(obj)
#
#     plug = transform_fn.findPlug(attribute_name, False)
#
#     if plug.isCompound:
#         for i in range(plug.numChildren()):
#             child_plug = plug.child(i)
#
#             attribute_value = child_plug.asDouble()
#
#             print("{0}: {1}".format(child_plug, attribute_value))

# Another way to effect an attribute
import maya.api.OpenMaya as om

node_name = "pCube1"
attribute_name = "translateY"

selection_list = om.MSelectionList()
selection_list.add(node_name)

obj = selection_list.getDependNode(0)

if obj.hasFn(om.MFn.kTransform):
    transform_fn = om.MFnTransform(obj)

    translation = transform_fn.translation(om.MSpace.kTransform) #Returns a vector
    translation[1] = 3.0
    transform_fn.setTranslation(translation, om.MSpace.kTransform)

