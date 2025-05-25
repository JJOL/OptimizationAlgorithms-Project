'''
AMMM P2 Instance Generator v2.0
Config attributes validator.
Copyright 2020 Luis Velasco

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

from AMMMGlobals import AMMMException


class ValidateConfig(object):
    # Validate config attributes read from a DAT file.

    @staticmethod
    def validate(data):
        # Validate that mandatory input parameters were found
        paramList = ['instancesDirectory', 'fileNamePrefix', 'fileNameExtension', 'numInstances',
                      'numUsers', 'probabilityOfBid', 'maxBid', 'minBid']
        for paramName in paramList:
            if paramName not in data.__dict__:
                raise AMMMException('Parameter(%s) has not been not specified in Configuration' % str(paramName))

        instancesDirectory = data.instancesDirectory
        if len(instancesDirectory) == 0: raise AMMMException('Value for instancesDirectory is empty')

        fileNamePrefix = data.fileNamePrefix
        if len(fileNamePrefix) == 0: raise AMMMException('Value for fileNamePrefix is empty')

        fileNameExtension = data.fileNameExtension
        if len(fileNameExtension) == 0: raise AMMMException('Value for fileNameExtension is empty')

        numInstances = data.numInstances
        if not isinstance(numInstances, int) or (numInstances <= 0):
            raise AMMMException('numInstances(%s) has to be a positive integer value.' % str(numInstances))

        numUsers = data.numUsers
        if not isinstance(numUsers, int) or (numUsers <= 0):
            raise AMMMException('numUsers(%s) has to be a positive integer value.' % str(numUsers))
        
        probabilityOfBid = data.probabilityOfBid
        if not isinstance(probabilityOfBid, (int, float)) or (probabilityOfBid <= 0):
            raise AMMMException('probabilityOfBid(%s) has to be a positive float value.' % str(probabilityOfBid))

        if probabilityOfBid > 1:
            raise AMMMException('probabilityOfBid(%s) has to be less or equal to 1' % str(probabilityOfBid))

        maxBid = data.maxBid
        if not isinstance(maxBid, (int, float)) or (maxBid <= 0):
            raise AMMMException('maxBid(%s) has to be a positive float value.' % str(maxBid))

        minBid = data.minBid
        if not isinstance(minBid, (int, float)) or (minBid <= 0):
            raise AMMMException('minBid(%s) has to be a positive float value.' % str(minBid))

        if maxBid < minBid:
            raise AMMMException('maxBid(%s) has to be >= minBid(%s).' % (str(maxBid), str(minBid)))
