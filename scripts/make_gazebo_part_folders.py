# prep models in .blend to folder in gazebo database
import os
import shutil
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


def urdf(file, name, collision, visual):
    scale = 1.0
    with open(file, 'w') as f:
        f.write(f"""<?xml version="1.0"?>
<robot name="{name}">
  <link name="{name}">
    <collision>
      <origin xyz= "0.0 0.0 0.0" rpy="0 0 0"/>
      <geometry>
        <mesh filename="file://$(find ros2_grasping)/urdf/{name}.dae" scale="1 1 1"/>
      </geometry>
    </collision>
    <visual>
      <origin xyz= "0.0 0.0 0.0" rpy="0 0 0"/>
      <geometry>
        <mesh filename="file://$(find ros2_grasping)/urdf/{name}.dae" scale="1 1 1"/>
      </geometry>
    </visual>
    <inertial>
      <origin xyz= "0.0 0.0 0.0" rpy="0 0 0"/>
      <mass value= "0.1" />
      <inertia
        ixx="0.15" ixy="0.0"  ixz="0.0"
        iyy="0.15" iyz="0.0"
        izz="0.15" />
    </inertial>
  </link>
</robot>
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
    if os.path.isdir(new_folder):
        shutil.rmtree(new_folder)
    os.mkdir(new_folder)
    obj.select_set(True)
    model_config(new_folder + "model.config", obj.name, obj.name)
    collision = f"{obj.name}/{obj.name}.stl"
    visual = f"{obj.name}/{obj.name}.dae"
    # export for gazebo objects
    model_sdf(new_folder + "model.sdf", obj.name, collision, visual)
    bpy.ops.export_mesh.stl(filepath=stl_path, use_selection=True)
    bpy.ops.wm.collada_export(filepath=dae_path, selected=True)
    # export for gazebo in robotics project
    fp = '/home/rms/dev_ws/src/ros2_RobotSimulation/ros2_grasping/urdf/' + obj.name
    bpy.ops.wm.collada_export(filepath=fp+".dae", selected=True)
    urdf(fp + ".urdf", obj.name, collision, visual)
    #
    obj.select_set(False)


database_path = "/home/rms/Github/autoassembly/database/"
# parts_folder = "/home/rms20/Github/autoassembly/parts/biplane/"
export_objects(database_path)
