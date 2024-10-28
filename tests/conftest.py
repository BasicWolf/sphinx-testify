from __future__ import annotations

from pathlib import Path

import pytest
from sphinx.testing.util import SphinxTestApp

from sphinx_testify.test_result import TestResult

pytest_plugins = ('sphinx.testing.fixtures',)

# Exclude 'fixtures' dirs for pytest test collector
collect_ignore = ['fixtures']


@pytest.fixture(scope='session')
def rootdir() -> Path:
    return Path(__file__).parent.resolve() / 'fixtures'


@pytest.fixture
def test_app(app: SphinxTestApp) -> TestifySphinxTestApp:
    return TestifySphinxTestApp(app)


class TestifySphinxTestApp:
    __test__ = False
    _app: SphinxTestApp
    _testified: list[str]

    def __init__(self, app: SphinxTestApp):
        self._app = app
        self._testified = []
        self._app.connect('testify-testified', self._on_testified)

    def _on_testified(self, _app, test_result: TestResult):
        self._testified.append(test_result.name)

    def build(self):
        self._app.build(filenames=[str(self._app.srcdir / 'index.rst')])

    def has_testified(self, test_name) -> bool:
        return test_name in self._testified
