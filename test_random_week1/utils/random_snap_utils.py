import sys
import maya.cmds as cmds
import random

class ObjectPlacementOnTerrain():
    def __init__(self, name, trn):
        """        
            Function for input name and terrain.        
        """         
        self.name = name
        self.trn = trn

    def place_objects(self, minrotation_values=0, maxrotation_values=0, scale_min_values=0, scale_max_values=0, snap_vertices=None, object_to_snap=None):
        """
            Function for creating objects and snapping them to vertices.

            Return
                if no object selected show warning.
        """
        trn_vtx_amount = cmds.polyEvaluate(self.trn, v=True)
        objects = []

        if object_to_snap is None:
            cmds.warning("No object selected for snapping. Please select an object and try again.")
            return

        if snap_vertices is not None:
            if snap_vertices <= trn_vtx_amount:
                vtx_indices = random.sample(range(trn_vtx_amount), snap_vertices)
            else:
                vtx_indices = range(trn_vtx_amount)
        else:
            vtx_indices = range(trn_vtx_amount)

        objects = []

        for i in vtx_indices:
            vtx_id = '{}.vtx[{}]'.format(self.trn, i)
            vtx_pos = cmds.xform(vtx_id, q=True, t=True, ws=True)

            obj = cmds.duplicate(object_to_snap, name='{}_{}_geo'.format(self.name, ('%03d' % i)))[0]
            objects.append(obj)

            random_rotation_x = random.uniform(minrotation_values[0], maxrotation_values[0])
            random_rotation_y = random.uniform(minrotation_values[1], maxrotation_values[1])
            random_rotation_z = random.uniform(minrotation_values[2], maxrotation_values[2])

            cmds.rotate(random_rotation_x, random_rotation_y, random_rotation_z, obj)

            random_scale_x = random.uniform(scale_min_values[0], scale_max_values[0])
            random_scale_y = random.uniform(scale_min_values[1], scale_max_values[1])
            random_scale_z = random.uniform(scale_min_values[2], scale_max_values[2])

            cmds.scale(random_scale_x, random_scale_y, random_scale_z, obj)

            cmds.xform(obj, t=vtx_pos, ws=True)

        cmds.group(objects, name='obj_grp')
