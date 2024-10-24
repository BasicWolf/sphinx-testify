from xml.etree import ElementTree

from docutils import nodes
from sphinx.application import Sphinx
from sphinx.util.docutils import SphinxDirective
from sphinx.util.logging import getLogger
from sphinx.util.typing import ExtensionMetadata

log = getLogger(__file__)


class TestifyDirective(SphinxDirective):
    """TODO"""

    has_content = True

    def run(self) -> list[nodes.Node]:
        for test_name in self.content:
            if test_name in getattr(self.env, 'testify_test_names'):
                self.env.app.emit('testify-testified', test_name)

        self._force_reread()
        return []

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
                     " The results should be in JUnit XML format""")
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
    setattr(app.env, 'testify_test_names', test_results)


def _parse_tests_results_xml(testify_from: list[str]) -> list[str]:
    test_names = []

    for path in testify_from:
        log.debug('Parsing Tests result from %s', path)
        tree = ElementTree.parse(path)
        root = tree.getroot()
        for testsuite_elem in root.iter('testsuite'):
            testsuite_name = testsuite_elem.get('name')
            for testcase_elem in testsuite_elem.iter('testcase'):
                test_class_name = testcase_elem.get('classname')
                test_name = testcase_elem.get('name')
                test_names.append(
                    f'{testsuite_name}.{test_class_name}.{test_name}'
                )
    return test_names
