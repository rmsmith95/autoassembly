import bpy

#bpy.ops.mesh.select_mode(type="VERT")
objs = bpy.context.scene.objects
for n in range(len(objs)):
    obj = objs[n]
    obj.select_set(True)
    bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_VOLUME', center='MEDIAN')
    obj.location.x=100*(n%4)
    obj.location.y=100*(n//4)
    obj.location.z=0

# lift
for n in range(len(objs)):
obj = objs[n]
# set z
bpy.ops.object.mode_set(mode = 'EDIT') 
min_z = 1000
for v in obj.data.vertices:
    if v.co.x < min_z:
        min_z = v.co.x

bpy.ops.object.mode_set(mode = 'OBJECT') 
obj.location.z = -min_z
obj.select_set(False)
