model_str = f"""
    <include>
      <uri>model://{name}</uri>
      <pose>{pose}</pose>
    </include>
"""



wolrd_file = f"""
<?xml version="1.0" ?>

<sdf version="1.4">

  <world name="default">
    <include>
      <uri>model://ground_plane</uri>
    </include>

    <include>
      <uri>model://sun</uri>
    </include>
    
    {models}

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