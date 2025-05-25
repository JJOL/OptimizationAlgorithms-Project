from dataclasses import dataclass
from executors import ExecResults, ExecTimes
import pandas as pd

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

    report_data = []

    for result in report_results:
        print(f'-----{result.solver}.{result.problem_size}-----')
        print(f'> Best Score: {result.results.obj_value} in {result.times.time_secs} secs')
        report_data.append({
            'Problem Size': result.problem_size,
            'Solver': result.solver,
            'Best Score': result.results.obj_value,
            'Execution Time (secs)': result.times.time_secs
        })

    # df = pd.DataFrame(report_data)
    # df = df.pivot(index='Problem Size', columns='Solver', values=['Best Score', 'Execution Time (secs)'])
    # df.columns = [f'{col[1]} ({col[0]})' for col in df.columns]
    # df = df.reset_index()
    # # save df to csv
    # df.to_csv('report.csv', index=False)