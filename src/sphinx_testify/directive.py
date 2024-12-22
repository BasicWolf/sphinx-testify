# Copyright: (c) 2024, Zaur Nasibov <zaur@zaurnasibov.com>
# GNU General Public License v3.0+
# See COPYING or https://www.gnu.org/licenses/gpl-3.0.txt

from typing import LiteralString
from docutils import nodes
from sphinx.application import Sphinx
from sphinx.util.docutils import SphinxDirective
from sphinx.util.logging import getLogger
from sphinx.util.typing import ExtensionMetadata

from .error import TestFailedError, TestNotFoundError
from .report_parser import parse_tests_results_xml
from .test_result import TestResults


log = getLogger(__file__)


class TestifyDirective(SphinxDirective):
    """Directive to testify documentation.

    The body of the directive are test names separated by newline.
    The test names correlate to their names in a JUnit-formatted
    testing report.

    For example:

    .. testify::
       pytest.tests.test_sphinx_testify.test_raise_error_when_test_result_not_found
       pytest.tests.test_sphinx_testify.test_raise_error_when_test_failed
    """

    DIRECTIVE_NAME: LiteralString = "testify"

    has_content = True

    def run(self) -> list[nodes.Node]:
        if self.testify_skip:
            return []

        for test_name in self.content:
            try:
                test_result = self.test_results[test_name]
            except KeyError:
                raise TestNotFoundError(test_name)

            if test_result.has_failed():
                raise TestFailedError(test_name)

            self.env.app.emit('testify-testified', test_result)

        self._force_reread()
        return []

    @property
    def test_results(self) -> TestResults:
        return getattr(self.env, 'testify_test_results', TestResults.empty())

    @property
    def testify_skip(self) -> bool:
        return self.env.config.testify_skip

    def _force_reread(self):
        env = self.state.document.settings.env
        env.note_reread()


def setup(app: Sphinx) -> ExtensionMetadata:
    app.add_config_value(
        'testify_from',
        default=[],
        rebuild='env',
        types=[list[str]],
        description=("List of testing result files paths. "
                     "The results should be in JUnit XML format")
    )
    app.add_config_value(
        'testify_skip',
        default=False,
        rebuild='env',
        types=[bool],
        description=(
            "Completely skip testifying. This can be used to avoid "
            "testifying in environments that can not run tests before "
            "building the output document."
        )
    )

    app.add_directive(TestifyDirective.DIRECTIVE_NAME, TestifyDirective)
    app.add_event('testify-testified')

    app.connect('builder-inited', _on_builder_inited)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }


def _on_builder_inited(app: Sphinx):
    if app.config.testify_skip:
        log.info(
            "I will skip testifying documentation: "
            "testify_skip configuration parameter is True"
        )
        return

    if not app.config.testify_from:
        log.warning(
            "`testify_from` configuration parameter is not set or empty."
        )

    test_results = parse_tests_results_xml(app.config.testify_from)
    setattr(app.env, 'testify_test_results', test_results)
