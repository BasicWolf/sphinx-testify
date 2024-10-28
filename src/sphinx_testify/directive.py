from xml.etree import ElementTree

from docutils import nodes
from sphinx.application import Sphinx
from sphinx.util.docutils import SphinxDirective
from sphinx.util.logging import getLogger
from sphinx.util.typing import ExtensionMetadata

from .error import TestFailedError, TestNotFoundError
from .test_result import TestFailure, TestResult, TestResults


log = getLogger(__file__)


class TestifyDirective(SphinxDirective):
    """TODO"""

    has_content = True

    def run(self) -> list[nodes.Node]:
        for test_name in self.content:
            try:
                test_result = self.test_results[test_name]
            except KeyError:
                raise TestNotFoundError(test_name)

            if len(test_result.failures) > 0:
                raise TestFailedError(test_name)

            self.env.app.emit('testify-testified', test_result)

        self._force_reread()
        return []

    @property
    def test_results(self) -> TestResults:
        return getattr(self.env, 'testify_test_results', TestResults.empty())

    def _force_reread(self):
        env = self.state.document.settings.env
        env.note_reread()


def setup(app: Sphinx) -> ExtensionMetadata:
    app.add_config_value(
        'testify_from',
        default=[],
        rebuild='env',
        types=[list[str]],
        description=("List of testing result files paths."
                     " The results should be in JUnit XML format")
    )
    app.add_directive('testify', TestifyDirective)
    app.add_event('testify-testified')

    app.connect('builder-inited', _on_builder_inited)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }


def _on_builder_inited(app: Sphinx):
    test_results = _parse_tests_results_xml(app.config.testify_from)
    setattr(app.env, 'testify_test_results', test_results)


def _parse_tests_results_xml(testify_from: list[str]) -> TestResults:
    test_results = TestResults.empty()

    for path in testify_from:
        log.debug('Parsing Tests result from %s', path)
        tree = ElementTree.parse(path)
        root = tree.getroot()
        for testsuite_elem in root.iter('testsuite'):
            testsuite_name = testsuite_elem.get('name')
            for testcase_elem in testsuite_elem.iter('testcase'):
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
