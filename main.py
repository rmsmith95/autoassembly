"""
This file automates creation of a product from parts
"""

import os
import subprocess
from make_program import *

cwd = os.getcwd()
blender_exe = '/opt/blender-3.6.5-linux-x64/blender'
assembly_blend = 'assemblies/biplane/biplane_assembly.blend'
parts_blend = 'assemblies/biplane/parts_on_floor.blend'

# make_gazebo_part_folders
make_folders_path = cwd + '/scripts/make_gazebo_part_folders.py'
subprocess.run([blender_exe, parts_blend, '--python', make_folders_path, '--background'])

# create the gazebo world, difd, & parts layout files
assembly_difd = '/home/rms/Github/autoassembly/test/biplane.difd'
make_difd_path = cwd + '/scripts/worldfile_assemblydifd.py'
subprocess.run([blender_exe, assembly_blend, '--python', make_difd_path, '--background'])

# create the program from the difd & parts layout
program = '/home/rms/dev_ws/src/ros2_RobotSimulation/ros2_execution/programs/panda_test.txt'
difd = '/home/rms/Github/autoassembly/test/biplane.difd'
partpose = '/home/rms/Github/autoassembly/test/partpose.txt'
ap = AssemblePart(program)
ap.assemble(partpose, difd)

# ap.assemble(assembly_difd, assembly)

# run the program