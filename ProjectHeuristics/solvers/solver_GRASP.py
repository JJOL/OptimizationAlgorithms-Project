'''
AMMM Lab Heuristics
GRASP solver
Copyright 2018 Luis Velasco.

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
'''

import random
import time
from solver import _Solver
from solvers.localSearch import LocalSearch


# Inherits from the parent abstract solver.
class Solver_GRASP(_Solver):

    def _selectCandidate(self, candidateList, alpha):

        
        # compute boundary highest load as a function of the minimum and maximum highest loads and the alpha parameter
        maxGain = candidateList[0][2]
        minGain = candidateList[-1][2]
        boundaryMinimumGain = maxGain - (maxGain - minGain) * alpha
        
        # find elements that fall into the RCL
        maxIndex = 0
        for i, candidate in enumerate(candidateList):
            if candidate[2] >= boundaryMinimumGain:
                maxIndex = i
            else:
                break

        # create RCL and pick an element randomly
        rcl = candidateList[0:maxIndex+1]          # pick first maxIndex elements starting from element 0
        if not rcl:
            return None
        return random.choice(rcl)          # pick a candidate from rcl at random
    
    def _greedyRandomizedConstruction(self, alpha):
        solution = self.instance.createSolution()
        candidateList = solution.findFeasibleBidWins()
        sortedCandidateList = sorted(candidateList, key=lambda x: x[2], reverse=True)

        count = 0
        while len(sortedCandidateList) > 0:
            # start = time.time()
            candidate = self._selectCandidate(sortedCandidateList, alpha)
            sortedCandidateList.remove(candidate)
            if solution.isCandidateFeasible(candidate):
                solution.assign(candidate)
            
            # end = time.time()

            # if count % 100 == 0:
            #     print('Greedy iteration: %d, candidateList size: %d, time: %f secs' % (count, len(candidateList), end - start))
            count += 1

        if not solution.isComplete():
            solution.makeInfeasible()
        return solution
    
    def stopCriteria(self):
        self.elapsedEvalTime = time.time() - self.startTime
        return time.time() - self.startTime > self.config.maxExecTime

    def solve(self, **kwargs):
        self.startTimeMeasure()
        incumbent = self.instance.createSolution()
        incumbent.makeInfeasible()
        bestHighestGain = incumbent.getFitness() # infinite BUT WE ARE MAXIMIZING.... SO LET's PUT IT -INF
        self.writeLogLine(bestHighestGain, 0)

        iteration = 0
        while not self.stopCriteria():
            iteration += 1
            
            # force first iteration as a Greedy execution (alpha == 0)
            alpha = 0 if iteration == 1 else self.config.alpha

            solution = self._greedyRandomizedConstruction(alpha)
            if self.config.localSearch:
                localSearch = LocalSearch(self.config, None)
                endTime = self.startTime + self.config.maxExecTime
                solution = localSearch.solve(solution=solution, startTime=self.startTime, endTime=endTime)

            if solution.isFeasible():
                solutionHighestGain = solution.getFitness()
                if solutionHighestGain > bestHighestGain :
                    incumbent = solution
                    bestHighestGain = solutionHighestGain
                    self.writeLogLine(bestHighestGain, iteration)

        self.writeLogLine(bestHighestGain, iteration)
        self.numSolutionsConstructed = iteration
        self.printPerformance()
        return incumbent

