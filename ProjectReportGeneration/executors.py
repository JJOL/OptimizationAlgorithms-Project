from dataclasses import dataclass
import os
import sys
from timeit import default_timer as timer
import subprocess

@dataclass
class ExecResults:
    obj_value: float

@dataclass
class ExecTimes:
    time_secs: float

def dat_file_assign(file_path: str, variable:str , value: str):
    with open(file_path, 'r') as file:
        file_lines = file.readlines()

    var_line = next(iter([(idx,line) for idx, line in enumerate(file_lines) if variable in line]), None)
    if var_line == None:
        sys.exit(f"Could not find matching line for variable '{variable}' in file at {file_path}")

    line_idx = var_line[0]
    line_str = var_line[1]
    left_side = line_str.split('=')[0] + '='
    new_line = left_side + ' ' + value + ';' + '\n'

    file_lines[line_idx] = new_line
    with open(file_path, 'w') as file:
        file.writelines(file_lines)

HEURISTICS_BASE = r'C:\Users\jjoul\Documents\UPC\AMMM\PythonCode\PythonCode\ProjectHeuristics'
def execute_python_solver(solver: str, instance_size: str) -> tuple[ExecResults, ExecTimes]:
    # Assign Input File and Solver
    config_file_path = os.path.join(HEURISTICS_BASE, r'config\config.dat')
    dat_file_assign(config_file_path, 'solver', solver)
    data_file = instance_size
    dat_file_assign(config_file_path, 'inputDataFile', os.path.join(HEURISTICS_BASE, '..', 'ProjectInstanceGenerator', 'output', data_file))

    # Execute
    sys.path.append(HEURISTICS_BASE)
    from datParser import DATParser
    from validateInputDataP2 import ValidateInputData
    from ValidateConfig import ValidateConfig
    from Main import Main

    config = DATParser.parse(config_file_path)
    ValidateConfig.validate(config)
    inputData = DATParser.parse(config.inputDataFile)
    ValidateInputData.validate(inputData)

    solver = Main(config)

    start = timer()

    solver.run(inputData)

    end = timer()
    print('Done.')

    solution_file_path = os.path.join(HEURISTICS_BASE, 'solutions', 'example.sol')
    sol = DATParser.parse(solution_file_path)

    return (ExecResults(sol.z), ExecTimes(end - start))

def execute_cplex_solver(instance_size: str) -> tuple[ExecResults, ExecTimes]:
    # Assign instance data file
    CPLEX_BASE = '..\\ProjectCPLEX'
    params_file_path = os.path.join(CPLEX_BASE, 'params.dat')
    dat_file_assign(params_file_path, 'dataFile', f"\"..\\\\ProjectInstanceGenerator\\\\output\\\\{instance_size}\"")


    start = timer()
    res = subprocess.run(['oplrun.exe', '..\\ProjectCPLEX\\main.mod', '..\\ProjectCPLEX\\params.dat'], timeout=60)
    end = timer()

    val = 0
    if res.returncode == 0:
        print('GOOD exeuction!')
        sys.path.append(HEURISTICS_BASE)
        from datParser import DATParser
        sol = DATParser.parse('..\\ProjectCPLEX\\solution.dat')
        val = sol.z

    return (ExecResults(val), ExecTimes(end - start))

def execute_search(solver: str, instance_size: str) -> tuple[ExecResults, ExecTimes]:
    print(f"Executing search with solver: {solver} and instance size: {instance_size}")

    if solver in ['Random', 'Greedy', 'GRASP', 'BRKGA']:
        print('Executing Heuristic Python Solver')
        return execute_python_solver(solver, instance_size)
    else:
        print('Executing MILP CPLEX Solver')
        return execute_cplex_solver(instance_size)


if __name__ == "__main__":
    # Example usage
    
    solver = sys.argv[1]
    problem_size = sys.argv[2]

    results, times = execute_search(solver, problem_size)

    print(f'Objective Value: {results.obj_value}')
    print(f'Execution Time: {times.time_secs:0.4f}s')