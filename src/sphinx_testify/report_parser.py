from xml.etree import ElementTree

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

                failures = [
                    TestFailure(
                        message=failure_elem.get('message', ''),
                        type=failure_elem.get('type', '')
                    )
                    for failure_elem in testcase_elem.iterfind('failure')
                ]

                test_results.add(
                    TestResult(
                        name=f'{testsuite_name}.{test_class_name}.{test_name}',
                        failures=failures
                    )
                )

    return test_results
