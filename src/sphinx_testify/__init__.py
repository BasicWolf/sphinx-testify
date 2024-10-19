from docutils import nodes

from sphinx.application import Sphinx
from sphinx.util.docutils import SphinxDirective
from sphinx.util.typing import ExtensionMetadata


class TestifyDirective(SphinxDirective):
    """TODO"""

    has_content = True

    def run(self) -> list[nodes.Node]:
        print(f'Content detected {self.content}')
        env = self.state.document.settings.env
        self._force_reread()

        comment_node = comment('hello world', env.app.builder.name)
        return [comment_node]

    def _force_reread(self):
        env = self.state.document.settings.env
        env.note_reread()



def comment(text: str, builder_name: str):
    comment_start = '<!--'
    comment_end = '-->'
    return nodes.raw('', f'{comment_start} {text} {comment_end}', format=builder_name)


def setup(app: Sphinx) -> ExtensionMetadata:
    app.add_directive('testify', TestifyDirective)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
