import maya.api.OpenMaya as om

selection = om.MGlobal.getActiveSelectionList()

for i in range(selection.length()):
    if i > 0:
        print('---------')

    obj = selection.getDependNode(i)
    print("API type: {0}".format(obj.apiTypeStr))

    if obj.hasFn(om.MFn.kDependencyNode):

        depend_fn = om.MFnDependencyNode(obj)
        print("Dependency Node: {0}".format(depend_fn.name()))

        if obj.hasFn(om.MFn.kTransform):
            transform_fn = om.MFnTransform(obj)
            print("Translation: {0}".format(transform_fn.translation(om.MSpace.kTransform)))

        elif obj.hasFn(om.MFn.kMesh):
            mesh_fn = om.MFnMesh(obj)
            print("Mesh Verticies: {0}".format(mesh_fn.getVertices()))

        elif obj.hasFn(om.MFn.kCamera):
            camera_fn = om.MFnCamera(obj)
            print("Clipping Planes: {0}, {1}".format(camera_fn.nearClippingPlane, camera_fn.farClippingPlane))