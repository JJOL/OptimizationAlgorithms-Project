'''
AMMM Lab Heuristics
Greedy solver
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
'''

import random, time
from solver import _Solver
from solvers.localSearch import LocalSearch


# Inherits from the parent abstract solver.
class Solver_Greedy(_Solver):

    def _selectCandidate(self, candidateList):
        if self.config.solver == 'Greedy':
            return candidateList[0]
        return random.choice(candidateList)

    def construction(self):
        # get an empty solution for the problem
        solution = self.instance.createSolution()
        candidateList = solution.findFeasibleBidWins()
        sortedCandidateList = sorted(candidateList, key=lambda x: x[2], reverse=True)
        count = 0
        while len(sortedCandidateList) > 0:
            # start = time.time()
            candidate = self._selectCandidate(sortedCandidateList)
            sortedCandidateList.remove(candidate)
            if solution.isCandidateFeasible(candidate):
                solution.assign(candidate)

            # solution.assign(candidate)
            # candidateList = solution.findFeasibleBidWins()
            # end = time.time()
            # if count % 100 == 0:
            #     print('Greedy iteration: %d, candidateList size: %d, time: %f secs' % (count, len(candidateList), end - start))
            count += 1

        if not solution.isComplete():
            solution.makeInfeasible()
        return solution
        
    def solve(self, **kwargs):
        self.startTimeMeasure()

        solver = kwargs.get('solver', None)
        if solver is not None:
            self.config.solver = solver
        localSearch = kwargs.get('localSearch', None)
        if localSearch is not None:
            self.config.localSearch = localSearch

        self.writeLogLine(float('inf'), 0)

        solution = self.construction()
        if self.config.localSearch:
            localSearch = LocalSearch(self.config, None)
            endTime= self.startTime + self.config.maxExecTime
            solution = localSearch.solve(solution=solution, startTime=self.startTime, endTime=endTime)

        self.elapsedEvalTime = time.time() - self.startTime
        self.numSolutionsConstructed = 1
        if self.config.localSearch:
            self.numSolutionsConstructed += localSearch.localIterations
        self.writeLogLine(solution.getFitness(), self.numSolutionsConstructed)
        self.printPerformance()

        return solution


