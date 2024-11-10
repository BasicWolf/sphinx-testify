# Copyright: (c) 2024, Zaur Nasibov <zaur@zaurnasibov.com>
# GNU General Public License v3.0+
# See COPYING or https://www.gnu.org/licenses/gpl-3.0.txt

from xml.etree import ElementTree
from xml.etree.ElementTree import Element

from sphinx.util.logging import getLogger

from .error import NameAttributeMissingError
from .test_result import TestFailure, TestResult, TestResults

log = getLogger(__file__)


def parse_tests_results_xml(testify_from: str | list[str]) -> TestResults:
    test_results = TestResults.empty()

    if isinstance(testify_from, str):
        testify_from = [testify_from]

    for path in testify_from:
        log.debug('Parsing Tests result from %s', path)

        tree = ElementTree.parse(path)
        root = tree.getroot()

        for testsuite_elem in root.iter('testsuite'):
            testcase_elements = (elem for elem in testsuite_elem
                                 if elem.tag == 'testcase')

            for testcase_elem in testcase_elements:
                test_results.add(
                    _parse_test_result(testsuite_elem, testcase_elem)
                )

    return test_results


def _parse_test_result(
    testsuite_elem: Element,
    testcase_elem: Element
) -> TestResult:
    test_name = testcase_elem.get('name')
    if not test_name:
        raise NameAttributeMissingError()

    testsuite_name = testsuite_elem.get('name') or ''
    test_class_name = testcase_elem.get('classname') or ''

    test_name = _normalize_test_name(
        testsuite_name,
        test_class_name,
        test_name
    )
    test_failures = _parse_failures(testcase_elem)
    return TestResult(test_name, test_failures)


def _normalize_test_name(
    testsuite_name: str,
    test_class_name: str,
    test_name: str
) -> str:
    if test_class_name.startswith(testsuite_name):
        test_name_parts = [test_class_name, test_name]
    else:
        test_name_parts = [testsuite_name, test_class_name, test_name]
    non_empty_parts = filter(bool, test_name_parts)
    return '.'.join(non_empty_parts)


def _parse_failures(testcase_elem):
    return [
        _parse_failure(failure_elem)
        for failure_elem in testcase_elem.iterfind('failure')
    ]


def _parse_failure(elem: Element) -> TestFailure:
    return TestFailure(
        message=elem.get('message', ''),
        type=elem.get('type', '')
    )
