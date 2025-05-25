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
from problem.graph import Graph, DynTopoDAG
from dataclasses import dataclass
import time

# This class stores the load of the highest loaded CPU
# when a task is assigned to a CPU.
class Assignment(object):
    def __init__(self, bid, revenue):
        self.bid = bid
        self.revenue = revenue

    def __str__(self):
        return "<t_%d, c_%d>: highestLoad: %.2f%%" % (self.taskId, self.cpuId, self.highestLoad*100)

@dataclass
class BidExchange:
    oldBid: tuple[int,int,int]
    newBid: tuple[int,int,int]
# Solution includes functions to manage the solution, to perform feasibility
# checks and to dump the solution into a string or file.
class Solution(_Solution):
    def __init__(self, nUsers, bidMatrix):
        self.nUsers = nUsers
        self.bidMatrix = bidMatrix
        self.edges = self._extractEdges(bidMatrix, nUsers)
        self.wonBids = []
        # self.graph = DynTopoDAG(nUsers)
        super().__init__()

    def clone(self):
        sol = Solution(self.nUsers, self.bidMatrix)
        for b in self.wonBids:
            sol.wonBids.append(b)
        sol.fitness = self.fitness
        return sol
    

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
        # self.graph.add_edge(bid[0], bid[1])

        return True
    
    def _remainingBids(self):
        remainingBids = []
        for e in self.edges:
            remainingBids.append((e[0], e[1], self.bidMatrix[e[0]][e[1]]))
        return remainingBids

    def findFeasibleBidWins(self):
        return self._remainingBids()
        # feasibleAssignments = []
        # # graph = Graph(self.nUsers)
        # # graph.makeBaseEdges(self.wonBids)
        # for bid in self._remainingBids():
        #     graph = Graph(self.nUsers, self.wonBids + [bid])
        #     is_dag = graph.isDAG()
        #     if is_dag:
        #         feasibleAssignments.append(bid)

        # return feasibleAssignments
    
    def isCandidateFeasible(self, candidate):
        graph = Graph(self.nUsers, self.wonBids + [candidate])
        return graph.isDAG()
    
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
    
    def getBidWinner(self, i, j):
        for b in self.wonBids:
            if b[0] == i and b[1] == j:
                return i
            if b[0] == j and b[1] == i:
                return j
        raise Exception("Trying to get bid winner state for incomplete solution!")
    
    def toState(self):
        state = ""
        for i in range(self.nUsers):
            for j in range(i + 1, self.nUsers):
                if (self.bidMatrix[i][j] + self.bidMatrix[j][i]) > 0:
                    if self.getBidWinner(i,j) == i:
                        state += "1"
                    else:
                        state += "0"
        return state
    
    def getExchangeCandidates(self) -> list[BidExchange]:
        candidates = []
        for b in self.wonBids:
            alternativeBids = [a for a in self.wonBids if a != b]
            counterBid = (b[1], b[0], self.bidMatrix[b[1]][b[0]])
            if Graph(self.nUsers, alternativeBids + [counterBid]).isDAG():
                candidates.append(BidExchange(b, counterBid))
            
        return candidates


    def applyExchange(self, exchange: BidExchange):
        self.wonBids.remove(exchange.oldBid)
        self.fitness -= exchange.oldBid[2]
        self.assign(exchange.newBid)



    def saveToFile(self, filePath):
        f = open(filePath, 'w')
        f.write(self.__str__())
        f.close()
