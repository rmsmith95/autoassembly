# read difd to write a program that controls the robot arm
import xml.etree.ElementTree as ET
import os


class Part:
    def __init__(self, id, name, pose):
        self.id = str(id)
        self.name = name
        self.pose = pose

class AssemblePart:
    """
    Inputs are:
    Assebmly DIFD
    assembly file with parts (.blend?)
    """
    def __init__(self, file):
        if os.path.isfile(program):
            os.remove(program)
        self.parts = dict()
        self.program = file
        self.ref_assembly = [0.0, 0.3, 0.0, 0.0, 0.0, 90.0]
        self.assembly = ''
        with open(self.program, "a") as program:
            self.program.write(f"""{{'action': 'GripperOpen'}}\n""")
    
    # we need pose of parts in the assembly (check blender) relative to other parts
    # query blender for pose of part of interest. Can even untransparent as joined?

    def move(self, part, dest=None):
        if dest is None:
            dest = self.ref_assembly
        
        with open(self.program, "a") as program:
            # 1. move arm to part
            # how to get part location? live or pre?
            x, y, z, yw, p, r = part.pose
            x = round(x, 2)
            y = round(y, 2)
            z = round(z + 1.6, 2)
            p = 180
            program.write(f"""{{'action': 'MoveXYZW', 'value': {{'positionx': {x}, 'positiony': {y}, 'positionz': {z}, 'yaw': {float(yw)}, 'pitch': {float(p)}, 'roll': {float(r)}}}, 'speed': 1.0}}\n""")
            # 2. grasp part
            program.write(f"""{{'action': 'GripperClose'}}\n""")
            # 3. move part to dest
            # this moves the arm to the pose
            # either call live 1 by 1 or in a .txt program
            x, y, z, yw, p, r = dest
            x = round(x, 2)
            y = round(y, 2)
            z = round(z + 1.6, 2)
            p = 180
            program.write(f"""{{'action': 'MoveXYZW', 'value': {{'positionx': {x}, 'positiony': {y}, 'positionz': {z}, 'yaw': {float(yw)}, 'pitch': {float(p)}, 'roll': {float(r)}}}, 'speed': 1.0}}\n""")
            # 4. let go of it
            program.write(f"""{{'action': 'GripperOpen'}}\n""")

    def join(self, id, parts_string):
        parts_ids = []
        for ps in parts_string.split(', '):
            parts_ids.append(ps)
        assembly = self.parts[parts_ids[0]]
        self.move(assembly)
        for i in parts_ids[1:]:
            part = self.parts[i]
            self.move(part, assembly.pose)
        self.parts[id] = assembly

    def assemble(self, difd):
        # self.assembly = assembly
        tree = ET.parse(difd)
        root = tree.getroot()
        # self.gripper_write(0,180,0)
        for child in root:
            print(child.tag, child.attrib)
            if child.tag == 'part':
                pose = []
                for s in child.text.split(', '):
                    pose.append(float(s))
                part = Part(child.attrib['id'], child.attrib['name'], pose)
                self.parts[child.attrib['id']] = part
            elif child.tag == 'join':
                self.join(child.attrib['id'], child.text)
            elif child.tag == 'move':
                pose = []
                for s in child.text.split(', '):
                    pose.append(float(s))
                self.move(self.parts[child.attrib['part']], pose)


# program = '/home/rms/dev_ws/src/ros2_RobotSimulation/ros2_execution/programs/cubePP.txt'
# # program = '/home/rms/Github/autoassembly/parts/program.txt'
# ap = AssemblePart(program)
# path = '/home/rms/Github/autoassembly/parts/biplane.difd'
# assembly = '/home/rms/Github/autoassembly/blender/assembly.blend'
# ap.assemble(path, assembly)

# path = '/home/rms/Github/autoassembly/parts/biplane.difd'
# assembly = '/home/rms/Github/autoassembly/assembly.blend'
# import xml.etree.ElementTree as ET
# tree = ET.parse(path)
# root = tree.getroot()