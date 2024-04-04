import random
import shutil
from bpelParser import BPELParser
from matcher import Matcher
from metricsEvaluator import MetricsEvaluator


class HDTFramework:
    def computeAL(self, possiblePaths, traversedTasks, anTask, currentTask, parser, matcher, metEval, bpelFile, ppFilename, nextTasks):
        taskAL = 0
        counter = 0
        evaluatedTasks = []  
        for path in possiblePaths:
            tasksInPath = parser.getTasksInPath(path, bpelFile)
            # get tasks between currentTask and task
            if anTask in tasksInPath:
                betweenTasks = tasksInPath[tasksInPath.index(currentTask): tasksInPath.index(anTask)]
                # print('HDTFramework::computeAL - task between', currentTask , 'and', anTask, ':', betweenTasks)
                for taskBet in betweenTasks:
                    # print('HDTFramework::computeAL - current path:', taskPath)
                    pathAL = 0
                    # if taskBet in evaluatedTasks:
                    #     # pathAL += 1
                    #     # counter += 1
                    #     print('HDTFramework::computeAL -', taskBet, 'has been evaluated => Not added', '\n tot pathAL:', pathAL)
                    if taskBet not in evaluatedTasks:
                        tAL = parser.getAL(taskBet, bpelFile)
                        pathAL += tAL
                        evaluatedTasks.append(taskBet)
                        # print('HDTFramework::computeAL -', taskBet, 'AL:', tAL, '\n tot pathAL:', pathAL)
                        counter += 1
                        taskAL += pathAL

            # return round(taskAL/counter, 2)
        return taskAL/counter

    def computeProbability(self, possiblePaths, workflowPaths, task, currentTask, parser, bpelFile):
        probability = 0
        evaluatedPaths = []
        # Get all paths in the workflow containing task
        for path in workflowPaths:
            # print('HDTFramework::computeProbability - current task', currentTask, ', task:', task , ' and path:', path)
            if (task + ':') in path:
                # compute probability from the starting node to current node
                # print('HDTFramework::computeProbability -', task, 'in :', path)
                possibleTaskPathsString = path.split(': ')[1]
                possibleTaskPaths = possibleTaskPathsString.split()
                # print('HDTFramework::computeProbability - possible paths of', task,' and', currentTask,'(current):', possibleTaskPaths)
                for taskPath in possibleTaskPaths:
                    # print('HDTFramework::computeProbability - current path:', taskPath)
                    # print('HDTFramework::computeProbability - possible paths:', possiblePaths)
                    if taskPath in possiblePaths:
                        # print('HDTFramework::computeProbability - current path (', taskPath,') in possible paths:', possiblePaths)
                        pathProbability = 0
                        tasksInPath = parser.getTasksInPath(taskPath, bpelFile)
                        # multiply the probability from the starting task to curentTask
                        # # # get the tasks from the start to current
                        # Get the tasks from the current task to the task
                        taskPosition = tasksInPath.index(task)
                        tasksToTaskId = tasksInPath[tasksInPath.index(currentTask):taskPosition + 1]
                        # print('HDTFramework::computeProbability - tasks in', taskPath, 'from', currentTask, '(current) until task:', tasksToTaskId)
                        if not  tasksToTaskId in evaluatedPaths:
                            for taskToTask in tasksToTaskId:
                                taskPosition = tasksToTaskId.index(taskToTask)
                                if taskPosition == 0:
                                    pathProbability = 1
                                else:
                                    previousTask = tasksToTaskId[taskPosition - 1]
                                    pathProbability = round(parser.getProbability(taskToTask, previousTask, bpelFile) * pathProbability, 4)
                                    # pathProbability *= parser.getProbability(taskToTask, previousTask, bpelFile)
                                    # print('HDTFramework::computeProbability - Task', taskToTask, 'probability:', parser.getProbability(taskToTask, previousTask, bpelFile))
                            probability += pathProbability
                            # probability = round(pathProbability + probability, 2)
                            evaluatedPaths.append(tasksToTaskId)
        return probability
    
    # set the AL for all tasks of a user
    def setAL(self, userType):
        # Random AL depending on the user's type:
        #   - 1 = Unconcerned internet users: AL nel range [0.83, 1]
        #   - 2 = Circumspect internet users: AL nel range [0.5, 0.82]
        #   - 3 = Wary internet users: AL nel range [0.18, 0.49]
        #   - 4 = A larmed internet users: AL nel range [0, 0.17]
        #   - 5 = to compute the th with AL = 1
        alTask = 0
        if userType == 1: 
            alTask = round(random.uniform(0.83, 1.00),2)
        elif userType == 2:
            alTask = round(random.uniform(0.50, 0.82), 2)
        elif userType == 3:
            alTask = round(random.uniform(0.18, 0.49), 2)
        elif userType == 4:
            alTask = round(random.uniform(0, 0.17), 2)
        elif userType == 5:
            alTask = 1
        return alTask

    def initialECComputation(self, bpelFile, outBpelFile, ppFilename, ecResults, userType):
        parser = BPELParser()
        metEval = MetricsEvaluator()

        # 1. get tasks and paths
        tasks = parser.getTasks(bpelFile)
        tasks_paths, allPaths = parser.getPaths(bpelFile)
        # print('HDTFramework::initialECComputation - tasks_paths:', tasks_paths)
        # print('HDTFramework::initialECComputation - tasks:', tasks)

        # Compute the ALs of the user
        for taskId in tasks:
            alTask = self.setAL(userType)
            parser.writeAL(taskId, alTask, outBpelFile)

        workflowPaths = metEval.generatePaths(tasks_paths, allPaths)

        for taskId in tasks:
            ecResults.write("\nEvaluating Task: " + str(taskId))
            possiblePaths = []
            # print('\nHDTFramework::initialECComputation - taskId:', taskId)
            # 2. compute match between pp and pol and then the AL (= get AL from bpel file)
            alTask = parser.getAL(taskId, outBpelFile)
            # print('HDTFramework::initialECComputation - AL of', taskId,':', alTask)
            ecResults.write("\nAL: " + str(alTask))

            # 3. Compute EC for the task:
            # 3.1 Get the task's probability
            probability = 0
            # get the paths containing the task
            for tp in tasks_paths:
                # print('HDTFramework::initialECComputation - tp:', tp)
                if (taskId+':') in tp: #for each path containing taskId
                    # print('HDTFramework::initialECComputation - if ', taskId, 'in', tp)
                    possiblePathsString = tp.split(': ')[1]
                    possiblePaths = possiblePathsString.split()
                    # print('HDTFramework::initialECComputation - possible paths of', taskId,':', possiblePaths)
                    # To avoid duplicates
                    alreadyEvaluatedTasks = []
                    for path in possiblePaths:
                        # get tasks until taskId
                        tasksInPath = parser.getTasksInPath(path, bpelFile)
                        # print('HDTFramework::initialECComputation - tasks in path', path ,':', tasksInPath)
                        # Get previous tasks of taskId
                        taskPosition = tasksInPath.index(taskId)
                        tasksToTaskId = tasksInPath[:taskPosition + 1]
                        # print("HDTFramework::initialECComputation - elements till task position", taskPosition,"(included) in list are : " + str(tasksToTaskId))
                        # avoid duplicates
                        pathProb = 0
                        if tasksToTaskId not in alreadyEvaluatedTasks:
                            # Add the list to the "checking list" and then get the probability
                            alreadyEvaluatedTasks.append(tasksToTaskId)

                            # Compute probability
                            for t in tasksToTaskId:
                                tPosition = tasksToTaskId.index(t)
                                if tPosition == 0:
                                    pathProb = parser.getProbability(t, "Task0", bpelFile)
                                    # print('HDTFramework::initialECComputation - path probability (', path, ') of task', t,':', pathProb)
                                else:
                                    previousTask = tasksToTaskId[tPosition - 1]
                                    # print('HDTFramework::initialECComputation - previous task of', t, ':', previousTask, "probability:",parser.getProbability(t, previousTask, bpelFile))
                                    # pathProb *= parser.getProbability(t, previousTask, bpelFile)
                                    pathProb = round(parser.getProbability(t, previousTask, bpelFile) * pathProb, 4)
                                    # print('HDTFramework::initialECComputation - path probability (', path, ') of task', t,':', pathProb)
                            # print('HDTFramework::initialECComputation - path probability:', pathProb)
                            # sum the probability of different paths
                            # probability = round(pathProb + probability, 2)
                            probability = pathProb + probability
            # print('HDTFramework::initialECComputation - probability of', taskId, ':', probability)
            ecResults.write("\nProbability: " + str(probability))

            # print('HDTFramework::initialECComputation - previous tasks of', taskId, ":", prevTasks)
            # print('HDTFramework::initialECComputation - total EC of', taskId, ':', totECs)

            # Compute the average of the AL of the previous tashs in the same paths as TaskId
            totAL = 0
            counter = 0
            evalTasks = []
            firstEval = False
            # get all the paths passing through taskId
            for path in possiblePaths:
                pathTasks = parser.getTasksInPath(path, bpelFile)
                taskPosition = pathTasks.index(taskId)
                # print('HDTFramework::initialECComputation -', taskId, 'in', path, 'at position:', taskPosition)
                if taskPosition == 0 and firstEval == False:
                    totAL += 1
                    counter += 1
                    firstEval = True
                  #  break
                else:
                    previousTasks = pathTasks[:taskPosition]
                    for pt in previousTasks:
                        if pt not in evalTasks: # So the previous task is evaluated only once
                            evalTasks.append(pt)
                            totAL += parser.getAL(pt, outBpelFile)
                            counter += 1
            # print('HDTFramework::initialECComputation - totAL for', taskId, ':', totAL)
            avgAL = round(totAL/counter, 2)
            # print('HDTFramework::initialECComputation - average AL for', taskId, ':', avgAL)
            ecResults.write("\nAverage AL: " + str(avgAL))


            # 3.3 Get alpha value of task
            avgAlpha = metEval.computeAlpha(taskId, workflowPaths)
            # print('HDTFramework::initialECComputation - average alpha of', taskId, ':', avgAlpha)
            ecResults.write("\nAverage alpha: " + str(avgAlpha))

            # 3.4 Evaluate EC
            # EC with AL 
            ec = metEval.computeEC(alTask, avgAL, probability, avgAlpha)
            # print('HDTFramework::initialECComputation - EC of', taskId, ':', ec)
            ecResults.write("\nEC: " + str(ec) + "\n")

            # 4. Write EC into new .bpel file
            parser.writeEC(taskId, ec, outBpelFile)

            # print('\n')

    def updateEC(self, bpelFile, outBpelFile, currentTask, traversedTasks, ppFilename, ecResults):
        parser = BPELParser()
        matcher = Matcher()
        metEval = MetricsEvaluator()

        # 1. get paths containing currentTask
        # 2. evaluate again the EC of the next tasks in the path considering the new AL values
        #    evaluate also the EC of the current task!
        # 2.1 compute EC:
        #    - get task AL
        #    - get task probability
        #    - get alpha
        #    - get AL of previous tasks
        #       - update the AL of the traversed tasks until currentTask (included) = 1


        # 1. get paths containing currentTask
        #   - get all paths
        #   - extract only the paths containing currentTask
        possiblePaths = []
        pathsInWorkflow, pathList = parser.getPaths(bpelFile)
        # print('HDTFramework::updateEC - paths in workflow:',pathsInWorkflow)
        for path in pathsInWorkflow:
            # print('HDTFramework::updateEC - current path in workflow:',path)
            if (currentTask + ':') in path:
                possiblePathsString = path.split(': ')[1]
                possiblePaths = possiblePathsString.split()
        # print('HDTFramework::updateEC - paths containing', currentTask, ':', possiblePaths)

        # 2. Evaluate (again) the EC from currentTask to the end
        #   - get list of the possible next tasks (including currentTask)
        nextTasks = []
        for path in possiblePaths:
            tasksInPath = parser.getTasksInPath(path, bpelFile)
            currentTaskPosition = tasksInPath.index(currentTask)
            nextTasks.extend(task for task in tasksInPath[currentTaskPosition:] if task not in nextTasks)
        # print('HDTFramework::updateEC - next tasks of', currentTask,':', nextTasks)

        # 2.1 Evaluate the EC of nextTasks (including currentTask)
        for task in nextTasks:
            ecResults.write("\n\nEvaluating Task: " + str(task))
            # get AL
            taskAL = parser.getAL(task, outBpelFile)
            # print('HDTFramework::updateEC - AL of', task,':', taskAL)
            ecResults.write("\nAL: " + str(taskAL))

            # To compute task probability (we need all paths in workflow)
            taskProbability = 0
            if task == currentTask:
                taskProbability = 1
            else:
                taskProbability = self.computeProbability(possiblePaths, pathsInWorkflow, task, currentTask, parser, bpelFile)
                # print('HDTFramework::updateEC - probability of', task, ':', taskProbability)
            ecResults.write("\nProbability: " + str(taskProbability))
            # Compute alpha
            workflowPaths = metEval.generatePaths(pathsInWorkflow, pathList)
            taskAlpha = metEval.computeAlpha(task, workflowPaths)
            ecResults.write("\nAlpha: " + str(taskAlpha))
            # print('HDTFramework::updateEC - average alpha of', task, ':', taskAlpha)

            # Compute AL of previous tasks
            #   AL of traversed task must be 1
            # print('HDTFramework::updateEC - current task:', currentTask, ', analysed task:', task)
            if task == currentTask:
                taskPreviousAL = 1
            else:
                taskPreviousAL = self.computeAL(possiblePaths, task, currentTask, parser, outBpelFile)
            # print('HDTFramework::updateEC - AL of previous tasks:', taskPreviousAL)
            ecResults.write("\nPrevious AL: " + str(taskPreviousAL))

            # Evaluate EC
            taskEC = metEval.computeEC(taskAL, taskPreviousAL, taskProbability, taskAlpha)
            # print('HDTFramework::updateEC - new EC of', task, ':', taskEC)
            ecResults.write("\nEC: " + str(taskEC))


            # 4. Write EC into new .bpel file
            parser.writeEC(task, taskEC, outBpelFile)

            # print('\n')