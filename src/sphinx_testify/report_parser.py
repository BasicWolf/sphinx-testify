from xml.etree import ElementTree
from xml.etree.ElementTree import Element

from sphinx.util.logging import getLogger
from sphinx_testify.test_result import TestFailure, TestResult, TestResults

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
            testsuite_name = testsuite_elem.get('name')

            testcase_elements = (elem for elem in testsuite_elem
                                 if elem.tag == 'testcase')

            for testcase_elem in testcase_elements:
                test_class_name = testcase_elem.get('classname')
                test_name = testcase_elem.get('name')

                test_results.add(
                    TestResult(
                        name=f'{testsuite_name}.{test_class_name}.{test_name}',
                        failures=_parse_failures(testcase_elem)
                    )
                )

    return test_results


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
