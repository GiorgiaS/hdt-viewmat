import re
import shutil
from typing import Final

class MetricsEvaluator:
    
    # Weights for parameters
    wData = 1.5
    wPurpose = 1.5
    wTP = 1
    wRetention = 1
    PROBABILITYCOEFF: Final = 0.2


    def computeAL(self, similarities):
        weightedSum = round((similarities['data'] * self.wData + similarities['purp'] * self.wPurpose + similarities['tp'] * self.wTP + similarities['ret'] * 
                       self.wRetention)/(self.wData + self.wPurpose + self.wTP + self.wRetention), 2)
        # print('ECEvaluator::computeAL - All AL:', similarities)
        # print('ECEvaluator::computeAL - total AL:', weightedSum)
        return weightedSum


    def computeAlpha(self, taskId, workflowPaths):
        alphaTot = 0
        counter = 0    
        # For each path, compute the task position
        for path in workflowPaths:
            if taskId in workflowPaths[path]:
                # print('MetricsEvaluator::computeAlpha - task', taskId, 'in path:', path)
                alphaTot += ((workflowPaths[path].index(taskId)+1)/(len(workflowPaths[path])+1))
                # print('MetricsEvaluator::computeAlpha - alphaTot', alphaTot)
                counter += 1

        avgAlpha = round(alphaTot/counter,2)
        # print('MetricsEvaluator::computeAlpha - average Alpha', avgAlpha)
        return avgAlpha


    # It stores the paths of the workflow in a dictionary
    def generatePaths(self, tasks_paths, paths):
        # Initialise the dictionary with the path as keys, and values as empty lists
        workflowPaths = {}
        for path in paths:
            workflowPaths[path] = []
        
        for task in tasks_paths:
            # Extract the task id and the paths
            taskId = task.split(':')[0]
            taskPaths = re.findall(r'[^:\s]+', task)[1:len(task)]

            # Insert the taskId in the paths of the workflow
            for path in taskPaths:
                workflowPaths[path].append(taskId)

        # print('MetricsEvaluator::generatePaths - paths into dictionary:') 
        # for path in workflowPaths:
        #     print(path, ':', sorted(workflowPaths[path], key=lambda s: int(re.search(r'\d+', s).group())))
        # print('\n')

        return workflowPaths
        
    def computeEC(self, taskAL, previousAL, taskProb, taskAlpha):
        if taskProb >= 1:
            taskProb = 1
        ec = previousAL * (taskAL + taskAlpha * (1 - taskAL)) * taskProb
        # ec = round(previousAL * (taskAL + taskAlpha * (1 - taskAL)) * taskProb, 2)
        return ec
    