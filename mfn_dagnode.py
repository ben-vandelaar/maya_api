import maya.api.OpenMaya as om

selection_list = om.MGlobal.getActiveSelectionList()

if not selection_list.isEmpty():
    dag_fn = om.MFnDagNode(selection_list.getDependNode(0))

    print("Children: \n")
    for i in range(dag_fn.childCount()):
        child_fn = om.MFnDagNode(dag_fn.child(i))
        print(child_fn.fullPathName())

    print("Parents: \n")
    for i in range(dag_fn.parentCount()):
        parent_fn = om.MFnDagNode(dag_fn.parent(i))
        print(parent_fn.fullPathName())