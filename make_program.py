# read difd to write a program that controls the robot arm
import xml.etree.ElementTree as ET
import os


class Part:
    def __init__(self, id, name, pose):
        self.id = str(id)
        self.name = name
        self.pose = pose

class AssemblePart:
    """"""
    def __init__(self, program):
        test_program = '/home/rms/Github/autoassembly/test/test_program.bash'
        if os.path.isfile(program):
            os.remove(program)
        self.parts = dict()
        self.program = program
        self.test_program = test_program
        with open(self.program, "w") as program:
            program.write(f"""{{'action': 'GripperOpen'}}\n""")
            # program.write(f"""{{'action': 'MoveG', 'value': {{'goal':' 0.04'}}}}\n""")
        with open(self.test_program, "w") as program2:
            program2.write("#!/bin/bash\n")
            program2.write(f"""ros2 action send_goal -f /MoveG ros2_data/action/MoveG \"{{'goal':' 0.04'}}\"\n""")
    
    # we need pose of parts in the assembly (check blender) relative to other parts
    # query blender for pose of part of interest. Can even untransparent as joined?
    
    def staging1(self):
        return f"""{{'action': 'MoveJs', 'value': {{'joint1': 90.00, 'joint2': -42.00, 'joint3': 0.00, 'joint4': -156.00, 'joint5': 0.00, 'joint6': 26.00, 'joint7': 0.00}}, 'speed': 1.0}}\n"""
    
    def staging2(self):
        return f"""{{'action': 'MoveJs', 'value': {{'joint1': -90.00, 'joint2': -42.00, 'joint3': 0.00, 'joint4': -156.00, 'joint5': 0.00, 'joint6': 26.00, 'joint7': 0.00}}, 'speed': 1.0}}\n"""


    def move(self, part, dest):
        # 1. move arm to part
        # how to get part location? live or pre?
        section = ""
        x, y, z, yw, p, r = part.pose
        x = 0.1
        y = -0.1
        z = -0.2
        section += self.staging1()
        section += f"""{{'action': 'MoveL', 'value': {{'movex': {x}, 'movey': {y}, 'movez': {z}}}, 'speed': 1.0}}\n"""
        # 2. grasp part
        section += f"""{{'action': 'GripperClose'}}\n"""
        section += self.staging1()
        # 3. move part to dest
        # this moves the arm to the pose
        # either call live 1 by 1 or in a .txt program
        x, y, z, yw, p, r = dest
        x = round(float(x), 3)
        y = round(float(y), 3)
        z = round(float(z)+0.2, 3)
        section += self.staging2()
        section += f"""{{'action': 'MoveL', 'value': {{'movex': {x}, 'movey': {y}, 'movez': {z}}}, 'speed': 1.0}}\n"""
        # 4. let go of it
        section += f"""{{'action': 'GripperOpen'}}\n"""
        section += self.staging2()
        # write section to the program
        with open(self.program, "a") as program:
            program.write(section)
    
    def test_move(self, part, dest):
        with open(self.test_program, "a") as program2:
            x, y, z, yw, p, r = part.pose
            x = round(float(x), 3)
            y = round(float(y), 3)
            z = round(float(z)+0.2, 3)
            z2 = round(float(z)+0.2, 3)
            p = 180
            program2.write(f"""ros2 action send_goal -f /MoveXYZW ros2_data/action/MoveXYZW "{{positionx: {x}, positiony: {y}, positionz: {z2}, yaw: 0.00, pitch: {p}, roll: 0.00, speed: 1.0}}\"\n""")
            program2.write(f"""ros2 action send_goal -f /MoveXYZW ros2_data/action/MoveXYZW "{{positionx: {x}, positiony: {y}, positionz: {z}, yaw: 0.00, pitch: {p}, roll: 0.00, speed: 1.0}}\"\n""")
            program2.write(f"""ros2 action send_goal -f /MoveG ros2_data/action/MoveG \"{{'goal':' 0.00'}}\"\n""")
            x, y, z, yw, p, r = dest
            x = round(float(x), 3)
            y = round(float(y), 3)
            z = round(float(z)+0.2, 3)
            z2 = round(float(z)+0.2, 3)
            p = 180
            print(str(z))
            program2.write(f"""ros2 action send_goal -f /MoveXYZW ros2_data/action/MoveXYZW "{{positionx: {x}, positiony: {y}, positionz: {z2}, yaw: 0.00, pitch: {p}, roll: 0.00, speed: 1.0}}\"\n""")
            program2.write(f"""ros2 action send_goal -f /MoveXYZW ros2_data/action/MoveXYZW "{{positionx: {x}, positiony: {y}, positionz: {z}, yaw: 0.00, pitch: {p}, roll: 0.00, speed: 1.0}}\"\n""")
            program2.write(f"""ros2 action send_goal -f /MoveG ros2_data/action/MoveG \"{{'goal':' 0.04'}}\"\n""")
            

    # def join(self, id, parts_string):
    #     parts_ids = []
    #     for ps in parts_string.split(', '):
    #         parts_ids.append(ps)
    #     assembly = self.parts[parts_ids[0]]
    #     # self.move(assembly)
    #     for i in parts_ids[1:]:
    #         part = self.parts[i]
    #         self.move(part, assembly.pose)
    #     self.parts[id] = assembly

    def assemble(self, partpose, difd):
        with open(partpose, 'r') as f:
            # self.assembly = assembly
            tree = ET.parse(difd)
            root = tree.getroot()
            # self.gripper_write(0,180,0)
            for child in root:
                print(child.tag, child.attrib)
                if child.tag == 'part':
                    pose_str = f.readline()
                    pose = pose_str.split(' ')
                    # for s in child.text.split(', '):
                    #     pose.append(float(s))
                    part = Part(child.attrib['id'], child.attrib['name'], pose)
                    self.parts[child.attrib['id']] = part
                    dest_pose = child.text.split(' ')
                    print(f'dst={dest_pose}')
                    self.move(part, dest_pose)
                    self.test_move(part, dest_pose)
                # elif child.tag == 'join':
                #     self.join(child.attrib['id'], child.text)
                # elif child.tag == 'move':
                #     pose = []
                #     for s in child.text.split(', '):
                #         pose.append(float(s))
                #     self.move(self.parts[child.attrib['part']], pose)


program = '/home/rms/dev_ws/src/ros2_RobotSimulation/ros2_execution/programs/panda_test.txt'
# program = '/home/rms/Github/autoassembly/test/program.txt'
ap = AssemblePart(program)
# difd = '/home/rms/Github/autoassembly/parts/biplane.difd'
difd = '/home/rms/Github/autoassembly/test/biplane.difd'
partpose = '/home/rms/Github/autoassembly/test/partpose.txt'
ap.assemble(partpose, difd)

# path = '/home/rms/Github/autoassembly/parts/biplane.difd'
# assembly = '/home/rms/Github/autoassembly/assembly.blend'
# import xml.etree.ElementTree as ET
# tree = ET.parse(path)
# root = tree.getroot()