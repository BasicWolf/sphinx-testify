import os.path

import pytest

from sphinx_testify.report_parser import parse_tests_results_xml


def test_parse_one_successful_testcase(path_to):
    test_results = parse_tests_results_xml(path_to('one_successful_testcase.xml'))
    assert len(test_results) == 1
    assert test_results['testsuite.testclass.a_successful_test']


def test_parse_report_without_top_level_tag(path_to):
    test_results = parse_tests_results_xml(path_to('no_testsuites_element.xml'))
    assert len(test_results) == 1
    assert test_results['testsuite.testclass.a_successful_test']


def test_parse_nested_testsuites(path_to):
    test_results = parse_tests_results_xml(
        path_to('nested_testsuite_elements.xml')
    )
    assert len(test_results) == 8


@pytest.fixture(scope='module')
def path_to():
    fixtures_root = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'fixtures/test-reports/'
    )

    def _path_to(filename: str) -> str:
        return os.path.join(fixtures_root, filename)

    return _path_to
