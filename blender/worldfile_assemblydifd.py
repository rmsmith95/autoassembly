import os
import bpy


wf1 = """<?xml version="1.0" ?>
<sdf version="1.4">
  <world name="default">
    <include>
      <uri>model://ground_plane</uri>
    </include>
    <include>
      <uri>model://sun</uri>
    </include>
"""

wf2 = """    
    <scene>
      <shadows>0</shadows>
    </scene>

    <!-- GAZEBO PLUGINS: -->
    <!-- The following plugins must be activated for the ros2_grasping to effectively work: -->

    <plugin name="gazebo_ros_state" filename="libgazebo_ros_state.so">
      <ros>
        <namespace>/ros2_grasp</namespace>
        <argument>model_states:=model_states</argument>
        <argument>link_states:=link_states</argument>
      </ros>
      <update_rate>1.0</update_rate>
    </plugin>

    <plugin name="gazebo_ros_properties" filename="libgazebo_ros_properties.so">
      <ros>
        <namespace>/ros2_grasp</namespace>
      </ros>
    </plugin>

  </world>
</sdf>
"""

def get_pose(n, name):
    x = round(0.1*(n%4)+0.2, 2)
    y = round(0.2*(n//4)-0.4, 2)
    # pose = f'{x} {y} 1.4 0 0 0'
    pose = [x, y, 1.4, 0, 0, 0]
    return pose


def gazebo_model_str(name, pose):
  return f"""
  <include>
    <uri>model://{name}</uri>
    <pose>{pose[0]} {pose[1]} {pose[2]} {pose[3]} {pose[4]} {pose[5]}</pose>
  </include>
"""


def create_world_file_and_assembly_difd(pose_file, world_path, assembly_difd):
  model_names = []
  for obj in bpy.data.objects:
    model_names.append(obj.name)
  # write gazebo world file
  init_poses = []
  with open(world_path, 'w') as f:
    f.write(wf1)
    for n, name in enumerate(model_names):
      pose = get_pose(n, name)
      ob_str = gazebo_model_str(name, pose)
      f.write(ob_str)
      init_poses.append(pose)
    f.write(wf2)
  with open(pose_file, 'w') as f:
    for pose in init_poses:
      f.write(f'{pose[0]} {pose[1]} {pose[2]} {pose[3]} {pose[4]} {pose[5]}\n')
  # write assembly difd
  with open(assembly_difd, 'w') as f:
    f.write("""<?xml version="1.0"?>
<assembly name="biplane">""")
    for n, name in enumerate(model_names):
      pose = get_pose(n, name)
      x = round(obj.location.x, 2)
      y = round(obj.location.y, 2)
      z = round(obj.location.z, 2)
      pose_str = f'{x} {y} {z} {0} {0} {0}'
      part_str = f"""\t<part id='{n}' name='{name}'>{pose_str}</part>\n"""
      f.write(part_str)
    f.write("""</assembly>""")


# world_path = "/home/rms/dev_ws/src/ros2_RobotSimulation/PandaRobot/panda_ros2_gazebo/worlds/panda.world"
world_path = '/home/rms/Github/autoassembly/test/world.txt'
assembly_difd = '/home/rms/Github/autoassembly/test/biplane.difd'
pose_file = '/home/rms/Github/autoassembly/test/partpose.txt'
create_world_file_and_assembly_difd(pose_file, world_path, assembly_difd)
