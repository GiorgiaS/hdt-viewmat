import os
from bpelParser import BPELParser
from termcolor import colored
from hdtFramework import HDTFramework

import shutil
import xlsxwriter

from materialise import Materialise

class UserSimulator:
    workflows = {
        'APP' : ['path1', 'path2','path3', 'path4','path5', 'path6','path7', 'path8', 'path9', 'path10','path11', 'path12', 'path13', 'path14','path15', 'path16', 'path17', 'path18', 'path19', 'path20', 'path21'],
        'Tuberculosis' : ['path1', 'path2','path3', 'path4','path5', 'path6','path7', 'path8', 'path9', 'path10','path11', 'path12', 'path13', 'path14','path15', 'path16', 'path17', 'path18', 'path19', 'path20', 'path21', 'path22', 'path23'],
        'GestationalDiabetes' : ['path1', 'path2', 'path3', 'path4','path5', 'path6','path7', 'path8', 'path9', 'path10','path11', 'path12'],
        'CoronaryHeartDisease' : ['path1', 'path2','path3', 'path4','path5', 'path6','path7', 'path8', 'path9'],
        'NhincComponentAuditLog' : ['path1', 'path2','path3', 'path4','path5', 'path6','path7', 'path8', 'path9', 'path10','path11', 'path12', 'path13', 'path14','path15', 'path16', 'path17', 'path18', 'path19', 'path20', 'path21','path22','path23', 'path24','path25', 'path26','path27', 'path28', 'path29', 'path30','path31', 'path32', 'path33', 'path34','path35', 'path36', 'path37', 'path38', 'path39', 'path40', 'path41', 'path42', 'path43', 'path44'],
        'AstroBookStore' : ['path1', 'path2','path3', 'path4','path5', 'path6','path7', 'path8', 'path9', 'path10','path11', 'path12', 'path13', 'path14','path15', 'path16', 'path17', 'path18', 'path19', 'path20', 'path21','path22','path23', 'path24','path25', 'path26','path27', 'path28', 'path29', 'path30','path31', 'path32', 'path33', 'path34', 'path35', 'path36', 'path37', 'path38', 'path39', 'path40', 'path41', 'path42', 'path43', 'path44', 'path45'],
        'Synchronous' : ['path1', 'path2', 'path3', 'path4', 'path5', 'path6', 'path7', 'path8', 'path9', 'path10', 'path11', 'path12'],
        'ClaimsProcess' : ['path1', 'path2', 'path3', 'path4', 'path5'],
        'PartsDataService' : ['path1', 'path2','path3', 'path4','path5', 'path6', 'path7', 'path8', 'path9', 'path10', 'path11', 'path12'],
        'LoanProcessWithSwimlanes' : ['path1', 'path2'],
        'BankTransferFlow2':  ['path1', 'path2'],
        'Synchronous1': ['path1', 'path2'],
        'SOAOrderBooking' : ['path1', 'path2','path3', 'path4'],
        'ResilientFlow' : ['path1', 'path2','path3', 'path4'],
        'DslService' : ['path1', 'path2'],
        'EntityComponentInternalSubscribeOrch' : ['path1', 'path2'],
        'EntityComponentInternalUnsubscribeOrch' : ['path1', 'path2'],
        'LoanApprovalProcess' : ['path1', 'path2', 'path3'],
        'LoanApprovalProcess1' : ['path1', 'path2', 'path3'],
        'LoanProcess' : ['path1', 'path2','path3', 'path4'],
        'NhinUnsubscribe' : ['path1', 'path2', 'path3'],
        'PrestamoRamas' : ['path1', 'path2','path3'],
        'QuoteProcess' : ['path1', 'path2','path3'],
        'TaxiServiceProvider' : ['path1', 'path2'],
        'WorkoutProcess' : ['path1', 'path2','path3'],
        'AstroBookBank' : ['path1', 'path2','path3', 'path4'],
        'ASTROBookCart' : ['path1', 'path2','path3', 'path4','path5', 'path6', 'path7', 'path8', 'path9', 'path10'],
        'ASTROBookSearch' : ['path1', 'path2','path3', 'path4'],
        'Ordering' : ['path1', 'path2','path3', 'path4'],
        'NhincComponentInternalSubDiscovery' : ['path1', 'path2','path3', 'path4','path5', 'path6'],
        'NhincComponentInternalSubscriptionOrch' : ['path1', 'path2','path3', 'path4','path5']
        }

    bpelFiles = {
        'APP' : './BPEL/Realistic/APP.bpel',
        'Tuberculosis': './BPEL/Realistic/Tuberculosis.bpel',
        'GestationalDiabetes': './BPEL/Realistic/GestationalDiabetes.bpel',
        'CoronaryHeartDisease': './BPEL/Realistic/CoronaryHeartDisease.bpel',
        'NhincComponentAuditLog' : './BPEL/Dataset178/Cluster12+/NhincComponentAuditLog  pick.bpel',
        'AstroBookStore' : './BPEL/Dataset178/Cluster12+/AstroBookStore.bpel',
        'Synchronous' : './BPEL/Dataset178/Cluster5-8/Synchronous.bpel',
        'ClaimsProcess' : './BPEL/Dataset178/Cluster5-8/ClaimsProcess.bpel',
        'PartsDataService' : './BPEL/Dataset178/Cluster12+/PartsDataService.bpel',
        'LoanProcessWithSwimlanes' : './BPEL/Dataset178/Cluster1-2/LoanProcessWithSwimlanes.bpel',
        'BankTransferFlow2' : './BPEL/Dataset178/Cluster1-2/BankTransferFlow2.bpel',
        'Synchronous1' : './BPEL/Dataset178/Cluster1-2/Synchronous1.bpel',
        'SOAOrderBooking' : './BPEL/Dataset178/Cluster1-2/SOAOrderBooking.bpel',
        'ResilientFlow' :  './BPEL/Dataset178/Cluster1-2/ResilientFlow.bpel',
        'DslService' :  './BPEL/Dataset178/Cluster1-2/DslService.bpel',
        'EntityComponentInternalSubscribeOrch' :  './BPEL/Dataset178/Cluster1-2/EntityComponentInternalSubscribeOrch.bpel',
        'EntityComponentInternalUnsubscribeOrch' :  './BPEL/Dataset178/Cluster1-2/EntityComponentInternalUnsubscribeOrch.bpel',
        'LoanApprovalProcess' :  './BPEL/Dataset178/Cluster3-4/LoanApprovalProcess.bpel',
        'LoanApprovalProcess1' :  './BPEL/Dataset178/Cluster3-4/loanApprovalProcess1.bpel',
        'LoanProcess' :  './BPEL/Dataset178/Cluster3-4/LoanProcess.bpel',
        'NhinUnsubscribe' :  './BPEL/Dataset178/Cluster3-4/NhinUnsubscribe.bpel',
        'PrestamoRamas' :  './BPEL/Dataset178/Cluster3-4/prestamo-ramas.bpel',
        'QuoteProcess' :   './BPEL/Dataset178/Cluster3-4/QuoteProcess.bpel',
        'TaxiServiceProvider' : './BPEL/Dataset178/Cluster3-4/TaxiServiceProvider foreach wjile.bpel',
        'WorkoutProcess' : './BPEL/Dataset178/Cluster3-4/WorkoutProcess while pick.bpel',
        'AstroBookBank' : './BPEL/Dataset178/Cluster5-8/ASTROBookBank if.bpel',
        'ASTROBookCart' : './BPEL/Dataset178/Cluster5-8/ASTROBookCart_exe if.bpel',
        'ASTROBookSearch' : './BPEL/Dataset178/Cluster5-8/ASTROBookSearch_exe  if.bpel',
        'Ordering' : './BPEL/Dataset178/Cluster5-8/Ordering if exit.bpel',
        'NhincComponentInternalSubDiscovery' : './BPEL/Dataset178/Cluster5-8/NhincComponentInternalSubDiscovery201302Orch.bpel',
        'NhincComponentInternalSubscriptionOrch' : './BPEL/Dataset178/Cluster5-8/NhincComponentInternalSubscriptionOrch.bpel',

    }


    enhancedBpelFiles = {
        'APP' : './BPEL/Enhanced/EnhancedAPP.bpel',
        'Tuberculosis': './BPEL/Enhanced/EnhancedTuberculosis.bpel',
        'GestationalDiabetes': './BPEL/Enhanced/EnhancedGestationalDiabetes.bpel',
        'CoronaryHeartDisease': './BPEL/Enhanced/EnhancedCoronaryHeartDisease.bpel',
        'NhincComponentAuditLog' : './BPEL/Enhanced/Cluster12+/EnhancedNhincComponentAuditLog  pick.bpel',
        'AstroBookStore' : './BPEL/Enhanced/Cluster12+/EnhancedAstroBookStore.bpel',
        'Synchronous' : './BPEL/Enhanced/Cluster5-8/EnhancedSynchronous.bpel',
        'ClaimsProcess' : './BPEL/Enhanced/Cluster5-8/EnhancedClaimsProcess.bpel',
        'PartsDataService' : './BPEL/Enhanced/Cluster12+/EnhancedPartsDataService.bpel',
        'LoanProcessWithSwimlanes' : './BPEL/Enhanced/Cluster1-2/EnhancedLoanProcessWithSwimlanes.bpel',
        'BankTransferFlow2' : './BPEL/Enhanced/Cluster1-2/EnhancedBankTransferFlow2.bpel',
        'Synchronous1' : './BPEL/Enhanced/Cluster1-2/EnhancedSynchronous1.bpel',
        'SOAOrderBooking' : './BPEL/Enhanced/Cluster1-2/EnhancedSOAOrderBooking.bpel',
        'ResilientFlow' :  './BPEL/Enhanced/Cluster1-2/EnhancedResilientFlow.bpel',
        'DslService' :  './BPEL/Enhanced/Cluster1-2/EnhancedDslService.bpel',
        'EntityComponentInternalSubscribeOrch' :  './BPEL/Enhanced/Cluster1-2/EnhancedEntityComponentInternalSubscribeOrch.bpel',
        'EntityComponentInternalUnsubscribeOrch' :  './BPEL/Enhanced/Cluster1-2/EnhancedEntityComponentInternalUnsubscribeOrch.bpel',
        'LoanApprovalProcess' :  './BPEL/Enhanced/Cluster3-4/EnhancedLoanApprovalProcess.bpel',
        'LoanApprovalProcess1' :  './BPEL/Enhanced/Cluster3-4/EnhancedLoanApprovalProcess1.bpel',
        'LoanProcess' :  './BPEL/Enhanced/Cluster3-4/EnhancedLoanProcess.bpel',
        'NhinUnsubscribe' :  './BPEL/Enhanced/Cluster3-4/EnhancedNhinUnsubscribe.bpel',
        'PrestamoRamas' :  './BPEL/Enhanced/Cluster3-4/Enhancedprestamo-ramas.bpel',
        'QuoteProcess' :   './BPEL/Enhanced/Cluster3-4/EnhancedQuoteProcess.bpel',
        'TaxiServiceProvider' : './BPEL/Enhanced/Cluster3-4/EnhancedTaxiServiceProvider foreach wjile.bpel',
        'WorkoutProcess' : './BPEL/Enhanced/Cluster3-4/EnhancedWorkoutProcess while pick.bpel',
        'AstroBookBank' : './BPEL/Enhanced/Cluster5-8/EnhancedASTROBookBank if.bpel',
        'ASTROBookCart' : './BPEL/Enhanced/Cluster5-8/EnhancedASTROBookCart_exe if.bpel',
        'ASTROBookSearch' : './BPEL/Enhanced/Cluster5-8/EnhancedASTROBookSearch_exe  if.bpel',
        'Ordering' : './BPEL/Enhanced/Cluster5-8/EnhancedOrdering if exit.bpel',
        'NhincComponentInternalSubDiscovery' : './BPEL/Enhanced/Cluster5-8/EnhancedNhincComponentInternalSubDiscovery201302Orch.bpel',
        'NhincComponentInternalSubscriptionOrch' : './BPEL/Enhanced/Cluster5-8/EnhancedNhincComponentInternalSubscriptionOrch.bpel',

    }


    pathPrematResults = {
        'mean' : 0.0,
        'median' : 0.0,
        '80percentile' : 0.0,
        '20percentile' : 0.0,
        '50percentile' : 0.0,
        '70percentile' : 0.0
    }

    wastedResults = {
        'mean' : 0.0,
        'median' : 0.0,
        '80percentile' : 0.0,
        '20percentile' : 0.0,
        '50percentile' : 0.0,
        '70percentile' : 0.0
    }


    dynamicTotWorkflowComputationTime = 0

    def resetResults(self):
        for r in self.pathPrematResults:
            self.pathPrematResults[str(r)] = 0

        for r in self.wastedResults:
            self.wastedResults[str(r)] = 0


    def staticPrecompSimulation(self, userType, businessProcess, ppFilename, al, dataset):
        
        self.resetResults()
        print(colored("\nUserSimulator::staticPrecompSimulation - Start ", 'blue'), businessProcess)

        parser = BPELParser()
        framework = HDTFramework()

        bpelFile = self.bpelFiles[businessProcess]
        enhancedBPELFile = self.enhancedBpelFiles[businessProcess]

        # Create a copy of the bpel file and open it as a tree
        shutil.copyfile(bpelFile, enhancedBPELFile)

        if not os.path.exists("./results"):
            os.makedirs("./results")
        if not os.path.exists("./results/healthcare"):
            os.makedirs("./results/healthcare")
            os.makedirs("./results/healthcare/ec")
            os.makedirs("./results/healthcare/statistics")
        if not os.path.exists("./results/benchmark"):
            os.makedirs("./results/benchmark")
            os.makedirs("./results/benchmark/ec")
            os.makedirs("./results/benchmark/statistics")
       
        materialisedResults = open('./results/{0}/statistics/{1}_{2}_StaticExecution.txt'.format(dataset, businessProcess, al), "w")
        materialisedResults.write("Static execution of {}".format(businessProcess))
        materialisedResults.close()

        ecResults = open('./results/{0}/ec/{1}_{2}_StaticExecution.txt'.format(dataset, businessProcess, al), "w")
        materialisedResults = open('./results/{0}/statistics/{1}_{2}_StaticExecution.txt'.format(dataset, businessProcess, al), "a")

        tasks = parser.getTasks(bpelFile)

        # 1. Get the EC when AL = 1 to compute the threshold
        framework.initialECComputation(bpelFile, enhancedBPELFile, './Policy&PP/privacy_preference AL=1.json', ecResults, 5)
        materialise = Materialise()
        materialise.addECs(tasks, enhancedBPELFile, ecResults)
        thresholds = materialise.computeThresholds(ecResults)

        # 2. Get all paths and pre-compute the EC
        framework.initialECComputation(bpelFile, enhancedBPELFile, ppFilename, ecResults, userType)

        # For each path and for each threshold
        for path in self.workflows[businessProcess]:
            tasksInPath = parser.getTasksInPath(path, bpelFile)
            materialisedResults.write("\n\n\nCurrentPath: " + path + ': ' + str(tasksInPath))
            for th in thresholds:

                prematPathPercent = 0
                prematWastPercent = 0
                wastedTasks = 0

                materialisedResults.write("\n\nThreshold " + str(th) + ': ' + str(materialise.thresholds[th]))
                
                # print('UserSimulator::staticPrecompSimulation - total tasks in path:', len(tasksInPath))
                materialisedResults.write('\nTotal tasks in path: ' + str(len(tasksInPath)))
                # Get the number of tasks that have been precomputed (and wasted)
                prematInPath, prematInProcess, prematList = materialise.staticPrematerialisedTasks(tasks, tasksInPath, parser, enhancedBPELFile, th)

                for pt in prematList:
                    if not pt in tasksInPath:
                        wastedTasks += 1

                prematPathPercent = round(prematInPath/len(tasksInPath), 2)
                if wastedTasks > 0:
                    prematWastPercent = round(wastedTasks/prematInProcess,2)
                else:
                    prematWastPercent = 0

                materialisedResults.write('\nTasks (Views) prematerialised in the process: ' + str(prematInProcess) + ': ' + str(prematList))
                materialisedResults.write('\nTasks (Views) prematerialised in the path: ' + str(prematInPath) + '('+ str(prematPathPercent) + '%)')
                materialisedResults.write('\nWasted tasks (views): ' + str(wastedTasks) + '('+ str(prematWastPercent) + '%)')

                self.wastedResults[th] += prematWastPercent
                self.pathPrematResults[th] += prematPathPercent


        paths = len(self.workflows[businessProcess])
        materialisedResults.write('\n\nAverage results:')
        for th in thresholds:
            materialisedResults.write('\n\nThreshold ' + str(th) + ': ' + str(thresholds[th]))
            materialisedResults.write('\nAvg prematerialised tasks in path: ' + str(round(self.pathPrematResults[th]/paths, 2)))
            materialisedResults.write('\nAvg wasted tasks: ' + str(round(self.wastedResults[th]/paths,2)))

        materialisedResults.close()


    def dynamicPrecompSimulation(self, userType, businessProcess, ppFilename, al, dataset):
        self.resetResults()
        print(colored("\nUserSimulator::dynamicPrecompSimulation - Start ", 'blue'), businessProcess)

        parser = BPELParser()
        framework = HDTFramework()

        bpelFile = self.bpelFiles[businessProcess]
        enhancedBPELFile = self.enhancedBpelFiles[businessProcess]
        # Create a copy of the bpel file
        shutil.copyfile(bpelFile, enhancedBPELFile)

        if not os.path.exists("./results"):
            os.makedirs("./results")
        if not os.path.exists("./results/healthcare"):
            os.makedirs("./results/healthcare")
            os.makedirs("./results/healthcare/ec")
            os.makedirs("./results/healthcare/statistics")
        if not os.path.exists("./results/benchmark"):
            os.makedirs("./results/benchmark")
            os.makedirs("./results/benchmark/ec")
            os.makedirs("./results/benchmark/statistics")

        materialisedResults = open('./results/{0}/ec/{1}_{2}_StaticExecution.txt'.format(dataset, businessProcess, al), "w")
        materialisedResults.write("Static execution of {}".format(businessProcess))
        materialisedResults.close()

        ecResults = open('./results/{0}/ec/{1}_{2}_StaticExecution.txt'.format(dataset, businessProcess, al), "w")
        materialisedResults = open('./results/{0}/ec/{1}_{2}_StaticExecution.txt'.format(dataset, businessProcess, al), "a")

        tasks = parser.getTasks(bpelFile)

        # 1. Get the EC when AL = 1 to compute the threshold
        framework.initialECComputation(bpelFile, enhancedBPELFile, './Policy&PP/privacy_preference AL=1.json', ecResults, 5)
        materialise = Materialise()
        materialise.addECs(tasks, enhancedBPELFile, ecResults)
        thresholds = materialise.computeThresholds(ecResults)


        # 2. For each path and for each threshold
        for path in self.workflows[businessProcess]:
            ecResults.write("\n\n\nCurrent Path: " + str(path))
            tasks = parser.getTasks(bpelFile)
            tasksInPath = parser.getTasksInPath(path, bpelFile)
            materialisedResults.write("\n\n\nCurrentPath: " + path + ':' + str(tasksInPath))
            print("\n", businessProcess, "- currentPath: " + path + ':' + str(tasksInPath))

            firstTask = tasksInPath[0]
            print("First task of path", path, ":", firstTask)
            for th in thresholds:
                print("Threshold: " + str(th))
                materialisedResults.write("\n\nThreshold " + str(th) + ": " + str(thresholds[th]))
                # print('UserSimulator::staticPrecompSimulation - total tasks in path:', len(tasksInPath))
                materialisedResults.write('\nTotal tasks in path: ' + str(len(tasksInPath)))

                prematList = []
                prematTasksPath = 0
                prematTasksProcess = 0
                wastedTasks = 0

                traversedTasks = []

                for currentTask in tasksInPath:
                    print('\nUserSimulator::dynamicPrecompSimulation - current task: ', currentTask)
                    taskPosition = tasksInPath.index(currentTask)
                    ecResults.write("\n\nCurrent Task: " + str(currentTask))
                    materialisedResults.write("\n\nCurrent Task: " + str(currentTask))
                    traversedTasks.append(currentTask)
                    # print('UserSimulator::dynamicPrecompSimulation - position of', taskId, 'in', path, ":", taskPosition)
                    # If it is the first task, behave as the static evaluation:
                    if taskPosition == 0: # It is the initial task, do as the static precomputator
                        framework.initialECComputation(bpelFile, enhancedBPELFile, ppFilename, ecResults, userType)
                    # evaluate again the EC for each task
                    else:
                        framework.updateEC(bpelFile, enhancedBPELFile, currentTask, traversedTasks, ppFilename, ecResults)
                    # print('UserSimulator::dynamicPrecompSimulation - (so far) traversed tasks:', traversedTasks)

                    newPrecomputedTasks, prematInPath, prematInProcess = materialise.dynamicPrematerialisedTasks(parser, tasks, enhancedBPELFile, prematList, th, tasksInPath)

                    for nt in newPrecomputedTasks:
                        prematList.append(nt)

                    print(currentTask, '- precomputedTasksList: ', prematList)
                    prematTasksPath += prematInPath
                    prematTasksProcess += prematInProcess

                    materialisedResults.write('\nNew prematerialised tasks: ' + str(newPrecomputedTasks))

                for pt in prematList:
                    if not pt in tasksInPath:
                        wastedTasks += 1

                prematPathPercent = round(prematTasksPath/len(tasksInPath), 2)
                if wastedTasks > 0:
                    prematWastPercent = round(wastedTasks/prematTasksProcess, 2)
                else:
                    prematWastPercent = 0

                materialisedResults.write('\nTasks (Views) prematerialised in the process: ' + str(prematTasksProcess) + ': ' + str(prematList))
                materialisedResults.write('\nTasks (Views) prematerialised in the path: ' + str(prematTasksPath) + '('+ str(prematPathPercent) + '%)')
                materialisedResults.write('\nWasted tasks (views): ' + str(wastedTasks) + '('+ str(prematWastPercent) + '%)')

                self.wastedResults[th] += prematWastPercent
                self.pathPrematResults[th] += prematPathPercent

        paths = len(self.workflows[businessProcess])
        materialisedResults.write('\n\nAverage results:')
        for th in thresholds:
            materialisedResults.write('\n\nThreshold ' + str(th) + ': ' + str(thresholds[th]))
            materialisedResults.write('\nAvg prematerialised tasks in path: ' + str(round(self.pathPrematResults[th]/paths, 2)))
            materialisedResults.write('\nAvg wasted tasks: ' + str(round(self.wastedResults[th]/paths,2)))

        # print('\n')

        materialisedResults.close()

    def writeDynamicResults(self, businessProcess, dynamicSheet, userType, dynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn):
        materialise = Materialise()
        thresholds = materialise.getThreshold()
        
        dynamicRow += 1

        if userType == 1: 
            dynamicSheet.write(dynamicRow, processColumn, 'AL = [0.83 - 1]')
        elif userType == 2:
            dynamicSheet.write(dynamicRow, processColumn, 'AL = [0.5 - 0.82]')
        elif userType == 3:
            dynamicSheet.write(dynamicRow, processColumn, 'AL = [0.18 - 0.49]')
        elif userType == 4:
            dynamicSheet.write(dynamicRow, processColumn, 'AL = [0 - 0.17]')

        for th in thresholds:
            dynamicRow += 1
            dynamicSheet.write(dynamicRow, processColumn, th)
            dynamicSheet.write(dynamicRow, thresholdColumn, (round(thresholds[th],2)))
            dynamicSheet.write(dynamicRow, matInPathColumn, (round(simulator.pathPrematResults[th]/len(simulator.workflows[businessProcess]), 2)))
            dynamicSheet.write(dynamicRow, wastedColumn, (round(simulator.wastedResults[th]/len(simulator.workflows[businessProcess]), 2)))
        return dynamicRow



    def writeStaticResults(self, businessProcess, staticSheet, userType, staticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn):
        materialise = Materialise()
        thresholds = materialise.getThreshold()
        
        staticRow += 1

        if userType == 1: 
            staticSheet.write(staticRow, processColumn, 'AL = [0.83 - 1]')
        elif userType == 2:
            staticSheet.write(staticRow, processColumn, 'AL = [0.5 - 0.82]')
        elif userType == 3:
            staticSheet.write(staticRow, processColumn, 'AL = [0.18 - 0.49]')
        elif userType == 4:
            staticSheet.write(staticRow, processColumn, 'AL = [0 - 0.17]')

        for th in thresholds:
            staticRow += 1
            staticSheet.write(staticRow, processColumn, th)
            staticSheet.write(staticRow, thresholdColumn, (round(thresholds[th],2)))
            staticSheet.write(staticRow, matInPathColumn, (round(simulator.pathPrematResults[th]/len(simulator.workflows[businessProcess]), 2)))
            staticSheet.write(staticRow, wastedColumn, (round(simulator.wastedResults[th]/len(simulator.workflows[businessProcess]), 2)))
        return staticRow



