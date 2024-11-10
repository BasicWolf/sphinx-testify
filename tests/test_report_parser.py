# Copyright: (c) 2024, Zaur Nasibov <zaur@zaurnasibov.com>
# GNU General Public License v3.0+
# See COPYING or https://www.gnu.org/licenses/gpl-3.0.txt

import os.path

import pytest

from sphinx_testify.report_parser import parse_tests_results_xml
from sphinx_testify.error import NameAttributeMissingError


def test_parse_one_successful_testcase(path_to):
    test_results = parse_tests_results_xml(path_to('one_successful_testcase.xml'))
    assert len(test_results) == 1
    assert test_results['testsuite.testclass.a_successful_test']


def test_parse_report_without_top_level_tag(path_to):
    test_results = parse_tests_results_xml(path_to('no_testsuites_element.xml'))
    assert len(test_results) == 1
    assert test_results['testsuite.testclass.a_successful_test']


def test_parse_with_missing_testsuite_name_and_testcase_classname(path_to):
    test_results = parse_tests_results_xml(
        path_to('missing_testsuite_name_and_testcase_classname.xml')
    )
    assert test_results['a_test']


def test_parse_nested_testsuites(path_to):
    test_results = parse_tests_results_xml(
        path_to('nested_testsuite_elements.xml')
    )
    assert len(test_results) == 8


def test_normalize_testcase_names(path_to):
    test_results = parse_tests_results_xml(
        path_to('testcases_with_full_class_names.xml')
    )
    assert test_results['Tests.Authentication.Login.testCase2'] is not None


def test_raise_if_testcase_name_is_missing(path_to):
    with pytest.raises(
        NameAttributeMissingError,
        match='"name" attribute is missing or empty in <testcase> tag'
    ):
        parse_tests_results_xml(
            path_to('missing_testcase_name.xml')
        )


@pytest.fixture(scope='module')
def path_to():
    fixtures_root = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'fixtures/test-reports/'
    )

    def _path_to(filename: str) -> str:
        return os.path.join(fixtures_root, filename)

    return _path_to
