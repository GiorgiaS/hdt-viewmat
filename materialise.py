
from bpelParser import BPELParser
import statistics
import numpy 

class Materialise:
    # thresholds = {
    #     # 'mean' : 0.0,
    #     # 'median' : 0.0,
    #     # '80percentile' : 0.0,
    #     # '20percentile' : 0.0,
    #     # '50percentile' : 0.0,
    #     # '70percentile' : 0.0
    # } #avg, median, percentile
    thresholds = {
        'mean' : 0.0,
    }

    ECValuesAL1 = []

    # Get the EC of all tasks when AL = 1 and store the value within ECValuesAL1
    def addECs(self, tasks, bpelFile, ecResults):
        # Empty list
        self.ECValuesAL1 = []

        parser = BPELParser()
        for task in tasks:
            self.ECValuesAL1.append(parser.getEC(task, bpelFile))
        print('Materialise::addECs - added ECs to list:', self.ECValuesAL1)
        ecResults.write("\nECs of workflow: " + str(self.ECValuesAL1))
    
    def computeThresholds(self, ecResults):
        # average
        avg = statistics.mean(self.ECValuesAL1)
        sum = 0
        # for ec in self.ECValuesAL1:
        #     sum += ec
        # avg = sum/len(self.ECValuesAL1)
        print('Materialise::computeThresholds - avg:', avg)
        self.thresholds['mean'] = avg

        # # median
        # median = statistics.median(self.ECValuesAL1)
        # print('Materialise::computeThresholds - median:', median)
        # self.thresholds['median'] = median
        # # percentile
        # percentile = numpy.percentile(self.ECValuesAL1, 80)
        # print('Materialise::computeThresholds - 80 percentile:', percentile)
        # self.thresholds['80percentile'] = percentile
  
        # percentile = numpy.percentile(self.ECValuesAL1, 20)
        # print('Materialise::computeThresholds - 20 percentile:', percentile)
        # self.thresholds['20percentile'] = percentile

        # percentile = numpy.percentile(self.ECValuesAL1, 50)
        # print('Materialise::computeThresholds - 50 percentile:', percentile)
        # self.thresholds['50percentile'] = percentile
        
        # percentile = numpy.percentile(self.ECValuesAL1, 70)
        # print('Materialise::computeThresholds - 70 percentile:', percentile)
        # self.thresholds['70percentile'] = percentile
        
        # ecResults.write("\nThresholds of workflow: \n\tMean: " + str(self.thresholds['mean']) + "\n\tMedian: " + str(self.thresholds['median']) + "\n\t80 Percentile: " + str(self.thresholds['80percentile']) + "\n\t20 Percentile: " + str(self.thresholds['20percentile']) + "\n\t50 Percentile: " + str(self.thresholds['50percentile']) + "\n")
        ecResults.write("\nThresholds of workflow: \n\tMean: " + str(self.thresholds['mean']) + "\n")

        return self.thresholds
    
    def staticPrematerialisedTasks(self, tasks, tasksInPath, parser, enhancedBPelFile, th):
        tasksPathPrematerialised = 0
        tasksProcessPrematerialised = 0
        precomputedTasks = []

        parser = BPELParser()
       
        for task in tasks:         
            taskEC = parser.getEC(task, enhancedBPelFile)
            # print('UserSimulator::wastedTimePrecomp -', task, 'EC:', taskEC)
            #    If EC > threshold precompute - i.e., sum the computation time to totPathPrecomputationTime
            if taskEC >= self.thresholds[th]:
                tasksProcessPrematerialised += 1
                precomputedTasks.append(task)
                if task in tasksInPath:
                    tasksPathPrematerialised += 1
        # print('UserSimulator::staticWastedTimePrecomp - total precomputed tasks (path):', tasksPathPrecomputed)
        # print('UserSimulator::staticWastedTimePrecomp - total precomputed tasks (workflow):', tasksWorkflowPrecomputed)
        # print('UserSimulator::staticWastedTimePrecomp - total wasted tasks:', wastedTasks)

        return tasksPathPrematerialised, tasksProcessPrematerialised, precomputedTasks


    def dynamicPrematerialisedTasks(self, parser, tasks, enhancedBPELFile, precomputedTasks, th, tasksInPath):
        # for each task which has not been already precomputed
        #   and with EC > threshold => precompute
        tasksPathPrematerialised = 0
        tasksProcessPrematerialised = 0
        newPrecomputedTasks = []
        for task in tasks:
            taskEC = parser.getEC(task, enhancedBPELFile)
            if task not in precomputedTasks and taskEC >= self.thresholds[th]:
                newPrecomputedTasks.append(task)
                tasksProcessPrematerialised +=1
                if task in tasksInPath:
                    tasksPathPrematerialised += 1
        return newPrecomputedTasks, tasksPathPrematerialised, tasksProcessPrematerialised

   
    
    def getThreshold(self):
        return self.thresholds