if __name__ == "__main__":
    simulator = UserSimulator()
    materialise = Materialise()

    ##############
    # HEALTHCARE #
    ##############
    processColumn = 1
    thresholdColumn = 2
    matInPathColumn = 3
    wastedColumn = 4

    healthcareStaticRow = 1
    healthcareDynamicRow = 1

    resultFile = xlsxwriter.Workbook('./results_healthcare.xlsx')
    healthcareStaticSheet = resultFile.add_worksheet('HealthcareStatic')
    healthcareDynamicSheet = resultFile.add_worksheet('HealthcareDynamic')

    healthcareStaticSheet.write(healthcareStaticRow, matInPathColumn, 'PrecompInPath')
    healthcareStaticSheet.write(healthcareStaticRow, wastedColumn, 'Wasted')
    healthcareStaticRow += 1

    healthcareDynamicSheet.write(healthcareDynamicRow, matInPathColumn, 'PrecompInPath')
    healthcareDynamicSheet.write(healthcareDynamicRow, wastedColumn, 'Wasted')
    healthcareDynamicRow += 1


    # APP
    #####
   
    healthcareStaticSheet.write(healthcareStaticRow, processColumn, 'APP')
   
    simulator.staticPrecompSimulation(1, "APP", './Policy&PP/privacy_preference AL=1.json', 'type1', "healthcare")
    thresholds = materialise.getThreshold()
    healthcareStaticRow = simulator.writeStaticResults('APP', healthcareStaticSheet, 1, healthcareStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(2, "APP", './Policy&PP/privacy_preference AL=0.9.json', 'type2', "healthcare")
    # healthcareStaticRow = simulator.writeStaticResults('APP', healthcareStaticSheet, 2, healthcareStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(3, "APP", './Policy&PP/privacy_preference AL=0.8.json', 'type3', "healthcare")
    # healthcareStaticRow = simulator.writeStaticResults('APP', healthcareStaticSheet, 3, healthcareStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(4, "APP", './Policy&PP/privacy_preference AL=0.8.json', 'type4', "healthcare")
    # healthcareStaticRow = simulator.writeStaticResults('APP', healthcareStaticSheet, 4, healthcareStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)

    healthcareDynamicSheet.write(healthcareDynamicRow, processColumn, 'APP')
    
    simulator.dynamicPrecompSimulation(1, 'APP', './Policy&PP/privacy_preference AL=1.json', 'type1', "healthcare")
    healthcareDynamicRow = simulator.writeDynamicResults('APP', healthcareDynamicSheet, 1, healthcareDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(2, 'APP', './Policy&PP/privacy_preference AL=0.9.json', 'type2', "healthcare")
    # healthcareDynamicRow = simulator.writeDynamicResults('APP', healthcareDynamicSheet, 2, healthcareDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(3, 'APP', './Policy&PP/privacy_preference AL=0.8.json', 'type3', "healthcare")
    # healthcareDynamicRow = simulator.writeDynamicResults('APP', healthcareDynamicSheet, 3, healthcareDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(4, 'APP', './Policy&PP/privacy_preference AL=0.8.json', 'type4', "healthcare")
    # healthcareDynamicRow = simulator.writeDynamicResults('APP', healthcareDynamicSheet, 4, healthcareDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)

    # healthcareDynamicRow += 2
    # healthcareStaticRow += 2

    # # Tuberculosis
    # #############

    # thresholds = materialise.getThreshold()
    # healthcareStaticSheet.write(healthcareStaticRow, processColumn, 'Tub')

    # simulator.staticPrecompSimulation(1, "Tuberculosis", './Policy&PP/privacy_preference AL=1.json', 'type1', "healthcare")
    # thresholds = materialise.getThreshold()
    # healthcareStaticRow = simulator.writeStaticResults("Tuberculosis", healthcareStaticSheet, 1, healthcareStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(2, "Tuberculosis", './Policy&PP/privacy_preference AL=0.9.json', 'type2', "healthcare")
    # healthcareStaticRow = simulator.writeStaticResults("Tuberculosis", healthcareStaticSheet, 2, healthcareStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(3, "Tuberculosis", './Policy&PP/privacy_preference AL=0.8.json', 'type3', "healthcare")
    # healthcareStaticRow = simulator.writeStaticResults("Tuberculosis", healthcareStaticSheet, 3, healthcareStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(4, "Tuberculosis", './Policy&PP/privacy_preference AL=0.8.json', 'type4', "healthcare")
    # healthcareStaticRow = simulator.writeStaticResults("Tuberculosis", healthcareStaticSheet, 4, healthcareStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)

    # healthcareDynamicSheet.write(healthcareDynamicRow, processColumn, 'Tub')
    # simulator.dynamicPrecompSimulation(1, "Tuberculosis", './Policy&PP/privacy_preference AL=1.json', 'type1', "healthcare")
    # healthcareDynamicRow = simulator.writeDynamicResults("Tuberculosis", healthcareDynamicSheet, 1, healthcareDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(2, "Tuberculosis", './Policy&PP/privacy_preference AL=0.9.json', 'type2', "healthcare")
    # healthcareDynamicRow = simulator.writeDynamicResults("Tuberculosis", healthcareDynamicSheet, 2, healthcareDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(3, "Tuberculosis", './Policy&PP/privacy_preference AL=0.8.json', 'type3', "healthcare")
    # healthcareDynamicRow = simulator.writeDynamicResults("Tuberculosis", healthcareDynamicSheet, 3, healthcareDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(4, "Tuberculosis", './Policy&PP/privacy_preference AL=0.8.json', 'type4', "healthcare")
    # healthcareDynamicRow = simulator.writeDynamicResults("Tuberculosis", healthcareDynamicSheet, 4, healthcareDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)

    # healthcareDynamicRow += 2
    # healthcareStaticRow += 2

    # # # # Gestional Diabetes
    # thresholds = materialise.getThreshold()
    # healthcareStaticSheet.write(healthcareStaticRow, processColumn, 'GD')

    # simulator.staticPrecompSimulation(1, "GestationalDiabetes", './Policy&PP/privacy_preference AL=1.json', 'type1', 'healthcare')
    # thresholds = materialise.getThreshold()
    # healthcareStaticRow = simulator.writeStaticResults("GestationalDiabetes", healthcareStaticSheet, 1, healthcareStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(2, "GestationalDiabetes", './Policy&PP/privacy_preference AL=0.9.json', 'type2', 'healthcare')
    # healthcareStaticRow = simulator.writeStaticResults("GestationalDiabetes", healthcareStaticSheet, 2, healthcareStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(3, "GestationalDiabetes", './Policy&PP/privacy_preference AL=0.8.json', 'type3', 'healthcare')
    # healthcareStaticRow = simulator.writeStaticResults("GestationalDiabetes", healthcareStaticSheet, 3, healthcareStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(4, "GestationalDiabetes", './Policy&PP/privacy_preference AL=0.8.json', 'type4', 'healthcare')
    # healthcareStaticRow = simulator.writeStaticResults("GestationalDiabetes", healthcareStaticSheet, 4, healthcareStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)

    # healthcareDynamicSheet.write(healthcareDynamicRow, processColumn, 'GD')
    # simulator.dynamicPrecompSimulation(1, "GestationalDiabetes", './Policy&PP/privacy_preference AL=1.json', 'type1', 'healthcare')
    # healthcareDynamicRow = simulator.writeDynamicResults("GestationalDiabetes", healthcareDynamicSheet, 1, healthcareDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(2, "GestationalDiabetes", './Policy&PP/privacy_preference AL=0.9.json', 'type2', 'healthcare')
    # healthcareDynamicRow = simulator.writeDynamicResults("GestationalDiabetes", healthcareDynamicSheet, 2, healthcareDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(3, "GestationalDiabetes", './Policy&PP/privacy_preference AL=0.8.json', 'type3', 'healthcare')
    # healthcareDynamicRow = simulator.writeDynamicResults("GestationalDiabetes", healthcareDynamicSheet, 3, healthcareDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(4, "GestationalDiabetes", './Policy&PP/privacy_preference AL=0.8.json', 'type4', 'healthcare')
    # healthcareDynamicRow = simulator.writeDynamicResults("GestationalDiabetes", healthcareDynamicSheet, 4, healthcareDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    
    # healthcareDynamicRow += 2
    # healthcareStaticRow += 2

    # # # Coronary Heart Disease
    # thresholds = materialise.getThreshold()
    # healthcareStaticSheet.write(healthcareStaticRow, processColumn, 'CHD')

    # simulator.staticPrecompSimulation(1, "CoronaryHeartDisease", './Policy&PP/privacy_preference AL=1.json', 'type1', 'healthcare')
    # thresholds = materialise.getThreshold()
    # healthcareStaticRow = simulator.writeStaticResults("CoronaryHeartDisease", healthcareStaticSheet, 1, healthcareStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(2, "CoronaryHeartDisease", './Policy&PP/privacy_preference AL=0.9.json', 'type2', 'healthcare')
    # healthcareStaticRow = simulator.writeStaticResults("CoronaryHeartDisease", healthcareStaticSheet, 2, healthcareStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(3, "CoronaryHeartDisease", './Policy&PP/privacy_preference AL=0.8.json', 'type3', 'healthcare')
    # healthcareStaticRow = simulator.writeStaticResults("CoronaryHeartDisease", healthcareStaticSheet, 3, healthcareStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(4, "CoronaryHeartDisease", './Policy&PP/privacy_preference AL=0.8.json', 'type4', 'healthcare')
    # healthcareStaticRow = simulator.writeStaticResults("CoronaryHeartDisease", healthcareStaticSheet, 4, healthcareStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)

    # healthcareDynamicSheet.write(healthcareDynamicRow, processColumn, 'CHD')
    # simulator.dynamicPrecompSimulation(1, "CoronaryHeartDisease", './Policy&PP/privacy_preference AL=1.json', 'type1', 'healthcare')
    # healthcareDynamicRow = simulator.writeDynamicResults("CoronaryHeartDisease", healthcareDynamicSheet, 1, healthcareDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(2, "CoronaryHeartDisease", './Policy&PP/privacy_preference AL=0.9.json', 'type2', 'healthcare')
    # healthcareDynamicRow = simulator.writeDynamicResults("CoronaryHeartDisease", healthcareDynamicSheet, 2, healthcareDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(3, "CoronaryHeartDisease", './Policy&PP/privacy_preference AL=0.8.json', 'type3', 'healthcare')
    # healthcareDynamicRow = simulator.writeDynamicResults("CoronaryHeartDisease", healthcareDynamicSheet, 3, healthcareDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(4, "CoronaryHeartDisease", './Policy&PP/privacy_preference AL=0.8.json', 'type4', 'healthcare')
    # healthcareDynamicRow = simulator.writeDynamicResults("CoronaryHeartDisease", healthcareDynamicSheet, 4, healthcareDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)

    resultFile.close()

    ###############
    # DATASET 178 #
    ###############

    resultFile = xlsxwriter.Workbook('./results_benchmark.xlsx')
    benchmarkStaticSheet = resultFile.add_worksheet('BenchmarkStatic')
    benchmarkDynamicSheet = resultFile.add_worksheet('BenchmarkDynamic')

    #############
    # Cluster 1 #
    #############
    benchmarkStaticSheet.write(0, 1, 'Cluster1')
    benchmarkDynamicSheet.write(0, 1, 'Cluster1')

    processColumn = 1
    thresholdColumn = 2
    matInPathColumn = 3
    wastedColumn = 4

    benchmarkStaticRow = 1
    benchmarkDynamicRow = 1

    benchmarkStaticSheet.write(benchmarkStaticRow, matInPathColumn, 'PrecompInPath')
    benchmarkStaticSheet.write(benchmarkStaticRow, wastedColumn, 'Wasted')
    benchmarkStaticRow += 1
    
    benchmarkDynamicSheet.write(benchmarkDynamicRow, matInPathColumn, 'PrecompInPath')
    benchmarkDynamicSheet.write(benchmarkDynamicRow, wastedColumn, 'Wasted')
    benchmarkDynamicRow += 1

    # # BankTransferFlow2
    thresholds = materialise.getThreshold()
    benchmarkStaticSheet.write(benchmarkStaticRow, processColumn, 'BankTransferFlow2')

    simulator.staticPrecompSimulation(1, "BankTransferFlow2", './Policy&PP/privacy_preference AL=1.json', 'type1', 'benchmark')
    thresholds = materialise.getThreshold()
    benchmarkStaticRow = simulator.writeStaticResults("BankTransferFlow2", benchmarkStaticSheet, 1, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(2, "BankTransferFlow2", './Policy&PP/privacy_preference AL=0.9.json', 'type2', 'benchmark')
    # benchmarkStaticRow = simulator.writeStaticResults("BankTransferFlow2", benchmarkStaticSheet, 2, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(3, "BankTransferFlow2", './Policy&PP/privacy_preference AL=0.8.json', 'type3', 'benchmark')
    # benchmarkStaticRow = simulator.writeStaticResults("BankTransferFlow2", benchmarkStaticSheet, 3, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(4, "BankTransferFlow2", './Policy&PP/privacy_preference AL=0.8.json', 'type4', 'benchmark')
    # benchmarkStaticRow = simulator.writeStaticResults("BankTransferFlow2", benchmarkStaticSheet, 4, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)

    benchmarkDynamicSheet.write(benchmarkDynamicRow, processColumn, 'BankTransferFlow2')
    simulator.dynamicPrecompSimulation(1, "BankTransferFlow2", './Policy&PP/privacy_preference AL=1.json', 'type1', 'benchmark')
    benchmarkDynamicRow = simulator.writeDynamicResults("BankTransferFlow2", benchmarkDynamicSheet, 1, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(2, "BankTransferFlow2", './Policy&PP/privacy_preference AL=0.9.json', 'type2', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("BankTransferFlow2", benchmarkDynamicSheet, 2, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(3, "BankTransferFlow2", './Policy&PP/privacy_preference AL=0.8.json', 'type3', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("BankTransferFlow2", benchmarkDynamicSheet, 3, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(4, "BankTransferFlow2", './Policy&PP/privacy_preference AL=0.8.json', 'type4', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("BankTransferFlow2", benchmarkDynamicSheet, 4, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    
    # benchmarkStaticRow += 2
    # benchmarkDynamicRow += 2

    # # DslService
    # thresholds = materialise.getThreshold()
    # benchmarkStaticSheet.write(benchmarkStaticRow, processColumn, 'DslService')

    # simulator.staticPrecompSimulation(1, "DslService", './Policy&PP/privacy_preference AL=1.json', 'type1', 'benchmark')
    # thresholds = materialise.getThreshold()
    # benchmarkStaticRow = simulator.writeStaticResults("DslService", benchmarkStaticSheet, 1, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(2, "DslService", './Policy&PP/privacy_preference AL=0.9.json', 'type2', 'benchmark')
    # benchmarkStaticRow = simulator.writeStaticResults("DslService", benchmarkStaticSheet, 2, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(3, "DslService", './Policy&PP/privacy_preference AL=0.8.json', 'type3', 'benchmark')
    # benchmarkStaticRow = simulator.writeStaticResults("DslService", benchmarkStaticSheet, 3, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(4, "DslService", './Policy&PP/privacy_preference AL=0.8.json', 'type4', 'benchmark')
    # benchmarkStaticRow = simulator.writeStaticResults("DslService", benchmarkStaticSheet, 4, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)

    # benchmarkDynamicSheet.write(benchmarkDynamicRow, processColumn, 'DslService')
    # simulator.dynamicPrecompSimulation(1, "DslService", './Policy&PP/privacy_preference AL=1.json', 'type1', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("DslService", benchmarkDynamicSheet, 1, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(2, "DslService", './Policy&PP/privacy_preference AL=0.9.json', 'type2', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("DslService", benchmarkDynamicSheet, 2, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(3, "DslService", './Policy&PP/privacy_preference AL=0.8.json', 'type3', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("DslService", benchmarkDynamicSheet, 3, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(4, "DslService", './Policy&PP/privacy_preference AL=0.8.json', 'type4', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("DslService", benchmarkDynamicSheet, 4, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)

    # benchmarkStaticRow += 2
    # benchmarkDynamicRow += 2

    # # LoanProcessWithSwimlanes
    # thresholds = materialise.getThreshold()
    # benchmarkStaticSheet.write(benchmarkStaticRow, processColumn, 'LoanProcessWithSwimlanes')

    # simulator.staticPrecompSimulation(1, "LoanProcessWithSwimlanes", './Policy&PP/privacy_preference AL=1.json', 'type1', 'benchmark')
    # thresholds = materialise.getThreshold()
    # benchmarkStaticRow = simulator.writeStaticResults("LoanProcessWithSwimlanes", benchmarkStaticSheet, 1, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(2, "LoanProcessWithSwimlanes", './Policy&PP/privacy_preference AL=0.9.json', 'type2', 'benchmark')
    # benchmarkStaticRow = simulator.writeStaticResults("LoanProcessWithSwimlanes", benchmarkStaticSheet, 2, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(3, "LoanProcessWithSwimlanes", './Policy&PP/privacy_preference AL=0.8.json', 'type3', 'benchmark')
    # benchmarkStaticRow = simulator.writeStaticResults("LoanProcessWithSwimlanes", benchmarkStaticSheet, 3, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(4, "LoanProcessWithSwimlanes", './Policy&PP/privacy_preference AL=0.8.json', 'type4', 'benchmark')
    # benchmarkStaticRow = simulator.writeStaticResults("LoanProcessWithSwimlanes", benchmarkStaticSheet, 4, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)

    # benchmarkDynamicSheet.write(benchmarkDynamicRow, processColumn, 'LoanProcessWithSwimlanes')
    # simulator.dynamicPrecompSimulation(1, "LoanProcessWithSwimlanes", './Policy&PP/privacy_preference AL=1.json', 'type1', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("LoanProcessWithSwimlanes", benchmarkDynamicSheet, 1, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(2, "LoanProcessWithSwimlanes", './Policy&PP/privacy_preference AL=0.9.json', 'type2', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("LoanProcessWithSwimlanes", benchmarkDynamicSheet, 2, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(3, "LoanProcessWithSwimlanes", './Policy&PP/privacy_preference AL=0.8.json', 'type3', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("LoanProcessWithSwimlanes", benchmarkDynamicSheet, 3, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(4, "LoanProcessWithSwimlanes", './Policy&PP/privacy_preference AL=0.8.json', 'type4', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("LoanProcessWithSwimlanes", benchmarkDynamicSheet, 4, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)

    # benchmarkStaticRow += 2
    # benchmarkDynamicRow += 2

    # # TaxiServiceProvider
    # thresholds = materialise.getThreshold()
    # benchmarkStaticSheet.write(benchmarkStaticRow, processColumn, 'TaxyServiceProvider')

    # simulator.staticPrecompSimulation(1, "TaxiServiceProvider", './Policy&PP/privacy_preference AL=1.json', 'type1', 'benchmark')
    # thresholds = materialise.getThreshold()
    # benchmarkStaticRow = simulator.writeStaticResults("TaxiServiceProvider", benchmarkStaticSheet, 1, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(2, "TaxiServiceProvider", './Policy&PP/privacy_preference AL=0.9.json', 'type2', 'benchmark')
    # benchmarkStaticRow = simulator.writeStaticResults("TaxiServiceProvider", benchmarkStaticSheet, 2, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(3, "TaxiServiceProvider", './Policy&PP/privacy_preference AL=0.8.json', 'type3', 'benchmark')
    # benchmarkStaticRow = simulator.writeStaticResults("TaxiServiceProvider", benchmarkStaticSheet, 3, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(4, "TaxiServiceProvider", './Policy&PP/privacy_preference AL=0.8.json', 'type4', 'benchmark')
    # benchmarkStaticRow = simulator.writeStaticResults("TaxiServiceProvider", benchmarkStaticSheet, 4, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)

    # benchmarkDynamicSheet.write(benchmarkDynamicRow, processColumn, 'TaxiServiceProvider')
    # simulator.dynamicPrecompSimulation(1, "TaxiServiceProvider", './Policy&PP/privacy_preference AL=1.json', 'type1', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("TaxiServiceProvider", benchmarkDynamicSheet, 1, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(2, "TaxiServiceProvider", './Policy&PP/privacy_preference AL=0.9.json', 'type2', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("TaxiServiceProvider", benchmarkDynamicSheet, 2, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(3, "TaxiServiceProvider", './Policy&PP/privacy_preference AL=0.8.json', 'type3', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("TaxiServiceProvider", benchmarkDynamicSheet, 3, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(4, "TaxiServiceProvider", './Policy&PP/privacy_preference AL=0.8.json', 'type4', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("TaxiServiceProvider", benchmarkDynamicSheet, 4, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)

    # benchmarkStaticRow += 2
    # benchmarkDynamicRow += 2

    #############
    # Cluster 2 #
    #############

    # benchmarkStaticSheet.write(0, 6, 'Cluster2')
    # benchmarkDynamicSheet.write(0, 6, 'Cluster2')

    # processColumn = 6
    # thresholdColumn = 7
    # matInPathColumn = 8
    # wastedColumn = 9

    # benchmarkStaticRow = 1
    # benchmarkDynamicRow = 1

    # benchmarkStaticSheet.write(benchmarkStaticRow, matInPathColumn, 'PrecompInPath')
    # benchmarkStaticSheet.write(benchmarkStaticRow, wastedColumn, 'Wasted')
    # benchmarkStaticRow += 1

    # benchmarkDynamicSheet.write(benchmarkDynamicRow, matInPathColumn, 'PrecompInPath')
    # benchmarkDynamicSheet.write(benchmarkDynamicRow, wastedColumn, 'Wasted')
    # benchmarkDynamicRow += 1

    # # EntityComponentInternalSubscribeOrch
    # thresholds = materialise.getThreshold()
    # benchmarkStaticSheet.write(benchmarkStaticRow, processColumn, 'EntityComponentInternalSubscribeOrch')

    # simulator.staticPrecompSimulation(1, "EntityComponentInternalSubscribeOrch", './Policy&PP/privacy_preference AL=1.json', 'type1', 'benchmark')
    # thresholds = materialise.getThreshold()
    # benchmarkStaticRow = simulator.writeStaticResults("EntityComponentInternalSubscribeOrch", benchmarkStaticSheet, 1, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(2, "EntityComponentInternalSubscribeOrch", './Policy&PP/privacy_preference AL=0.9.json', 'type2', 'benchmark')
    # benchmarkStaticRow = simulator.writeStaticResults("EntityComponentInternalSubscribeOrch", benchmarkStaticSheet, 2, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(3, "EntityComponentInternalSubscribeOrch", './Policy&PP/privacy_preference AL=0.8.json', 'type3', 'benchmark')
    # benchmarkStaticRow = simulator.writeStaticResults("EntityComponentInternalSubscribeOrch", benchmarkStaticSheet, 3, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(4, "EntityComponentInternalSubscribeOrch", './Policy&PP/privacy_preference AL=0.8.json', 'type4', 'benchmark')
    # benchmarkStaticRow = simulator.writeStaticResults("EntityComponentInternalSubscribeOrch", benchmarkStaticSheet, 4, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)

    # benchmarkDynamicSheet.write(benchmarkDynamicRow, processColumn, 'EntityComponentInternalSubscribeOrch')
    # simulator.dynamicPrecompSimulation(1, "EntityComponentInternalSubscribeOrch", './Policy&PP/privacy_preference AL=1.json', 'type1', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("EntityComponentInternalSubscribeOrch", benchmarkDynamicSheet, 1, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(2, "EntityComponentInternalSubscribeOrch", './Policy&PP/privacy_preference AL=0.9.json', 'type2', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("EntityComponentInternalSubscribeOrch", benchmarkDynamicSheet, 2, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(3, "EntityComponentInternalSubscribeOrch", './Policy&PP/privacy_preference AL=0.8.json', 'type3', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("EntityComponentInternalSubscribeOrch", benchmarkDynamicSheet, 3, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(4, "EntityComponentInternalSubscribeOrch", './Policy&PP/privacy_preference AL=0.8.json', 'type4', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("EntityComponentInternalSubscribeOrch", benchmarkDynamicSheet, 4, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn) 

    # benchmarkStaticRow += 2
    # benchmarkDynamicRow += 2

    # # EntityComponentInternalUnsubscribeOrch
    # thresholds = materialise.getThreshold()
    # benchmarkStaticSheet.write(benchmarkStaticRow, processColumn, 'EntityComponentInternalUnsubscribeOrch')

    # simulator.staticPrecompSimulation(1, "EntityComponentInternalUnsubscribeOrch", './Policy&PP/privacy_preference AL=1.json', 'type1', 'benchmark')
    # thresholds = materialise.getThreshold()
    # benchmarkStaticRow = simulator.writeStaticResults("EntityComponentInternalUnsubscribeOrch", benchmarkStaticSheet, 1, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(2, "EntityComponentInternalUnsubscribeOrch", './Policy&PP/privacy_preference AL=0.9.json', 'type2', 'benchmark')
    # benchmarkStaticRow = simulator.writeStaticResults("EntityComponentInternalUnsubscribeOrch", benchmarkStaticSheet, 2, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(3, "EntityComponentInternalUnsubscribeOrch", './Policy&PP/privacy_preference AL=0.8.json', 'type3', 'benchmark')
    # benchmarkStaticRow = simulator.writeStaticResults("EntityComponentInternalUnsubscribeOrch", benchmarkStaticSheet, 3, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(4, "EntityComponentInternalUnsubscribeOrch", './Policy&PP/privacy_preference AL=0.8.json', 'type4', 'benchmark')
    # benchmarkStaticRow = simulator.writeStaticResults("EntityComponentInternalUnsubscribeOrch", benchmarkStaticSheet, 4, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)

    # benchmarkDynamicSheet.write(benchmarkDynamicRow, processColumn, 'EntityComponentInternalUnsubscribeOrch')
    # simulator.dynamicPrecompSimulation(1, "EntityComponentInternalUnsubscribeOrch", './Policy&PP/privacy_preference AL=1.json', 'type1', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("EntityComponentInternalUnsubscribeOrch", benchmarkDynamicSheet, 1, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(2, "EntityComponentInternalUnsubscribeOrch", './Policy&PP/privacy_preference AL=0.9.json', 'type2', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("EntityComponentInternalUnsubscribeOrch", benchmarkDynamicSheet, 2, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(3, "EntityComponentInternalUnsubscribeOrch", './Policy&PP/privacy_preference AL=0.8.json', 'type3', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("EntityComponentInternalUnsubscribeOrch", benchmarkDynamicSheet, 3, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(4, "EntityComponentInternalUnsubscribeOrch", './Policy&PP/privacy_preference AL=0.8.json', 'type4', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("EntityComponentInternalUnsubscribeOrch", benchmarkDynamicSheet, 4, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)

    # benchmarkStaticRow += 2
    # benchmarkDynamicRow += 2

    # # Synchronous1
    # thresholds = materialise.getThreshold()
    # benchmarkStaticSheet.write(benchmarkStaticRow, processColumn, 'Synchronous1')
    
    # simulator.staticPrecompSimulation(1, "Synchronous1", './Policy&PP/privacy_preference AL=1.json', 'type1', 'benchmark')
    # thresholds = materialise.getThreshold()
    # benchmarkStaticRow = simulator.writeStaticResults("Synchronous1", benchmarkStaticSheet, 1, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(2, "Synchronous1", './Policy&PP/privacy_preference AL=0.9.json', 'type2', 'benchmark')
    # benchmarkStaticRow = simulator.writeStaticResults("Synchronous1", benchmarkStaticSheet, 2, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(3, "Synchronous1", './Policy&PP/privacy_preference AL=0.8.json', 'type3', 'benchmark')
    # benchmarkStaticRow = simulator.writeStaticResults("Synchronous1", benchmarkStaticSheet, 3, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(4, "Synchronous1", './Policy&PP/privacy_preference AL=0.8.json', 'type4', 'benchmark')
    # benchmarkStaticRow = simulator.writeStaticResults("Synchronous1", benchmarkStaticSheet, 4, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)

    # benchmarkDynamicSheet.write(benchmarkDynamicRow, processColumn, 'Synchronous1')
    # simulator.dynamicPrecompSimulation(1, "Synchronous1", './Policy&PP/privacy_preference AL=1.json', 'type1', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("Synchronous1", benchmarkDynamicSheet, 1, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(2, "Synchronous1", './Policy&PP/privacy_preference AL=0.9.json', 'type2', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("Synchronous1", benchmarkDynamicSheet, 2, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(3, "Synchronous1", './Policy&PP/privacy_preference AL=0.8.json', 'type3', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("Synchronous1", benchmarkDynamicSheet, 3, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(4, "Synchronous1", './Policy&PP/privacy_preference AL=0.8.json', 'type4', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("Synchronous1", benchmarkDynamicSheet, 4, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)

    # ############
    # Cluster 3 #
    # ############

    # benchmarkStaticSheet.write(0, 11, 'Cluster3')
    # benchmarkDynamicSheet.write(0, 11, 'Cluster3')

    # processColumn = 11
    # thresholdColumn = 12
    # matInPathColumn = 13
    # wastedColumn = 14

    # benchmarkStaticRow = 1
    # benchmarkDynamicRow = 1

    # benchmarkStaticSheet.write(benchmarkStaticRow, matInPathColumn, 'PrecompInPath')
    # benchmarkStaticSheet.write(benchmarkStaticRow, wastedColumn, 'Wasted')
    # benchmarkStaticRow += 1

    # benchmarkDynamicSheet.write(benchmarkDynamicRow, matInPathColumn, 'PrecompInPath')
    # benchmarkDynamicSheet.write(benchmarkDynamicRow, wastedColumn, 'Wasted')
    # benchmarkDynamicRow += 1


    #  LoanApprovalProcess
    # thresholds = materialise.getThreshold()
    # benchmarkStaticSheet.write(benchmarkStaticRow, processColumn, 'LoanApprovalProcess')

    # simulator.staticPrecompSimulation(1, "LoanApprovalProcess", './Policy&PP/privacy_preference AL=1.json', 'type1', 'benchmark')
    # thresholds = materialise.getThreshold()
    # benchmarkStaticRow = simulator.writeStaticResults("LoanApprovalProcess", benchmarkStaticSheet, 1, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(2, "LoanApprovalProcess", './Policy&PP/privacy_preference AL=0.9.json', 'type2', 'benchmark')
    # benchmarkStaticRow = simulator.writeStaticResults("LoanApprovalProcess", benchmarkStaticSheet, 2, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(3, "LoanApprovalProcess", './Policy&PP/privacy_preference AL=0.8.json', 'type3', 'benchmark')
    # benchmarkStaticRow = simulator.writeStaticResults("LoanApprovalProcess", benchmarkStaticSheet, 3, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(4, "LoanApprovalProcess", './Policy&PP/privacy_preference AL=0.8.json', 'type4', 'benchmark')
    # benchmarkStaticRow = simulator.writeStaticResults("LoanApprovalProcess", benchmarkStaticSheet, 4, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)

    # benchmarkDynamicSheet.write(benchmarkDynamicRow, processColumn, 'LoanApprovalProcess')
    # simulator.dynamicPrecompSimulation(1, "LoanApprovalProcess", './Policy&PP/privacy_preference AL=1.json', 'type1', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("LoanApprovalProcess", benchmarkDynamicSheet, 1, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(2, "LoanApprovalProcess", './Policy&PP/privacy_preference AL=0.9.json', 'type2', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("LoanApprovalProcess", benchmarkDynamicSheet, 2, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(3, "LoanApprovalProcess", './Policy&PP/privacy_preference AL=0.8.json', 'type3', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("LoanApprovalProcess", benchmarkDynamicSheet, 3, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(4, "LoanApprovalProcess", './Policy&PP/privacy_preference AL=0.8.json', 'type4', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("LoanApprovalProcess", benchmarkDynamicSheet, 4, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)

    # benchmarkStaticRow += 2
    # benchmarkDynamicRow += 2

    # # # LoanApprovalProcess1ù
    # benchmarkStaticSheet.write(benchmarkStaticRow, processColumn, 'LoanApprovalProcess1')

    # simulator.staticPrecompSimulation(1, "LoanApprovalProcess1", './Policy&PP/privacy_preference AL=1.json', 'type1', 'benchmark')
    # thresholds = materialise.getThreshold()
    # benchmarkStaticRow = simulator.writeStaticResults("LoanApprovalProcess1", benchmarkStaticSheet, 1, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(2, "LoanApprovalProcess1", './Policy&PP/privacy_preference AL=0.9.json', 'type2', 'benchmark')
    # benchmarkStaticRow = simulator.writeStaticResults("LoanApprovalProcess1", benchmarkStaticSheet, 2, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(3, "LoanApprovalProcess1", './Policy&PP/privacy_preference AL=0.8.json', 'type3', 'benchmark')
    # benchmarkStaticRow = simulator.writeStaticResults("LoanApprovalProcess1", benchmarkStaticSheet, 3, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(4, "LoanApprovalProcess1", './Policy&PP/privacy_preference AL=0.8.json', 'type4', 'benchmark')
    # benchmarkStaticRow = simulator.writeStaticResults("LoanApprovalProcess1", benchmarkStaticSheet, 4, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)

    # benchmarkDynamicSheet.write(benchmarkDynamicRow, processColumn, 'LoanApprovalProcess1')
    # simulator.dynamicPrecompSimulation(1, "LoanApprovalProcess1", './Policy&PP/privacy_preference AL=1.json', 'type1', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("LoanApprovalProcess1", benchmarkDynamicSheet, 1, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(2, "LoanApprovalProcess1", './Policy&PP/privacy_preference AL=0.9.json', 'type2', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("LoanApprovalProcess1", benchmarkDynamicSheet, 2, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(3, "LoanApprovalProcess1", './Policy&PP/privacy_preference AL=0.8.json', 'type3', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("LoanApprovalProcess1", benchmarkDynamicSheet, 3, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(4, "LoanApprovalProcess1", './Policy&PP/privacy_preference AL=0.8.json', 'type4', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("LoanApprovalProcess1", benchmarkDynamicSheet, 4, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)

    # benchmarkStaticRow += 2
    # benchmarkDynamicRow += 2

    # # QuoteProcess
    # thresholds = materialise.getThreshold()
    # benchmarkStaticSheet.write(benchmarkStaticRow, processColumn, 'QuoteProcess')

    # simulator.staticPrecompSimulation(1, "QuoteProcess", './Policy&PP/privacy_preference AL=1.json', 'type1', 'benchmark')
    # thresholds = materialise.getThreshold()
    # benchmarkStaticRow = simulator.writeStaticResults("QuoteProcess", benchmarkStaticSheet, 1, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(2, "QuoteProcess", './Policy&PP/privacy_preference AL=0.9.json', 'type2', 'benchmark')
    # benchmarkStaticRow = simulator.writeStaticResults("QuoteProcess", benchmarkStaticSheet, 2, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(3, "QuoteProcess", './Policy&PP/privacy_preference AL=0.8.json', 'type3', 'benchmark')
    # benchmarkStaticRow = simulator.writeStaticResults("QuoteProcess", benchmarkStaticSheet, 3, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(4, "QuoteProcess", './Policy&PP/privacy_preference AL=0.8.json', 'type4', 'benchmark')
    # benchmarkStaticRow = simulator.writeStaticResults("QuoteProcess", benchmarkStaticSheet, 4, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)

    # benchmarkDynamicSheet.write(benchmarkDynamicRow, processColumn, 'QuoteProcess')
    # simulator.dynamicPrecompSimulation(1, "QuoteProcess", './Policy&PP/privacy_preference AL=1.json', 'type1', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("QuoteProcess", benchmarkDynamicSheet, 1, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(2, "QuoteProcess", './Policy&PP/privacy_preference AL=0.9.json', 'type2', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("QuoteProcess", benchmarkDynamicSheet, 2, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(3, "QuoteProcess", './Policy&PP/privacy_preference AL=0.8.json', 'type3', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("QuoteProcess", benchmarkDynamicSheet, 3, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(4, "QuoteProcess", './Policy&PP/privacy_preference AL=0.8.json', 'type4', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("QuoteProcess", benchmarkDynamicSheet, 4, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)


    # ############
    # Cluster 4 #
    # ############
    # benchmarkStaticSheet.write(0, 16, 'Cluster4')
    # benchmarkDynamicSheet.write(0, 16, 'Cluster4')

    # processColumn = 16
    # thresholdColumn = 17
    # matInPathColumn = 18
    # wastedColumn = 19

    # benchmarkStaticRow = 1
    # benchmarkDynamicRow = 1

    # benchmarkStaticSheet.write(benchmarkStaticRow, matInPathColumn, 'PrecompInPath')
    # benchmarkStaticSheet.write(benchmarkStaticRow, wastedColumn, 'Wasted')
    # benchmarkStaticRow += 1

    # benchmarkDynamicSheet.write(benchmarkDynamicRow, matInPathColumn, 'PrecompInPath')
    # benchmarkDynamicSheet.write(benchmarkDynamicRow, wastedColumn, 'Wasted')
    # benchmarkDynamicRow += 1


    # # # NhinUnsubscribe
    # thresholds = materialise.getThreshold()
    # benchmarkStaticSheet.write(benchmarkStaticRow, processColumn, 'NhinUnsubscribe')

    # simulator.staticPrecompSimulation(1, "NhinUnsubscribe", './Policy&PP/privacy_preference AL=1.json', 'type1', 'benchmark')
    # thresholds = materialise.getThreshold()
    # benchmarkStaticRow = simulator.writeStaticResults("NhinUnsubscribe", benchmarkStaticSheet, 1, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(2, "NhinUnsubscribe", './Policy&PP/privacy_preference AL=0.9.json', 'type2', 'benchmark')
    # benchmarkStaticRow = simulator.writeStaticResults("NhinUnsubscribe", benchmarkStaticSheet, 2, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(3, "NhinUnsubscribe", './Policy&PP/privacy_preference AL=0.8.json', 'type3', 'benchmark')
    # benchmarkStaticRow = simulator.writeStaticResults("NhinUnsubscribe", benchmarkStaticSheet, 3, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(4, "NhinUnsubscribe", './Policy&PP/privacy_preference AL=0.8.json', 'type4', 'benchmark')
    # benchmarkStaticRow = simulator.writeStaticResults("NhinUnsubscribe", benchmarkStaticSheet, 4, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)

    # benchmarkDynamicSheet.write(benchmarkDynamicRow, processColumn, 'NhinUnsubscribe')
    # simulator.dynamicPrecompSimulation(1, "NhinUnsubscribe", './Policy&PP/privacy_preference AL=1.json', 'type1', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("NhinUnsubscribe", benchmarkDynamicSheet, 1, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(2, "NhinUnsubscribe", './Policy&PP/privacy_preference AL=0.9.json', 'type2', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("NhinUnsubscribe", benchmarkDynamicSheet, 2, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(3, "NhinUnsubscribe", './Policy&PP/privacy_preference AL=0.8.json', 'type3', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("NhinUnsubscribe", benchmarkDynamicSheet, 3, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(4, "NhinUnsubscribe", './Policy&PP/privacy_preference AL=0.8.json', 'type4', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("NhinUnsubscribe", benchmarkDynamicSheet, 4, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)

    # benchmarkStaticRow += 2
    # benchmarkDynamicRow += 2

    # # WorkoutProcess
    # thresholds = materialise.getThreshold()
    # benchmarkStaticSheet.write(benchmarkStaticRow, processColumn, 'WorkoutProcess')
    
    # simulator.staticPrecompSimulation(1, "WorkoutProcess", './Policy&PP/privacy_preference AL=1.json', 'type1', 'benchmark')
    # thresholds = materialise.getThreshold()
    # benchmarkStaticRow = simulator.writeStaticResults("WorkoutProcess", benchmarkStaticSheet, 1, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(2, "WorkoutProcess", './Policy&PP/privacy_preference AL=0.9.json', 'type2', 'benchmark')
    # benchmarkStaticRow = simulator.writeStaticResults("WorkoutProcess", benchmarkStaticSheet, 2, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(3, "WorkoutProcess", './Policy&PP/privacy_preference AL=0.8.json', 'type3', 'benchmark')
    # benchmarkStaticRow = simulator.writeStaticResults("WorkoutProcess", benchmarkStaticSheet, 3, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(4, "WorkoutProcess", './Policy&PP/privacy_preference AL=0.8.json', 'type4', 'benchmark')
    # benchmarkStaticRow = simulator.writeStaticResults("WorkoutProcess", benchmarkStaticSheet, 4, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    
    # benchmarkDynamicSheet.write(benchmarkDynamicRow, processColumn, 'WorkoutProcess')
    # simulator.dynamicPrecompSimulation(1, "WorkoutProcess", './Policy&PP/privacy_preference AL=1.json', 'type1', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("WorkoutProcess", benchmarkDynamicSheet, 1, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(2, "WorkoutProcess", './Policy&PP/privacy_preference AL=0.9.json', 'type2', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("WorkoutProcess", benchmarkDynamicSheet, 2, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(3, "WorkoutProcess", './Policy&PP/privacy_preference AL=0.8.json', 'type3', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("WorkoutProcess", benchmarkDynamicSheet, 3, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(4, "WorkoutProcess", './Policy&PP/privacy_preference AL=0.8.json', 'type4', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("WorkoutProcess", benchmarkDynamicSheet, 4, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)


    # ############
    # Cluster 5 #
    # ############
    # benchmarkStaticSheet.write(0, 21, 'Cluster5')
    # benchmarkDynamicSheet.write(0, 21, 'Cluster5')

    # processColumn = 21
    # thresholdColumn = 22
    # matInPathColumn = 23
    # wastedColumn = 24

    # benchmarkStaticRow = 1
    # benchmarkDynamicRow = 1

    # benchmarkStaticSheet.write(benchmarkStaticRow, matInPathColumn, 'PrecompInPath')
    # benchmarkStaticSheet.write(benchmarkStaticRow, wastedColumn, 'Wasted')
    # benchmarkStaticRow += 1

    # benchmarkDynamicSheet.write(benchmarkDynamicRow, matInPathColumn, 'PrecompInPath')
    # benchmarkDynamicSheet.write(benchmarkDynamicRow, wastedColumn, 'Wasted')
    # benchmarkDynamicRow += 1


    # # ASTROBookSearch
    # thresholds = materialise.getThreshold()
    # benchmarkStaticSheet.write(benchmarkStaticRow, processColumn, 'AstroBookSearch')
    
    # simulator.staticPrecompSimulation(1, "ASTROBookSearch", './Policy&PP/privacy_preference AL=1.json', 'type1', 'benchmark')
    # thresholds = materialise.getThreshold()
    # benchmarkStaticRow = simulator.writeStaticResults("ASTROBookSearch", benchmarkStaticSheet, 1, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(2, "ASTROBookSearch", './Policy&PP/privacy_preference AL=0.9.json', 'type2', 'benchmark')
    # benchmarkStaticRow = simulator.writeStaticResults("ASTROBookSearch", benchmarkStaticSheet, 2, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(3, "ASTROBookSearch", './Policy&PP/privacy_preference AL=0.8.json', 'type3', 'benchmark')
    # benchmarkStaticRow = simulator.writeStaticResults("ASTROBookSearch", benchmarkStaticSheet, 3, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(4, "ASTROBookSearch", './Policy&PP/privacy_preference AL=0.8.json', 'type4', 'benchmark')
    # benchmarkStaticRow = simulator.writeStaticResults("ASTROBookSearch", benchmarkStaticSheet, 4, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)

    # benchmarkDynamicSheet.write(benchmarkDynamicRow, processColumn, 'ASTROBookSearch')
    # simulator.dynamicPrecompSimulation(1, "ASTROBookSearch", './Policy&PP/privacy_preference AL=1.json', 'type1', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("ASTROBookSearch", benchmarkDynamicSheet, 1, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(2, "ASTROBookSearch", './Policy&PP/privacy_preference AL=0.9.json', 'type2', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("ASTROBookSearch", benchmarkDynamicSheet, 2, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(3, "ASTROBookSearch", './Policy&PP/privacy_preference AL=0.8.json', 'type3', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("ASTROBookSearch", benchmarkDynamicSheet, 3, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(4, "ASTROBookSearch", './Policy&PP/privacy_preference AL=0.8.json', 'type4', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("ASTROBookSearch", benchmarkDynamicSheet, 4, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)

    # benchmarkStaticRow += 2
    # benchmarkDynamicRow += 2

    # # LoanProcess
    # thresholds = materialise.getThreshold()
    # benchmarkStaticSheet.write(benchmarkStaticRow, processColumn, 'LoanProcess')

    # simulator.staticPrecompSimulation(1, "LoanProcess", './Policy&PP/privacy_preference AL=1.json', 'type1', 'benchmark')
    # thresholds = materialise.getThreshold()
    # benchmarkStaticRow = simulator.writeStaticResults("LoanProcess", benchmarkStaticSheet, 1, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(2, "LoanProcess", './Policy&PP/privacy_preference AL=0.9.json', 'type2', 'benchmark')
    # benchmarkStaticRow = simulator.writeStaticResults("LoanProcess", benchmarkStaticSheet, 2, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(3, "LoanProcess", './Policy&PP/privacy_preference AL=0.8.json', 'type3', 'benchmark')
    # benchmarkStaticRow = simulator.writeStaticResults("LoanProcess", benchmarkStaticSheet, 3, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(4, "LoanProcess", './Policy&PP/privacy_preference AL=0.8.json', 'type4', 'benchmark')
    # benchmarkStaticRow = simulator.writeStaticResults("LoanProcess", benchmarkStaticSheet, 4, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)

    # benchmarkDynamicSheet.write(benchmarkDynamicRow, processColumn, 'LoanProcess')
    # simulator.dynamicPrecompSimulation(1, "LoanProcess", './Policy&PP/privacy_preference AL=1.json', 'type1', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("LoanProcess", benchmarkDynamicSheet, 1, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(2, "LoanProcess", './Policy&PP/privacy_preference AL=0.9.json', 'type2', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("LoanProcess", benchmarkDynamicSheet, 2, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(3, "LoanProcess", './Policy&PP/privacy_preference AL=0.8.json', 'type3', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("LoanProcess", benchmarkDynamicSheet, 3, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(4, "LoanProcess", './Policy&PP/privacy_preference AL=0.8.json', 'type4', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("LoanProcess", benchmarkDynamicSheet, 4, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)

    # benchmarkStaticRow += 2
    # benchmarkDynamicRow += 2
    
    #  # PrestamoRamas
    # thresholds = materialise.getThreshold()
    # benchmarkStaticSheet.write(benchmarkStaticRow, processColumn, 'PrestamoRamas')

    # simulator.staticPrecompSimulation(1, "PrestamoRamas", './Policy&PP/privacy_preference AL=1.json', 'type1', 'benchmark')
    # thresholds = materialise.getThreshold()
    # benchmarkStaticRow = simulator.writeStaticResults("PrestamoRamas", benchmarkStaticSheet, 1, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(2, "PrestamoRamas", './Policy&PP/privacy_preference AL=0.9.json', 'type2', 'benchmark')
    # benchmarkStaticRow = simulator.writeStaticResults("PrestamoRamas", benchmarkStaticSheet, 2, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(3, "PrestamoRamas", './Policy&PP/privacy_preference AL=0.8.json', 'type3', 'benchmark')
    # benchmarkStaticRow = simulator.writeStaticResults("PrestamoRamas", benchmarkStaticSheet, 3, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(4, "PrestamoRamas", './Policy&PP/privacy_preference AL=0.8.json', 'type4', 'benchmark')
    # benchmarkStaticRow = simulator.writeStaticResults("PrestamoRamas", benchmarkStaticSheet, 4, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)

    # benchmarkDynamicSheet.write(benchmarkDynamicRow, processColumn, 'PrestamoRamas')
    # simulator.dynamicPrecompSimulation(1, "PrestamoRamas", './Policy&PP/privacy_preference AL=1.json', 'type1', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("PrestamoRamas", benchmarkDynamicSheet, 1, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(2, "PrestamoRamas", './Policy&PP/privacy_preference AL=0.9.json', 'type2', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("PrestamoRamas", benchmarkDynamicSheet, 2, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(3, "PrestamoRamas", './Policy&PP/privacy_preference AL=0.8.json', 'type3', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("PrestamoRamas", benchmarkDynamicSheet, 3, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(4, "PrestamoRamas", './Policy&PP/privacy_preference AL=0.8.json', 'type4', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("PrestamoRamas", benchmarkDynamicSheet, 4, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)

    # benchmarkStaticRow += 2
    # benchmarkDynamicRow += 2

    # # ResilientFlow
    # thresholds = materialise.getThreshold()
    # benchmarkStaticSheet.write(benchmarkStaticRow, processColumn, 'ResilientFlow')

    # simulator.staticPrecompSimulation(1, "ResilientFlow", './Policy&PP/privacy_preference AL=1.json', 'type1', 'benchmark')
    # thresholds = materialise.getThreshold()
    # benchmarkStaticRow = simulator.writeStaticResults("ResilientFlow", benchmarkStaticSheet, 1, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(2, "ResilientFlow", './Policy&PP/privacy_preference AL=0.9.json', 'type2', 'benchmark')
    # benchmarkStaticRow = simulator.writeStaticResults("ResilientFlow", benchmarkStaticSheet, 2, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(3, "ResilientFlow", './Policy&PP/privacy_preference AL=0.8.json', 'type3', 'benchmark')
    # benchmarkStaticRow = simulator.writeStaticResults("ResilientFlow", benchmarkStaticSheet, 3, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(4, "ResilientFlow", './Policy&PP/privacy_preference AL=0.8.json', 'type4', 'benchmark')
    # benchmarkStaticRow = simulator.writeStaticResults("ResilientFlow", benchmarkStaticSheet, 4, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)

    # benchmarkDynamicSheet.write(benchmarkDynamicRow, processColumn, 'ResilientFlow')
    # simulator.dynamicPrecompSimulation(1, "ResilientFlow", './Policy&PP/privacy_preference AL=1.json', 'type1', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("ResilientFlow", benchmarkDynamicSheet, 1, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(2, "ResilientFlow", './Policy&PP/privacy_preference AL=0.9.json', 'type2', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("ResilientFlow", benchmarkDynamicSheet, 2, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(3, "ResilientFlow", './Policy&PP/privacy_preference AL=0.8.json', 'type3', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("ResilientFlow", benchmarkDynamicSheet, 3, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(4, "ResilientFlow", './Policy&PP/privacy_preference AL=0.8.json', 'type4', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("ResilientFlow", benchmarkDynamicSheet, 4, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)


    # ############
    # Cluster 6 #
    # ############
    # benchmarkStaticSheet.write(0, 26, 'Cluster6')
    # benchmarkDynamicSheet.write(0, 26, 'Cluster6')

    # processColumn = 26
    # thresholdColumn = 27
    # matInPathColumn = 28
    # wastedColumn = 29

    # benchmarkStaticRow = 1
    # benchmarkDynamicRow = 1

    # benchmarkStaticSheet.write(benchmarkStaticRow, matInPathColumn, 'PrecompInPath')
    # benchmarkStaticSheet.write(benchmarkStaticRow, wastedColumn, 'Wasted')
    # benchmarkStaticRow += 1

    # benchmarkDynamicSheet.write(benchmarkDynamicRow, matInPathColumn, 'PrecompInPath')
    # benchmarkDynamicSheet.write(benchmarkDynamicRow, wastedColumn, 'Wasted')
    # benchmarkDynamicRow += 1

    # AstroBookBank
    # thresholds = materialise.getThreshold()
    # benchmarkStaticSheet.write(benchmarkStaticRow, processColumn, 'AstroBookBank')

    # simulator.staticPrecompSimulation(1, "AstroBookBank", './Policy&PP/privacy_preference AL=1.json', 'type1', 'benchmark')
    # thresholds = materialise.getThreshold()
    # benchmarkStaticRow = simulator.writeStaticResults("AstroBookBank", benchmarkStaticSheet, 1, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(2, "AstroBookBank", './Policy&PP/privacy_preference AL=0.9.json', 'type2', 'benchmark')
    # benchmarkStaticRow = simulator.writeStaticResults("AstroBookBank", benchmarkStaticSheet, 2, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(3, "AstroBookBank", './Policy&PP/privacy_preference AL=0.8.json', 'type3', 'benchmark')
    # benchmarkStaticRow = simulator.writeStaticResults("AstroBookBank", benchmarkStaticSheet, 3, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(4, "AstroBookBank", './Policy&PP/privacy_preference AL=0.8.json', 'type4', 'benchmark')
    # benchmarkStaticRow = simulator.writeStaticResults("AstroBookBank", benchmarkStaticSheet, 4, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)

    # benchmarkDynamicSheet.write(benchmarkDynamicRow, processColumn, 'AstroBookBank')
    # simulator.dynamicPrecompSimulation(1, "AstroBookBank", './Policy&PP/privacy_preference AL=1.json', 'type1', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("AstroBookBank", benchmarkDynamicSheet, 1, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(2, "AstroBookBank", './Policy&PP/privacy_preference AL=0.9.json', 'type2', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("AstroBookBank", benchmarkDynamicSheet, 2, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(3, "AstroBookBank", './Policy&PP/privacy_preference AL=0.8.json', 'type3', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("AstroBookBank", benchmarkDynamicSheet, 3, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(4, "AstroBookBank", './Policy&PP/privacy_preference AL=0.8.json', 'type4', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("AstroBookBank", benchmarkDynamicSheet, 4, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)

    # benchmarkStaticRow += 2
    # benchmarkDynamicRow += 2

    # # Ordering
    # thresholds = materialise.getThreshold()
    # benchmarkStaticSheet.write(benchmarkStaticRow, processColumn, 'Ordering')

    # simulator.staticPrecompSimulation(1, "Ordering", './Policy&PP/privacy_preference AL=1.json', 'type1', 'benchmark')
    # thresholds = materialise.getThreshold()
    # benchmarkStaticRow = simulator.writeStaticResults("Ordering", benchmarkStaticSheet, 1, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(2, "Ordering", './Policy&PP/privacy_preference AL=0.9.json', 'type2', 'benchmark')
    # benchmarkStaticRow = simulator.writeStaticResults("Ordering", benchmarkStaticSheet, 2, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(3, "Ordering", './Policy&PP/privacy_preference AL=0.8.json', 'type3', 'benchmark')
    # benchmarkStaticRow = simulator.writeStaticResults("Ordering", benchmarkStaticSheet, 3, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(4, "Ordering", './Policy&PP/privacy_preference AL=0.8.json', 'type4', 'benchmark')
    # benchmarkStaticRow = simulator.writeStaticResults("Ordering", benchmarkStaticSheet, 4, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)

    # benchmarkDynamicSheet.write(benchmarkDynamicRow, processColumn, 'Ordering')
    # simulator.dynamicPrecompSimulation(1, "Ordering", './Policy&PP/privacy_preference AL=1.json', 'type1', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("Ordering", benchmarkDynamicSheet, 1, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(2, "Ordering", './Policy&PP/privacy_preference AL=0.9.json', 'type2', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("Ordering", benchmarkDynamicSheet, 2, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(3, "Ordering", './Policy&PP/privacy_preference AL=0.8.json', 'type3', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("Ordering", benchmarkDynamicSheet, 3, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(4, "Ordering", './Policy&PP/privacy_preference AL=0.8.json', 'type4', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("Ordering", benchmarkDynamicSheet, 4, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    
    # benchmarkStaticRow += 2
    # benchmarkDynamicRow += 2

    # # SOAOrderBooking
    # thresholds = materialise.getThreshold()
    # benchmarkStaticSheet.write(benchmarkStaticRow, processColumn, 'SOAOrderBooking')
    
    # simulator.staticPrecompSimulation(1, "SOAOrderBooking", './Policy&PP/privacy_preference AL=1.json', 'type1', 'benchmark')
    # thresholds = materialise.getThreshold()
    # benchmarkStaticRow = simulator.writeStaticResults("SOAOrderBooking", benchmarkStaticSheet, 1, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(2, "SOAOrderBooking", './Policy&PP/privacy_preference AL=0.9.json', 'type2', 'benchmark')
    # benchmarkStaticRow = simulator.writeStaticResults("SOAOrderBooking", benchmarkStaticSheet, 2, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(3, "SOAOrderBooking", './Policy&PP/privacy_preference AL=0.8.json', 'type3', 'benchmark')
    # benchmarkStaticRow = simulator.writeStaticResults("SOAOrderBooking", benchmarkStaticSheet, 3, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(4, "SOAOrderBooking", './Policy&PP/privacy_preference AL=0.8.json', 'type4', 'benchmark')
    # benchmarkStaticRow = simulator.writeStaticResults("SOAOrderBooking", benchmarkStaticSheet, 4, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)

    # benchmarkDynamicSheet.write(benchmarkDynamicRow, processColumn, 'SOAOrderBooking')
    # simulator.dynamicPrecompSimulation(1, "SOAOrderBooking", './Policy&PP/privacy_preference AL=1.json', 'type1', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("SOAOrderBooking", benchmarkDynamicSheet, 1, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(2, "SOAOrderBooking", './Policy&PP/privacy_preference AL=0.9.json', 'type2', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("SOAOrderBooking", benchmarkDynamicSheet, 2, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(3, "SOAOrderBooking", './Policy&PP/privacy_preference AL=0.8.json', 'type3', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("SOAOrderBooking", benchmarkDynamicSheet, 3, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(4, "SOAOrderBooking", './Policy&PP/privacy_preference AL=0.8.json', 'type4', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("SOAOrderBooking", benchmarkDynamicSheet, 4, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)


    # ############
    # Cluster 7 #
    # ############
    # benchmarkStaticSheet.write(0, 31, 'Cluster7')
    # benchmarkDynamicSheet.write(0, 31, 'Cluster7')

    # processColumn = 31
    # thresholdColumn = 32
    # matInPathColumn = 33
    # wastedColumn = 34

    # benchmarkStaticRow = 1
    # benchmarkDynamicRow = 1

    # benchmarkStaticSheet.write(benchmarkStaticRow, matInPathColumn, 'PrecompInPath')
    # benchmarkStaticSheet.write(benchmarkStaticRow, wastedColumn, 'Wasted')
    # benchmarkStaticRow += 1

    # benchmarkDynamicSheet.write(benchmarkDynamicRow, matInPathColumn, 'PrecompInPath')
    # benchmarkDynamicSheet.write(benchmarkDynamicRow, wastedColumn, 'Wasted')
    # benchmarkDynamicRow += 1

    # #ClaimsProcess
    # thresholds = materialise.getThreshold()
    # benchmarkStaticSheet.write(benchmarkStaticRow, processColumn, 'ClaimProcess')

    # simulator.staticPrecompSimulation(1, "ClaimsProcess", './Policy&PP/privacy_preference AL=1.json', 'type1', 'benchmark')
    # thresholds = materialise.getThreshold()
    # benchmarkStaticRow = simulator.writeStaticResults("ClaimsProcess", benchmarkStaticSheet, 1, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(2, "ClaimsProcess", './Policy&PP/privacy_preference AL=0.9.json', 'type2', 'benchmark')
    # benchmarkStaticRow = simulator.writeStaticResults("ClaimsProcess", benchmarkStaticSheet, 2, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(3, "ClaimsProcess", './Policy&PP/privacy_preference AL=0.8.json', 'type3', 'benchmark')
    # benchmarkStaticRow = simulator.writeStaticResults("ClaimsProcess", benchmarkStaticSheet, 3, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(4, "ClaimsProcess", './Policy&PP/privacy_preference AL=0.8.json', 'type4', 'benchmark')
    # benchmarkStaticRow = simulator.writeStaticResults("ClaimsProcess", benchmarkStaticSheet, 4, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    
    # benchmarkDynamicSheet.write(benchmarkDynamicRow, processColumn, 'ClaimsProcess')
    # simulator.dynamicPrecompSimulation(1, "ClaimsProcess", './Policy&PP/privacy_preference AL=1.json', 'type1', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("ClaimsProcess", benchmarkDynamicSheet, 1, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(2, "ClaimsProcess", './Policy&PP/privacy_preference AL=0.9.json', 'type2', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("ClaimsProcess", benchmarkDynamicSheet, 2, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(3, "ClaimsProcess", './Policy&PP/privacy_preference AL=0.8.json', 'type3', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("ClaimsProcess", benchmarkDynamicSheet, 3, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(4, "ClaimsProcess", './Policy&PP/privacy_preference AL=0.8.json', 'type4', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("ClaimsProcess", benchmarkDynamicSheet, 4, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)

    # benchmarkStaticRow += 2
    # benchmarkDynamicRow += 2
    
    # # NhincComponentInternalSubDiscovery
    # thresholds = materialise.getThreshold()
    # benchmarkStaticSheet.write(benchmarkStaticRow, processColumn, 'NhincComponentInternalSubDiscovery')

    # simulator.staticPrecompSimulation(1, "NhincComponentInternalSubDiscovery", './Policy&PP/privacy_preference AL=1.json', 'type1', 'benchmark')
    # thresholds = materialise.getThreshold()
    # benchmarkStaticRow = simulator.writeStaticResults("NhincComponentInternalSubDiscovery", benchmarkStaticSheet, 1, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(2, "NhincComponentInternalSubDiscovery", './Policy&PP/privacy_preference AL=0.9.json', 'type2', 'benchmark')
    # benchmarkStaticRow = simulator.writeStaticResults("NhincComponentInternalSubDiscovery", benchmarkStaticSheet, 2, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(3, "NhincComponentInternalSubDiscovery", './Policy&PP/privacy_preference AL=0.8.json', 'type3', 'benchmark')
    # benchmarkStaticRow = simulator.writeStaticResults("NhincComponentInternalSubDiscovery", benchmarkStaticSheet, 3, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(4, "NhincComponentInternalSubDiscovery", './Policy&PP/privacy_preference AL=0.8.json', 'type4', 'benchmark')
    # benchmarkStaticRow = simulator.writeStaticResults("NhincComponentInternalSubDiscovery", benchmarkStaticSheet, 4, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)

    # benchmarkDynamicSheet.write(benchmarkDynamicRow, processColumn, 'NhincComponentInternalSubDiscovery')
    # simulator.dynamicPrecompSimulation(1, "NhincComponentInternalSubDiscovery", './Policy&PP/privacy_preference AL=1.json', 'type1', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("NhincComponentInternalSubDiscovery", benchmarkDynamicSheet, 1, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(2, "NhincComponentInternalSubDiscovery", './Policy&PP/privacy_preference AL=0.9.json', 'type2', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("NhincComponentInternalSubDiscovery", benchmarkDynamicSheet, 2, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(3, "NhincComponentInternalSubDiscovery", './Policy&PP/privacy_preference AL=0.8.json', 'type3', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("NhincComponentInternalSubDiscovery", benchmarkDynamicSheet, 3, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(4, "NhincComponentInternalSubDiscovery", './Policy&PP/privacy_preference AL=0.8.json', 'type4', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("NhincComponentInternalSubDiscovery", benchmarkDynamicSheet, 4, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)

    # benchmarkStaticRow += 2
    # benchmarkDynamicRow += 2

    # # NhincComponentInternalSubscriptionOrch
    # thresholds = materialise.getThreshold()
    # benchmarkStaticSheet.write(benchmarkStaticRow, processColumn, 'NhincComponentInternalSubscriptionOrch')

    # simulator.staticPrecompSimulation(1, "NhincComponentInternalSubscriptionOrch", './Policy&PP/privacy_preference AL=1.json', 'type1', 'benchmark')
    # thresholds = materialise.getThreshold()
    # benchmarkStaticRow = simulator.writeStaticResults("NhincComponentInternalSubscriptionOrch", benchmarkStaticSheet, 1, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(2, "NhincComponentInternalSubscriptionOrch", './Policy&PP/privacy_preference AL=0.9.json', 'type2', 'benchmark')
    # benchmarkStaticRow = simulator.writeStaticResults("NhincComponentInternalSubscriptionOrch", benchmarkStaticSheet, 2, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(3, "NhincComponentInternalSubscriptionOrch", './Policy&PP/privacy_preference AL=0.8.json', 'type3', 'benchmark')
    # benchmarkStaticRow = simulator.writeStaticResults("NhincComponentInternalSubscriptionOrch", benchmarkStaticSheet, 3, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(4, "NhincComponentInternalSubscriptionOrch", './Policy&PP/privacy_preference AL=0.8.json', 'type4', 'benchmark')
    # benchmarkStaticRow = simulator.writeStaticResults("NhincComponentInternalSubscriptionOrch", benchmarkStaticSheet, 4, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)

    # benchmarkDynamicSheet.write(benchmarkDynamicRow, processColumn, 'NhincComponentInternalSubscriptionOrch')
    # simulator.dynamicPrecompSimulation(1, "NhincComponentInternalSubscriptionOrch", './Policy&PP/privacy_preference AL=1.json', 'type1', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("NhincComponentInternalSubscriptionOrch", benchmarkDynamicSheet, 1, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(2, "NhincComponentInternalSubscriptionOrch", './Policy&PP/privacy_preference AL=0.9.json', 'type2', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("NhincComponentInternalSubscriptionOrch", benchmarkDynamicSheet, 2, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(3, "NhincComponentInternalSubscriptionOrch", './Policy&PP/privacy_preference AL=0.8.json', 'type3', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("NhincComponentInternalSubscriptionOrch", benchmarkDynamicSheet, 3, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(4, "NhincComponentInternalSubscriptionOrch", './Policy&PP/privacy_preference AL=0.8.json', 'type4', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("NhincComponentInternalSubscriptionOrch", benchmarkDynamicSheet, 4, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)


    # ############
    # Cluster 8 #
    # ############
    # benchmarkStaticSheet.write(0, 36, 'Cluster8')
    # benchmarkDynamicSheet.write(0, 36, 'Cluster8')

    # processColumn = 36
    # thresholdColumn = 37
    # matInPathColumn = 38
    # wastedColumn = 39

    # benchmarkStaticRow = 1
    # benchmarkDynamicRow = 1

    # benchmarkStaticSheet.write(benchmarkStaticRow, matInPathColumn, 'PrecompInPath')
    # benchmarkStaticSheet.write(benchmarkStaticRow, wastedColumn, 'Wasted')
    # benchmarkStaticRow += 1

    # benchmarkDynamicSheet.write(benchmarkDynamicRow, matInPathColumn, 'PrecompInPath')
    # benchmarkDynamicSheet.write(benchmarkDynamicRow, wastedColumn, 'Wasted')
    # benchmarkDynamicRow += 1

    # # ASTROBookCart
    # thresholds = materialise.getThreshold()
    # benchmarkStaticSheet.write(benchmarkStaticRow, processColumn, 'AstroBookCart')

    # simulator.staticPrecompSimulation(1, "ASTROBookCart", './Policy&PP/privacy_preference AL=1.json', 'type1', 'benchmark')
    # thresholds = materialise.getThreshold()
    # benchmarkStaticRow = simulator.writeStaticResults("ASTROBookCart", benchmarkStaticSheet, 1, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(2, "ASTROBookCart", './Policy&PP/privacy_preference AL=0.9.json', 'type2', 'benchmark')
    # benchmarkStaticRow = simulator.writeStaticResults("ASTROBookCart", benchmarkStaticSheet, 2, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(3, "ASTROBookCart", './Policy&PP/privacy_preference AL=0.8.json', 'type3', 'benchmark')
    # benchmarkStaticRow = simulator.writeStaticResults("ASTROBookCart", benchmarkStaticSheet, 3, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(4, "ASTROBookCart", './Policy&PP/privacy_preference AL=0.7.json', 'type3', 'benchmark')
    # benchmarkStaticRow = simulator.writeStaticResults("ASTROBookCart", benchmarkStaticSheet, 4, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)

    # benchmarkDynamicSheet.write(benchmarkDynamicRow, processColumn, 'ASTROBookCart')
    # simulator.dynamicPrecompSimulation(1, "ASTROBookCart", './Policy&PP/privacy_preference AL=1.json', 'type1', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("ASTROBookCart", benchmarkDynamicSheet, 1, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(2, "ASTROBookCart", './Policy&PP/privacy_preference AL=0.9.json', 'type2', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("ASTROBookCart", benchmarkDynamicSheet, 2, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(3, "ASTROBookCart", './Policy&PP/privacy_preference AL=0.8.json', 'type3', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("ASTROBookCart", benchmarkDynamicSheet, 3, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(4, "ASTROBookCart", './Policy&PP/privacy_preference AL=0.8.json', 'type4', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("ASTROBookCart", benchmarkDynamicSheet, 4, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    
    # benchmarkStaticRow += 2
    # benchmarkDynamicRow += 2

    # # #PartsDataService
    # thresholds = materialise.getThreshold()
    # benchmarkStaticSheet.write(benchmarkStaticRow, processColumn, 'PartsDataService')
    
    # simulator.staticPrecompSimulation(1, "PartsDataService", './Policy&PP/privacy_preference AL=1.json', 'type1', 'benchmark')
    # thresholds = materialise.getThreshold()
    # benchmarkStaticRow = simulator.writeStaticResults("PartsDataService", benchmarkStaticSheet, 1, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(2, "PartsDataService", './Policy&PP/privacy_preference AL=0.9.json', 'type2', 'benchmark')
    # benchmarkStaticRow = simulator.writeStaticResults("PartsDataService", benchmarkStaticSheet, 2, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(3, "PartsDataService", './Policy&PP/privacy_preference AL=0.8.json', 'type3', 'benchmark')
    # benchmarkStaticRow = simulator.writeStaticResults("PartsDataService", benchmarkStaticSheet, 3, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(4, "PartsDataService", './Policy&PP/privacy_preference AL=0.8.json', 'type4', 'benchmark')
    # benchmarkStaticRow = simulator.writeStaticResults("PartsDataService", benchmarkStaticSheet, 4, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)

    # benchmarkDynamicSheet.write(benchmarkDynamicRow, processColumn, 'PartsDataService')
    # simulator.dynamicPrecompSimulation(1, "PartsDataService", './Policy&PP/privacy_preference AL=1.json', 'type1', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("PartsDataService", benchmarkDynamicSheet, 1, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(2, "PartsDataService", './Policy&PP/privacy_preference AL=0.9.json', 'type2', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("PartsDataService", benchmarkDynamicSheet, 2, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(3, "PartsDataService", './Policy&PP/privacy_preference AL=0.8.json', 'type3', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("PartsDataService", benchmarkDynamicSheet, 3, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(4, "PartsDataService", './Policy&PP/privacy_preference AL=0.8.json', 'type4', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("PartsDataService", benchmarkDynamicSheet, 4, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)

    # benchmarkStaticRow += 2
    # benchmarkDynamicRow += 2

    # #Synchronous
    # thresholds = materialise.getThreshold()
    # benchmarkStaticSheet.write(benchmarkStaticRow, processColumn, 'Synchronous')

    # simulator.staticPrecompSimulation(1, "Synchronous", './Policy&PP/privacy_preference AL=1.json', 'type1', 'benchmark')
    # thresholds = materialise.getThreshold()
    # benchmarkStaticRow = simulator.writeStaticResults("Synchronous", benchmarkStaticSheet, 1, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(2, "Synchronous", './Policy&PP/privacy_preference AL=0.9.json', 'type2', 'benchmark')
    # benchmarkStaticRow = simulator.writeStaticResults("Synchronous", benchmarkStaticSheet, 2, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(3, "Synchronous", './Policy&PP/privacy_preference AL=0.8.json', 'type3', 'benchmark')
    # benchmarkStaticRow = simulator.writeStaticResults("Synchronous", benchmarkStaticSheet, 3, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(4, "Synchronous", './Policy&PP/privacy_preference AL=0.8.json', 'type4', 'benchmark')
    # benchmarkStaticRow = simulator.writeStaticResults("Synchronous", benchmarkStaticSheet, 4, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)

    # benchmarkDynamicSheet.write(benchmarkDynamicRow, processColumn, 'Synchronous')
    # simulator.dynamicPrecompSimulation(1, "Synchronous", './Policy&PP/privacy_preference AL=1.json', 'type1', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("Synchronous", benchmarkDynamicSheet, 1, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(2, "Synchronous", './Policy&PP/privacy_preference AL=0.9.json', 'type2', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("Synchronous", benchmarkDynamicSheet, 2, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(3, "Synchronous", './Policy&PP/privacy_preference AL=0.8.json', 'type3', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("Synchronous", benchmarkDynamicSheet, 3, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(4, "Synchronous", './Policy&PP/privacy_preference AL=0.8.json', 'type4', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("Synchronous", benchmarkDynamicSheet, 4, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)

    # benchmarkStaticRow += 2
    # benchmarkDynamicRow += 2

    # ############
    # Cluster 9 #
    # ############
    
    # benchmarkStaticSheet.write(0, 41, 'Cluster9')
    # benchmarkDynamicSheet.write(0, 41, 'Cluster9')

    # processColumn = 41
    # thresholdColumn = 42
    # matInPathColumn = 43
    # wastedColumn = 44

    # benchmarkStaticRow = 1
    # benchmarkDynamicRow = 1

    # benchmarkStaticSheet.write(benchmarkStaticRow, matInPathColumn, 'PrecompInPath')
    # benchmarkStaticSheet.write(benchmarkStaticRow, wastedColumn, 'Wasted')
    # benchmarkStaticRow += 1

    # benchmarkDynamicSheet.write(benchmarkDynamicRow, matInPathColumn, 'PrecompInPath')
    # benchmarkDynamicSheet.write(benchmarkDynamicRow, wastedColumn, 'Wasted')
    # benchmarkDynamicRow += 1


    # # # # NhincComponentAuditLog
    # thresholds = materialise.getThreshold()
    # benchmarkStaticSheet.write(benchmarkStaticRow, processColumn, 'NhincComponentAuditLog')

    # simulator.staticPrecompSimulation(1, "NhincComponentAuditLog", './Policy&PP/privacy_preference AL=1.json', 'type1', 'benchmark')
    # thresholds = materialise.getThreshold()
    # benchmarkStaticRow = simulator.writeStaticResults("NhincComponentAuditLog", benchmarkStaticSheet, 1, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(2, "NhincComponentAuditLog", './Policy&PP/privacy_preference AL=0.9.json', 'type2', 'benchmark')
    # benchmarkStaticRow = simulator.writeStaticResults("NhincComponentAuditLog", benchmarkStaticSheet, 2, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(3, "NhincComponentAuditLog", './Policy&PP/privacy_preference AL=0.8.json', 'type3', 'benchmark')
    # benchmarkStaticRow = simulator.writeStaticResults("NhincComponentAuditLog", benchmarkStaticSheet, 3, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(4, "NhincComponentAuditLog", './Policy&PP/privacy_preference AL=0.8.json', 'type4', 'benchmark')
    # benchmarkStaticRow = simulator.writeStaticResults("NhincComponentAuditLog", benchmarkStaticSheet, 4, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
   
    # benchmarkDynamicSheet.write(benchmarkDynamicRow, processColumn, 'NhincComponentAuditLog')
    # simulator.dynamicPrecompSimulation(1, "NhincComponentAuditLog", './Policy&PP/privacy_preference AL=1.json', 'type1', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("NhincComponentAuditLog", benchmarkDynamicSheet, 1, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(2, "NhincComponentAuditLog", './Policy&PP/privacy_preference AL=0.9.json', 'type2', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("NhincComponentAuditLog", benchmarkDynamicSheet, 2, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(3, "NhincComponentAuditLog", './Policy&PP/privacy_preference AL=0.8.json', 'type3', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("NhincComponentAuditLog", benchmarkDynamicSheet, 3, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(4, "NhincComponentAuditLog", './Policy&PP/privacy_preference AL=0.8.json', 'type4', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("NhincComponentAuditLog", benchmarkDynamicSheet, 4, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)

    # #############
    # Cluster 10 #
    # #############

    # benchmarkStaticSheet.write(0, 46, 'Cluster10')
    # benchmarkDynamicSheet.write(0, 46, 'Cluster10')

    # processColumn = 46
    # thresholdColumn = 47
    # matInPathColumn = 48
    # wastedColumn = 49

    # benchmarkStaticRow = 1
    # benchmarkDynamicRow = 1

    # benchmarkStaticSheet.write(benchmarkStaticRow, matInPathColumn, 'PrecompInPath')
    # benchmarkStaticSheet.write(benchmarkStaticRow, wastedColumn, 'Wasted')
    # benchmarkStaticRow += 1

    # benchmarkDynamicSheet.write(benchmarkDynamicRow, matInPathColumn, 'PrecompInPath')
    # benchmarkDynamicSheet.write(benchmarkDynamicRow, wastedColumn, 'Wasted')
    # benchmarkDynamicRow += 1
    

    # #AstroBookStore
    # thresholds = materialise.getThreshold()
    # benchmarkStaticSheet.write(benchmarkStaticRow, processColumn, 'AstroBookStore')

    # simulator.staticPrecompSimulation(1, "AstroBookStore", './Policy&PP/privacy_preference AL=1.json', 'type1', 'benchmark')
    # thresholds = materialise.getThreshold()
    # benchmarkStaticRow = simulator.writeStaticResults("AstroBookStore", benchmarkStaticSheet, 1, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(2, "AstroBookStore", './Policy&PP/privacy_preference AL=0.9.json', 'type2', 'benchmark')
    # benchmarkStaticRow = simulator.writeStaticResults("AstroBookStore", benchmarkStaticSheet, 2, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(3, "AstroBookStore", './Policy&PP/privacy_preference AL=0.8.json', 'type3', 'benchmark')
    # benchmarkStaticRow = simulator.writeStaticResults("AstroBookStore", benchmarkStaticSheet, 3, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.staticPrecompSimulation(4, "AstroBookStore", './Policy&PP/privacy_preference AL=0.8.json', 'type4', 'benchmark')
    # benchmarkStaticRow = simulator.writeStaticResults("AstroBookStore", benchmarkStaticSheet, 4, benchmarkStaticRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)

    # benchmarkDynamicSheet.write(benchmarkDynamicRow, processColumn, 'AstroBookStore')
    # simulator.dynamicPrecompSimulation(1, "AstroBookStore", './Policy&PP/privacy_preference AL=1.json', 'type1', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("AstroBookStore", benchmarkDynamicSheet, 1, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(2, "AstroBookStore", './Policy&PP/privacy_preference AL=0.9.json', 'type2', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("AstroBookStore", benchmarkDynamicSheet, 2, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(3, "AstroBookStore", './Policy&PP/privacy_preference AL=0.8.json', 'type3', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("AstroBookStore", benchmarkDynamicSheet, 3, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)
    # simulator.dynamicPrecompSimulation(4, "AstroBookStore", './Policy&PP/privacy_preference AL=0.8.json', 'type4', 'benchmark')
    # benchmarkDynamicRow = simulator.writeDynamicResults("AstroBookStore", benchmarkDynamicSheet, 4, benchmarkDynamicRow, processColumn, thresholdColumn, matInPathColumn, wastedColumn)

   
    
    resultFile.close()