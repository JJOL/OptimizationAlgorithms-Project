from dataclasses import dataclass
from executors import ExecResults, ExecTimes

@dataclass
class ReportResult:
    problem_size: str
    solver: str
    results: ExecResults
    times: ExecTimes

def render_report(
        report_results: list[ReportResult],
        problem_sizes: list[str],
        solvers: list[str]):
    
    print('Making report...')
    print('Problem Instances:', problem_sizes)
    print('Solvers:', solvers)

    for result in report_results:
        print(f'-----{result.solver}.{result.problem_size}-----')
        print(f'> Best Score: {result.results.obj_value} in {result.times.time_secs} secs')