import sys
import maya.cmds as cmds

class ObjectPlacementOnTerrain():
    def __init__(self, name, trn):
        """        
            Function for input name and terrain.        
        """         
        self.name = name
        self.trn = trn

    def place_objects(self, minrotation_values, maxrotation_values, scale_min_values, scale_max_values, snap_vertices=None):
        """
            Function for create name object to snap vertex and group. Create random scale and rotation.
            Ardyments :
                minrotation_values = store input min values rotation.
                maxrotation_values = store input max values rotation.
                scale_min_values = store input min values scale.
                scale_max_values = store input max values scale.
                snap_vertices=None are when user didn't input number for snap then snap all vertex.

            return 
                Random rotation and scale values also the object that was created by name padding are 3.
        """

        trn_vtx_amount = cmds.polyEvaluate(self.trn, v=True)
        
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
            obj_name = '{}{}_geo'.format(self.name, ('%03d' % i))

            vtx_pos = cmds.xform(vtx_id, q=True, t=True, ws=True)
            obj = cmds.polyCone(name=obj_name)[0]
            objects.append(obj)

            # Apply user-defined rotation and scale values
            random_rotation_x = random.uniform(minrotation_values[0], maxrotation_values[0])
            random_rotation_y = random.uniform(minrotation_values[1], maxrotation_values[1])
            random_rotation_z = random.uniform(minrotation_values[2], maxrotation_values[2])

            cmds.rotate(random_rotation_x, random_rotation_y, random_rotation_z, obj)

            # Generate random scale values within the specified ranges
            random_scale_x = random.uniform(scale_min_values[0], scale_max_values[0])
            random_scale_y = random.uniform(scale_min_values[1], scale_max_values[1])
            random_scale_z = random.uniform(scale_min_values[2], scale_max_values[2])

            cmds.scale(random_scale_x, random_scale_y, random_scale_z, obj)
            
            cmds.xform(obj, t=vtx_pos, ws=True)

        cmds.group(objects, name='obj_grp')