"""
AMMM Lab Heuristics
Local Search algorithm
Copyright 2020 Luis Velasco.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import copy
import time
from solver import _Solver
from AMMMGlobals import AMMMException
import random

# A change in a solution in the form: move taskId from curCPUId to newCPUId.
# This class is used to perform sets of modifications.
# A new solution can be created based on an existing solution and a list of
# changes using the createNeighborSolution(solution, moves) function.
class Move(object):
    def __init__(self, taskId, curCPUId, newCPUId):
        self.taskId = taskId
        self.curCPUId = curCPUId
        self.newCPUId = newCPUId

    def __str__(self):
        return "taskId: %d Move: %d -> %d" % (self.taskId, self.curCPUId, self.newCPUId)


# Implementation of a local search using two neighborhoods and two different policies.
class LocalSearch(_Solver):
    def __init__(self, config, instance):
        self.enabled = config.localSearch
        self.nhStrategy = config.neighborhoodStrategy
        self.policy = config.policy
        self.maxExecTime = config.maxExecTime
        self.localIterations = 0
        super().__init__(config, instance)

    def createNeighborSolution(self, solution, moves):
        # unassign the tasks specified in changes
        # and reassign them to the new CPUs

        newSolution = copy.deepcopy(solution)

        for move in moves:
            newSolution.unassign(move.taskId, move.curCPUId)

        for move in moves:
            feasible = newSolution.assign(move.taskId, move.newCPUId)
            if not feasible: return None

        return newSolution

    def evaluateNeighbor(self, solution, moves):
        newAvailCapPerCPUId = copy.deepcopy(solution.availCapacityPerCPUId)

        for move in moves:
            taskId = move.taskId
            newAvailCapPerCPUId[move.curCPUId] += solution.tasks[taskId].getTotalResources()

        for move in moves:
            taskId = move.taskId
            newCPUId = move.newCPUId
            taskResources = solution.tasks[taskId].getTotalResources()
            if newAvailCapPerCPUId[newCPUId] < taskResources: return float('infinity')
            newAvailCapPerCPUId[newCPUId] -= taskResources

        highestLoad = 0.0
        for cpu in solution.cpus:
            cpuId = cpu.getId()
            totalCapacity = cpu.getTotalCapacity()
            availableCapacity = newAvailCapPerCPUId[cpuId]
            highestLoad = max(highestLoad, (totalCapacity - availableCapacity) / totalCapacity)

        return highestLoad

    def getCPUswithAssignemnts(self, solution):
        tasks = solution.tasks
        cpus = solution.cpus

        # create vector of assignments <task, cpu>
        cpusWithAssignments = []
        for cpu in cpus:
            cpuId = cpu.getId()
            load = solution.loadPerCPUId[cpuId]
            assignedTasks = solution.cpuIdToListTaskId[cpuId]
            if assignedTasks is None: assignedTasks = []
            assignedTasksWithResources = []
            for taskId in assignedTasks:
                taskPair = (taskId, tasks[taskId].getTotalResources())
                assignedTasksWithResources.append(taskPair)
            assignedTasksWithResources.sort(key=lambda task: task[1], reverse=True)
            cpuWithAssignments = (cpuId, load, solution.availCapacityPerCPUId[cpuId], assignedTasksWithResources)
            cpusWithAssignments.append(cpuWithAssignments)

        # Sort assignments by the load of the assigned CPU in descending order.
        cpusWithAssignments.sort(key=lambda cpuWithAssignment: cpuWithAssignment[1], reverse=True)
        return cpusWithAssignments

    def getAssignmentsSortedByCPULoad(self, solution):
        tasks = solution.tasks
        cpus = solution.cpus

        # create vector of assignments <task, cpu>
        assignments = []
        for task in tasks:
            taskId = task.getId()
            cpuId = solution.getCPUIdAssignedToTaskId(taskId)
            cpu = cpus[cpuId]
            highestLoad = solution.loadPerCPUId[cpuId]
            assignment = (task, cpu, highestLoad)
            assignments.append(assignment)

        # For best improvement policy it does not make sense to sort the tasks since all of them must be explored.
        # However, for first improvement, we can start by the tasks assigned to the more loaded CPUs.
        if self.policy == 'BestImprovement': return assignments

        # Sort assignments by the load of the assigned CPU in descending order.
        sorted_assignments = sorted(assignments, key=lambda x: x[2], reverse=True)
        return sorted_assignments

    def exploreReassignment(self, solution):
        cpus = solution.cpus
        curHighestLoad = solution.getFitness()
        bestNeighbor = solution

        sortedAssignments = self.getAssignmentsSortedByCPULoad(solution)

        for assignment in sortedAssignments:
            task = assignment[0]
            taskId = task.getId()

            curCPU = assignment[1]
            curCPUId = curCPU.getId()

            for cpu in cpus:
                newCPUId = cpu.getId()
                if newCPUId == curCPUId: continue

                moves = [Move(taskId, curCPUId, newCPUId)]
                neighborHighestLoad = self.evaluateNeighbor(solution, moves)
                if curHighestLoad > neighborHighestLoad:
                    neighbor = self.createNeighborSolution(solution, moves)
                    if neighbor is None: continue
                    if self.policy == 'FirstImprovement':
                        return neighbor
                    else:
                        bestNeighbor = neighbor
                        curHighestLoad = neighborHighestLoad

        return bestNeighbor

    def exploreExchange(self, solution, visited: list[str]):
        curHighestLoad = solution.getFitness()
        bestNeighbor = None

        for c in solution.getExchangeCandidates():
            sol = solution.clone()
            sol.applyExchange(c)
            if sol.toState() in visited: continue

            if sol.getFitness() > curHighestLoad:
                bestNeighbor = sol
                curHighestLoad = sol.getFitness()
                if self.policy == 'FirstImprovement': return bestNeighbor

        return bestNeighbor

    def exploreNeighborhood(self, solution, visited):
        if self.nhStrategy == 'BidExchange': return self.exploreExchange(solution, visited)
        elif self.nhStrategy == 'PrioritizeUser': return self.exploreReassignment(solution, visited) 
        # Select a node reverse it's highest arrow (cost) and all others needed to avoid cycles. Use DFS to find other arrows to reverse
        else: raise AMMMException('Unsupported NeighborhoodStrategy(%s)' % self.nhStrategy)

    def solve(self, **kwargs):
        initialSolution = kwargs.get('solution', None)
        if initialSolution is None:
            raise AMMMException('[local search] No solution could be retrieved')

        if not initialSolution.isFeasible(): return initialSolution
        self.startTime = kwargs.get('startTime', None)
        endTime = kwargs.get('endTime', None)

        incumbent = initialSolution
        incumbentFitness = incumbent.getFitness()
        iterations = 0

        if self.config.verbose: print('Fitness prior to localSearch: ' + str(incumbentFitness))

        visited = []
        visited.append(incumbent.toState())
        # keep iterating while improvements are found
        while time.time() < endTime:
            iterations += 1
            neighbor = self.exploreNeighborhood(incumbent, visited)
            if neighbor is None: break
            visited.append(neighbor.toState())
            neighborFitness = neighbor.getFitness()
            if incumbentFitness > neighborFitness: break
            incumbent = neighbor
            incumbentFitness = neighborFitness

        if self.config.verbose: print('Search iterations: ' + str(iterations))
        if self.config.verbose: print('Fitness after localSearch: ' + str(incumbentFitness))

        self.localIterations = iterations

        return incumbent
