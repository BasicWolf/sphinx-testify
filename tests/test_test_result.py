import pytest

from sphinx_testify.test_result import TestFailure, TestResult


def test_test_result_did_not_fail(successful_test_result):
    assert not successful_test_result.has_failed()


def test_test_result_has_failed(failed_test_result):
    assert failed_test_result.has_failed()


@pytest.fixture
def failed_test_result() -> TestResult:
    return TestResult(
        name='no-matter',
        failures=[
            TestFailure('no-matter', 'no-matter')
        ]
    )


@pytest.fixture
def successful_test_result() -> TestResult:
    return TestResult(
        name='no-matter',
        failures=[]
    )
