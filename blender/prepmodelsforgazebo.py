# prep models in .blend to folder in gazebo database
import os
import bpy


def model_config(file, name, description):
    with open(file, 'w') as f:
        f.write(f"""<?xml version="1.0"?>
<model>
  <name>{name}</name>
  <version>1.0</version>
  <sdf version="1.6">model.sdf</sdf>
  <author>
    <name>Robert Smith</name>
    <email></email>
  </author>
  <description>
    {description}
  </description>
</model>
""")
          

def model_sdf(file, name, collision, visual):
    scale = 0.001
    with open(file, 'w') as f:
        f.write(f"""<?xml version="1.0" ?>
<sdf version="1.6">
  <model name="{name}">
    <static>true</static>
    <link name="link">
      <collision name="collision">
        <geometry>
          <mesh>
            <scale>{scale} {scale} {scale}</scale>
            <uri>model://{collision}</uri>
          </mesh>
        </geometry>
      </collision>
      <visual name="visual">
        <geometry>
          <mesh>
            <scale>{scale} {scale} {scale}</scale>
            <uri>model://{visual}</uri>
          </mesh>
        </geometry>
      </visual>
    </link>
  </model>
</sdf>
""")

def export_objects(database_path):
  for obj in bpy.data.objects:
      # centre objects
      obj.location.x = 0
      obj.location.y = 0
      obj.location.z = 0
      new_folder = database_path + obj.name + "/"
      stl_path = new_folder + obj.name + '.stl'
      dae_path = new_folder + obj.name + '.dae'
      os.mkdir(new_folder)
      obj.select_set(True)
      model_config(new_folder + "model.config", obj.name, obj.name)
      collision = f"{obj.name}/{obj.name}.stl"
      visual = f"{obj.name}/{obj.name}.dae"
      model_sdf(new_folder + "model.sdf", obj.name, collision, visual)
      bpy.ops.export_mesh.stl(filepath=stl_path, use_selection=True)
      bpy.ops.wm.collada_export(filepath=dae_path, selected=True)
      obj.select_set(False)


database_path = "/home/rms/Github/autoassembly/parts/database/"
# parts_folder = "/home/rms20/Github/autoassembly/parts/biplane/"
# base_blend_file = "/home/rms/Github/autoassembly/base.blend"
export_objects(database_path)
