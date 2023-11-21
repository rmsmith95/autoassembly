"""
This file automates creation of a product from parts
"""

import os
import subprocess

# 1. Get parts path
os.getcwd()

# open blender
blender_exe = '/home/rms20/Downloads/blender-4.0.1-linux-x64/blender'
blender_project = 'base.blend'
subprocess.run([blender_exe, blender_project])

# load part, find COM, find base
# part_file = '/home/rms20/Github/autoassembly/parts/biplane/1)Lower Wing.STL'
# todo: load part, for now will be in base

"""
import bpy

bpy.ops.object.mode_set(mode = 'OBJECT')
obj = bpy.context.active_object
bpy.ops.object.mode_set(mode = 'EDIT') 
bpy.ops.mesh.select_mode(type="VERT")


points = []
min_y = 1000
for v in obj.data.vertices:
    if v.co.y < (min_y-0.0001):
        points = [v]
        min_y = v.co.y
        bpy.ops.mesh.select_all(action = 'DESELECT')
    elif v.co.y < (min_y+0.0001):
        points.append(v)
        v.select=True

bpy.ops.mesh.select_all(action = 'DESELECT')
bpy.ops.object.mode_set(mode = 'OBJECT')
for v in points:
    v.select = True
bpy.ops.object.mode_set(mode = 'EDIT') 

"""