from __future__ import annotations

from dataclasses import dataclass


class TestResults:
    __test__ = False

    _results: dict[str, TestResult]

    def __init__(self):
        self._results = {}

    @staticmethod
    def empty() -> TestResults:
        return TestResults()

    def add(self, test_result: TestResult):
        self._results[test_result.name] = test_result

    def __getitem__(self, test_name: str) -> TestResult:
        return self._results[test_name]


@dataclass
class TestResult:
    __test__ = False

    name: str
    failures: list[TestFailure]


@dataclass
class TestFailure:
    __test__ = False

    message: str = ''
    type: str = ''
