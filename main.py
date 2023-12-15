"""
This file automates creation of a product from parts
"""

import os
import subprocess
from program_from_difd import *

cwd = os.getcwd()
blender_exe = '/home/rms20/Downloads/blender-4.0.1-linux-x64/blender'
blender_project = 'blender/assembly.blend'

# export models to gazebo folders
database_path = "/home/rms/Github/autoassembly/parts/database/"
p1 = cwd + '/blender/prepmodelsforgazebo.py'
subprocess.run([blender_exe, blender_project, p1])

# create the gazebo world with parts layout
world_path = "/home/rms/dev_ws/src/ros2_RobotSimulation/PandaRobot/panda_ros2_gazebo/worlds/panda.world"
assembly_difd = '/home/rms/Github/autoassembly/parts/biplane.difd'
p2 = cwd + '/blender/worldfile_assemblydifd.py'
# todo: export parts layout
subprocess.run([blender_exe, blender_project, '--python', p2, '--background'])

# create difd - currently manually but parts from exporting base .blend obj pose

# create the program from the difd & parts layout
program = '/home/rms/dev_ws/src/ros2_RobotSimulation/ros2_execution/programs/cubePP.txt'
# program = '/home/rms/Github/autoassembly/parts/program.txt'
ap = AssemblePart(program)
assembly = '/home/rms/Github/autoassembly/blender/assembly.blend'
ap.assemble(assembly_difd, assembly)

# run the program