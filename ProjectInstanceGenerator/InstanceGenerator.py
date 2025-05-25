'''
AMMM P2 Instance Generator v2.0
Instance Generator class.
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

import os, random
from AMMMGlobals import AMMMException


class InstanceGenerator(object):
    # Generate instances based on read configuration.

    def __init__(self, config):
        self.config = config

    def generate(self):
        instancesDirectory = self.config.instancesDirectory
        fileNamePrefix = self.config.fileNamePrefix
        fileNameExtension = self.config.fileNameExtension
        numInstances = self.config.numInstances

        numUsers = self.config.numUsers
        probabilityOfBid = self.config.probabilityOfBid
        minBid = self.config.minBid
        maxBid = self.config.maxBid

        if not os.path.isdir(instancesDirectory):
            raise AMMMException('Directory(%s) does not exist' % instancesDirectory)

        for i in range(numInstances):
            instancePath = os.path.join(instancesDirectory, '%s.%d.%s' % (fileNamePrefix, i, fileNameExtension))
            fInstance = open(instancePath, 'w')

            # cpuCapacity = [0] * numCPUs
            # for c in range(numCPUs):
            #     cpuCapacity[c] = random.uniform(minCapacityPerCPU, maxCapacityPerCPU)

            # taskResources = [0] * numTasks
            # for t in range(numTasks):
            #     taskResources[t] = random.uniform(minResourcesPerTask, maxResourcesPerTask)

            fInstance.write('N = %d;\n' % numUsers)

            bidMatrix = []
            # users can not bid against themselves, so bidMatrix[i][i] = 0 for all i
            # each pair of different users i and j, will bid with probabilityOfBid
            # if two users i,j bid, their bid against the other user bidMatrix[i][j] and bidMatrix[j][i] will be a random float between minBid and maxBid.
            # similar to the Erdos-Renyi model, we will generate a random graph with a given probability of bid
            for i in range(numUsers):
                bidMatrix.append([0] * numUsers)

            for i in range(numUsers):
                for j in range(i+1, numUsers):
                    if random.random() < probabilityOfBid:
                        biditoj = random.uniform(minBid, maxBid)
                        bidMatrix[i][j] = biditoj
                        bidjtoi = random.uniform(minBid, maxBid)
                        bidMatrix[j][i] = bidjtoi

            fInstance.write('m = [\n')
            for i in range(numUsers):
                fInstance.write('    [  ')
                for j in range(numUsers):
                    fInstance.write(str(bidMatrix[i][j]))
                    fInstance.write('  ')
                fInstance.write(']\n')
            fInstance.write('];\n')


            fInstance.close()
