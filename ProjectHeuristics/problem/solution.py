"""
AMMM Lab Heuristics
Representation of a solution instance
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
from solution import _Solution
from problem.graph import Graph


# This class stores the load of the highest loaded CPU
# when a task is assigned to a CPU.
class Assignment(object):
    def __init__(self, bid, revenue):
        self.bid = bid
        self.revenue = revenue

    def __str__(self):
        return "<t_%d, c_%d>: highestLoad: %.2f%%" % (self.taskId, self.cpuId, self.highestLoad*100)


# Solution includes functions to manage the solution, to perform feasibility
# checks and to dump the solution into a string or file.
class Solution(_Solution):
    def __init__(self, nUsers, bidMatrix):
        self.nUsers = nUsers
        self.bidMatrix = bidMatrix
        self.edges = self._extractEdges(bidMatrix, nUsers)
        self.wonBids = []
        super().__init__()

    def _extractEdges(self, matrix, n):
        edges = []
        for i in range(n):
            for j in range(n):
                if (matrix[i][j] + matrix[j][i]) > 0:
                    edges.append((i, j, matrix[i][j]))
        return edges

    def assign(self, bid):
        self.wonBids.append(bid)
        self.fitness += bid[2]
        return True
    
    def _remainingBids(self):
        return [e for e in self.edges if e not in self.wonBids]

    def findFeasibleBidWins(self):
        feasibleAssignments = []
        for bid in self._remainingBids():
            if Graph(self.nUsers, self.wonBids + [bid]).isDAG():
                feasibleAssignments.append(bid)

        return feasibleAssignments
    
    def isComplete(self):
        return len(self.wonBids) == len(self.edges)/2

    def __str__(self):
        strSolution = 'z = %10.8f;\n' % self.fitness
        if self.fitness == float('inf'): return strSolution

        # Xtc: decision variable containing the assignment of tasks to CPUs
        # pre-fill with no assignments (all-zeros)
        for bid in self.wonBids:
            strSolution += '%d -> %d\n' % (bid[0]+1, bid[1]+1)

        return strSolution

    def saveToFile(self, filePath):
        f = open(filePath, 'w')
        f.write(self.__str__())
        f.close()
