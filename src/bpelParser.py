import xml.etree.ElementTree as ET
import re
from lxml import etree

# This class is responsible for reading the bpel file, extracting the paths and probabilities
# Then, it generates a new bpel file storing the EC

class BPELParser:
    namespace = '{http://docs.oasis-open.org/wsbpel/2.0/process/executable}'
    namespaceTasks = '{http://schemas.oracle.com/bpel/extension}'

    # ToDo: it prints twice tasks. Maybe it traverse twice the process
    def getTasks(self, bpelFile):
        bpelTree = ET.parse(bpelFile)
        bpelRoot = bpelTree.getroot()
        tasks = []
        tasks = self.exploreTasks(bpelRoot, tasks)
        # print('BPELParser::gettasks - tasks:', tasks)
        return tasks

    def exploreTasks(self, element, tasks):
        for el in element:
            if el.tag == f'{self.namespace}invoke':
                taskName = el.get('name')
                tasks.append(taskName)
            else:
                self.exploreTasks(el, tasks)
        return tasks


    def getPaths(self, bpelFile):
        bpelTree = ET.parse(bpelFile)
        tasks = self.getTasks(bpelFile)
        # print('BPELParser::getPaths - tasks:', tasks)
        tasks_paths = []
        paths = []
        for taskId in tasks:
            for property in bpelTree.findall(f".//{self.namespace}invoke[@name='{taskId}']/{self.namespaceTasks}toProperties/{self.namespaceTasks}toProperty"):
                if property.get('name') == 'paths':
                    path = property.text
                    task_path = taskId + ': ' + path
                    tasks_paths.append(task_path)

                    # # Extract all the paths and remove duplicates
                    paths.extend(x for x in path.split() if x not in paths)

        # print('BPELParser::getPaths - taskId-paths:', tasks_paths)
        # print('BPELParser::getPaths - paths:', paths)
        return tasks_paths, paths

    # Returns all tasks in a path
    def getTasksInPath(self, pathID, bpelFile):
        tasks = []
        task_paths, _ = self.getPaths(bpelFile)
        for tp in task_paths:
            # print("BpelParser::getTasksInPath - tp:", tp)
            tpSplitted = tp.split(' ')
            if pathID in tpSplitted:
                # print("BpelParser::getTasksInPath - pathID:", pathID, ' tpSplitted:', tpSplitted, '\n')
                tasks.append(tpSplitted[0].replace(':',''))

        return sorted(tasks, key=lambda s: int(re.search(r'\d+', s).group()))

    def getProbability(self, taskId, prevTask, bpelFile):
        bpelTree = ET.parse(bpelFile)
        probability = 0
        for property in bpelTree.findall(f".//{self.namespace}invoke[@name='{taskId}']/{self.namespaceTasks}toProperties/{self.namespaceTasks}toProperty"):
                if property.get('name') == 'probability':
                    probabilities = property.text
                    task_probability = probabilities.split()
                    # print('BPELParser::getProbability - all input probabilities:', task_probability)
                    # print('BPELParser::getProbability - previousTask in BPEL:', probabilities)
                    # print('BPELParser::getProbability - previousTask in input:', prevTask)
                    for tp in task_probability:
                        if prevTask in tp:
                            # print('BPELParser::getProbability - input probability of task', prevTask, '(', tp.split(':')[0],'):', tp.split(':')[1])
                            probability = float(tp.split(':')[1])
        return probability


    def getEC(self, taskId, bpelFile):
        bpelTree = ET.parse(bpelFile)
        bpelRoot = bpelTree.getroot()
        ec = bpelRoot.find(f".//{self.namespace}invoke[@name='{taskId}']/{self.namespaceTasks}toProperties/{self.namespaceTasks}toProperty[@name='ec']")
        # print('BPELParser::getEC - EC of', taskId,':', ec.text)
        return round(float(ec.text), 2)
    
    def getAL(self, taskId, bpelFile):
        bpelTree = ET.parse(bpelFile)
        bpelRoot = bpelTree.getroot()
        al = bpelRoot.find(f".//{self.namespace}invoke[@name='{taskId}']/{self.namespaceTasks}toProperties/{self.namespaceTasks}toProperty[@name='al']")
        # print('BPELParser::getEC - EC of', taskId,':', ec.text)
        return round(float(al.text), 2)

    def writeEC(self, taskId, ec, enhancedBpelFile):

        bpelTree = etree.parse(enhancedBpelFile)
        bpelRoot = bpelTree.getroot()

        invokeElement = bpelRoot.findall(f".//{self.namespace}invoke")

        for invoke in invokeElement:
            toPropertiesElement = invoke.find(f'.//{self.namespaceTasks}toProperties')

            if invoke.get('name') == taskId:

                toPropertyEC = toPropertiesElement.find(f".//{self.namespaceTasks}toProperty[@name='ec']")
                if toPropertyEC is not None: # if EC already exists, update (for dynamic evaluation)
                    # print('BPELParser::writeEC - property EC of', taskId, 'is not empty')
                    toPropertyEC.text = str(ec)
                else: # Write the EC (for initial or static evaluation)
                    # print('BPELParser::writeEC - property EC of', taskId, 'is empty')
                    toPropertyEC = etree.Element(f'{self.namespaceTasks}toProperty', name='ec')
                    toPropertyEC.text = str(ec)
                    toPropertiesElement.append(toPropertyEC)                    

        modified_bpel_xml = etree.tostring(bpelTree, pretty_print=True, encoding='utf-8', xml_declaration=True).decode('utf-8')

        # Write the modified XML back to the original file
        with open(enhancedBpelFile, 'w', encoding='utf-8') as f:
            f.write(modified_bpel_xml)

        return 0
    

    def writeAL(self, taskId, al, enhancedBpelFile):

        bpelTree = etree.parse(enhancedBpelFile)
        bpelRoot = bpelTree.getroot()

        invokeElement = bpelRoot.findall(f".//{self.namespace}invoke")

        for invoke in invokeElement:
            toPropertiesElement = invoke.find(f'.//{self.namespaceTasks}toProperties')

            if invoke.get('name') == taskId:
                toPropertyAL = toPropertiesElement.find(f".//{self.namespaceTasks}toProperty[@name='al']")
                if toPropertyAL is not None: # if EC already exists, update (for dynamic evaluation)
                    # print('BPELParser::writeEC - property EC of', taskId, 'is not empty')
                    toPropertyAL.text = str(al)
                else: # Write the EC (for initial or static evaluation)
                    # print('BPELParser::writeEC - property EC of', taskId, 'is empty')
                    toPropertyAL = etree.Element(f'{self.namespaceTasks}toProperty', name='al')
                    toPropertyAL.text = str(al)
                    toPropertiesElement.append(toPropertyAL)                    

        modified_bpel_xml = etree.tostring(bpelTree, pretty_print=True, encoding='utf-8', xml_declaration=True).decode('utf-8')

        # Write the modified XML back to the original file
        with open(enhancedBpelFile, 'w', encoding='utf-8') as f:
            f.write(modified_bpel_xml)

        return 0

