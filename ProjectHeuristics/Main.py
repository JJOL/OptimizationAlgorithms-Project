"""
AMMM Lab Heuristics
Main function
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

from argparse import ArgumentParser
from pathlib import Path

import sys

from datParser import DATParser
from AMMMGlobals import AMMMException
from BRKGA_fwk.solver_BRKGA import Solver_BRKGA
from validateInputDataP2 import ValidateInputData
from ValidateConfig import ValidateConfig
from solvers.solver_Greedy import Solver_Greedy
from solvers.solver_GRASP import Solver_GRASP
from solvers.decoder_BRKGA import Decoder
from problem.instance import Instance


class Main:
    def __init__(self, config):
        self.config = config

    def run(self, data):
        try:
            if self.config.verbose: print('Creating Problem Instance...')
            instance = Instance(self.config, data)
            if self.config.verbose: print('Solving the Problem...')
            if instance.checkInstance():
                initialSolution = None
                if self.config.solver == 'Greedy' or self.config.solver == 'Random':
                    solver = Solver_Greedy(self.config, instance)
                elif self.config.solver == 'GRASP':
                    solver = Solver_GRASP(self.config, instance)
                elif self.config.solver == 'BRKGA':
                    verbose = self.config.verbose
                    self.config.verbose = False
                    greedy = Solver_Greedy(self.config, instance)
                    initialSolution = greedy.solve(solver='Greedy', localSearch=False)
                    self.config.verbose = verbose
                    decoder = Decoder(self.config, instance)
                    solver = Solver_BRKGA(decoder, instance)
                else:
                    raise AMMMException('Solver %s not supported.' % str(self.config.solver))
                solution = solver.solve(solution=initialSolution)
                # print('Solution (CPUid: [TasksId]): %s' % str(solution.cpuIdToListTaskId))
                solution.saveToFile(self.config.solutionFile)
            else:
                print('Instance is infeasible.')
                solution = instance.createSolution()
                solution.makeInfeasible()
                solution.saveToFile(self.config.solutionFile)
            return 0
        except AMMMException as e:
            print('Exception:', e)
            return 1


if __name__ == '__main__':
    parser = ArgumentParser(description='AMMM Lab Heuristics')
    parser.add_argument('-c', '--configFile', nargs='?', type=Path,
                        default=Path(__file__).parent / 'config/config.dat', help='specifies the config file')
    args = parser.parse_args()

    config = DATParser.parse(args.configFile)
    ValidateConfig.validate(config)
    inputData = DATParser.parse(config.inputDataFile)
    ValidateInputData.validate(inputData)

    if config.verbose:
        print('AMMM Lab Heuristics')
        print('-------------------')
        print('Config file %s' % args.configFile)
        print('Input Data file %s' % config.inputDataFile)

    main = Main(config)
    sys.exit(main.run(inputData))
    