import bpy


# create parts xml code
objs = bpy.context.scene.objects
r=2
for n in range(len(objs)):
    obj = objs[n]
    status = bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_VOLUME', center='MEDIAN')
    print(f"""<part id='{n}' name='{obj.name}'>{round(obj.location.x,r)}, {round(obj.location.y,r)}, {round(obj.location.z,r)}, {round(obj.rotation_euler.x,r)}, {round(obj.rotation_euler.y,r)}, {round(obj.rotation_euler.z,r)}</part>""")

# ?
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
