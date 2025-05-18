"""
AMMM Lab Heuristics
Representation of a problem instance
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

from problem.Task import Task
from problem.CPU import CPU
from problem.solution import Solution


class Instance(object):
    def __init__(self, config, inputData):
        self.config = config
        self.inputData = inputData

        self.nUsers = inputData.N
        self._bidMatrix = inputData.m

    # def getNumTasks(self):
    #     return len(self.tasks)

    # def getNumCPUs(self):
    #     return len(self.cpus)

    # def getTasks(self):
    #     return self.tasks

    # def getCPUs(self):
    #     return self.cpus

    def createSolution(self):
        solution = Solution(self.nUsers, self._bidMatrix)
        solution.setVerbose(self.config.verbose)
        return solution

    def checkInstance(self):
        for i in range(self.nUsers):
            if self._bidMatrix[i][i] > 0:
                return False
        return True
