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
    pass