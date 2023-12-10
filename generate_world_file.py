"""
gazebo .world file
"""


def model_str(name, pose):
  return f"""
    <include>
      <uri>model://{name}</uri>
      <pose>{pose}</pose>
    </include>
"""

wf1 = """
<?xml version="1.0" ?>

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

model_names = [
  '10)Landing Gear',
  '16)Vertical cross bar',
  '7)Horizontal Tail',
  '11)Main Axle',
  '16)Vertical cross bar.001',
  '8)Vertical Tail',
  '12)Wheel',
  '1)Lower Wing',
  '9)Pilot',
  '12)Wheel.001',
  '2)Upper Wing',
  '13)Wheel Axle',
  '3)Fuselage',
  '13)Wheel Axle.001',
  '4)Motor',
  '14)Stud 6×32mm',
  '5)Propeller',
  '15)Stud 4×15mm',
  '6)Holder',
]

world_path = "/home/rms/dev_ws/src/ros2_RobotSimulation/PandaRobot/panda_ros2_gazebo/worlds/panda.world"
with open(world_path, 'w') as f:
  f.write(wf1)
  for n, name in enumerate(model_names):
    pose = f'{0.2*(n%4)+0.2} {0.2*(n//4)-0.4} 0.1 0 0 0'
    ob_str = model_str(name, pose)
    f.write(ob_str)
  f.write(wf2)
