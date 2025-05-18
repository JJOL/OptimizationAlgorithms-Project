"""
AMMM Lab Heuristics
Instance file validator v2.0
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

from AMMMGlobals import AMMMException


# Validate instance attributes read from a DAT file.
# It validates the structure of the parameters read from the DAT file.
# It does not validate that the instance is feasible or not.
# Use Problem.checkInstance() function to validate the feasibility of the instance.
class ValidateInputData(object):
    @staticmethod
    def validate(data):
        # Validate that all input parameters were found
        for paramName in ['N', 'm']:
            if paramName not in data.__dict__:
                raise AMMMException('Parameter/Set(%s) not contained in Input Data' % str(paramName))

        # Validate nTasks
        N = data.N
        if not isinstance(N, int) or (N <= 0):
            raise AMMMException('N(%s) has to be a positive integer value.' % str(N))

        # Validate rt
        data.m = list(data.m)
        m = data.m
        if len(m) != N:
            raise AMMMException('Size of m(%d) does not match with value of N(%d).' % (len(m), N))
        for i in range(N):
            m[i] = list(m[i])
            if len(m[i]) != N:
                raise AMMMException('Size of m[%d](%d) does not match with value of N(%d).' % (i, len(m), N))

        for row in m:
            for value in row:
                if not isinstance(value, (int, float)) or (value < 0):
                    raise AMMMException('Invalid parameter value(%s) in m. Should be a float greater or equal than zero.' % str(value))

