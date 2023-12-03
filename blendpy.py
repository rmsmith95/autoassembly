import bpy
import math

bpy.ops.object.mode_set(mode = 'OBJECT')
obj = bpy.context.active_object
bpy.ops.object.mode_set(mode = 'EDIT') 
bpy.ops.mesh.select_mode(type="VERT")


# get points on resting plane
points = []
min_y = 1000
for v in obj.data.vertices:
    if v.co.y < (min_y-0.0001):
        points = [v]
        min_y = v.co.y
        #bpy.ops.mesh.select_all(action = 'DESELECT')
    elif v.co.y < (min_y+0.0001):
        points.append(v)
        #v.select=True


# calculate base area
total_area = 0
a = points[-1].co
b = points[-2].co
ab = a-b
abl = math.hypot(ab.x, ab.y, ab.z)
for n in range(len(points)-2):
    c = points[n+2].co
    ac = a-c
    bc = b-c
    acl = math.hypot(ac.x, ac.y, ac.z)
    bcl = math.hypot(bc.x, bc.y, bc.z)
    area = abl + acl + bcl / 2
    total_area += area

print(f'total_area = {total_area} mm2')

# get centre of volume
bpy.ops.object.mode_set(mode = 'OBJECT')
bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_VOLUME', center='MEDIAN')
obj.location   # centre of volume
# find the height of COV from the tangent distance to the base plane
# then find minimum radius of the base plane
# stability = base width / COM height

# for now lets use base area to decide which part is the best base to use

# next... look at DIFD and see which parts can be attached




# import STL objects in folder, resize, centre and re-export
import os
folder = "/home/rms20/Github/autoassembly/parts/biplane/"

for file in os.listdir(folder):
    if file[-4:] != '.STL':
        continue
    full_file = folder + file
    bpy.ops.import_mesh.stl(filepath=full_file)

bpy.ops.mesh.select_all(action = 'DESELECT')

# centre objects
for obj in bpy.data.objects:
    obj.location.x = 0
    obj.location.y = 0
    obj.location.z = 0


# export all objects
new_folder = "/home/rms20/Github/autoassembly/parts/biplane_parts/"
for obj in bpy.data.objects:
    if file[-4:] != '.STL':
        continue
    new_path = new_folder + obj.name
    bpy.ops.export_mesh.stl(filepath=new_path, use_selection=True)
