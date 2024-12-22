# Copyright: (c) 2024, Zaur Nasibov <zaur@zaurnasibov.com>
# GNU General Public License v3.0+
# See COPYING or https://www.gnu.org/licenses/gpl-3.0.txt

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

    def __len__(self):
        return len(self._results)


@dataclass
class TestResult:
    __test__ = False

    name: str
    failures: list[TestFailure]

    def has_failed(self) -> bool:
        return len(self.failures) > 0


@dataclass
class TestFailure:
    __test__ = False

    message: str = ''
    type: str = ''
