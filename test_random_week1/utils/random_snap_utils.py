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

        Parameters:
            minrotation_values (list): Minimum rotation values for X, Y, and Z axes.
            maxrotation_values (list): Maximum rotation values for X, Y, and Z axes.
            scale_min_values (list): Minimum scale values for X, Y, and Z axes.
            scale_max_values (list): Maximum scale values for X, Y, and Z axes.
            snap_vertices (int): Number of vertices to snap to. If 0, snap to all vertices.
            object_to_snap (str): Name of the object to snap.

        Returns:
            None
        """
        if object_to_snap is None:
            cmds.warning("No object selected for snapping. Please select an object and try again.")
            return

        trn_vtx_amount = cmds.polyEvaluate(self.trn, v=True)
        objects = []

        if snap_vertices is not None and snap_vertices != 0:
            # Snap to the specified number of vertices
            if snap_vertices <= trn_vtx_amount:
                vtx_indices = random.sample(range(trn_vtx_amount), snap_vertices)
            else:
                vtx_indices = range(trn_vtx_amount)
        else:
            # Snap to all vertices
            vtx_indices = range(trn_vtx_amount)

        for i in vtx_indices:
            vtx_id = '{}.vtx[{}]'.format(self.trn, i)
            vtx_pos = cmds.xform(vtx_id, q=True, t=True, ws=True)

            # Create a new object using the same name pattern
            obj_name = '{}{}_geo'.format(self.name, ('%03d' % i))

            # Duplicate the object specified by object_to_snap
            obj = cmds.duplicate(object_to_snap, name=obj_name)[0]
            objects.append(obj)

            # Apply random rotation
            random_rotation_x = random.uniform(minrotation_values[0], maxrotation_values[0])
            random_rotation_y = random.uniform(minrotation_values[1], maxrotation_values[1])
            random_rotation_z = random.uniform(minrotation_values[2], maxrotation_values[2])
            cmds.rotate(random_rotation_x, random_rotation_y, random_rotation_z, obj)

            # Apply random scale
            random_scale_x = random.uniform(scale_min_values[0], scale_max_values[0])
            random_scale_y = random.uniform(scale_min_values[1], scale_max_values[1])
            random_scale_z = random.uniform(scale_min_values[2], scale_max_values[2])
            cmds.scale(random_scale_x, random_scale_y, random_scale_z, obj)

            # Move the object to the vertex position
            cmds.xform(obj, t=vtx_pos, ws=True)

        cmds.group(objects, name='obj_grp')
