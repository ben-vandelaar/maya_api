import maya.api.OpenMaya as om

selection_list = om.MGlobal.getActiveSelectionList()

#traversal_type = om.MItDag.kBreadthFirst
traversal_type = om.MItDag.kDepthFirst

filter_type = om.MFn.kMesh

dag_iter = om.MItDag(traversal_type,filter_type)

if not selection_list.isEmpty():
    dag_iter.reset(selection_list.getDependNode(0), traversal_type, filter_type)

while not dag_iter.isDone():

    #print(dag_iter.partialPathName()) #dag_iter.fullPathName()
    #dag_path = dag_iter.getPath()
    #print(dag_path.fullPathName())

    shape_obj = dag_iter.currentItem()
    dag_fn = om.MFnDagNode(shape_obj)
    for i in range(dag_fn.parentCount()):
        parent_fn = om.MFnDagNode(dag_fn.parent(i))
        print(parent_fn.fullPathName())

    dag_iter.next()