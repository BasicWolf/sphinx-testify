# Copyright: (c) 2024, Zaur Nasibov <zaur@zaurnasibov.com>
# GNU General Public License v3.0+
# See COPYING or https://www.gnu.org/licenses/gpl-3.0.txt

from __future__ import annotations

import logging

from pathlib import Path

import pytest
from sphinx.config import Config
from sphinx.testing.util import SphinxTestApp
from sphinx.errors import ExtensionError
from sphinx_testify.test_result import TestResult

log = logging.getLogger(__file__)

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
    _testified: set[str]

    def __init__(self, app: SphinxTestApp):
        self._app = app
        self._testified = set()
        try:
            self._app.connect('testify-testified', self._on_testified)
        except ExtensionError:
            log.warning(
                "Unable to listen to `testify-testified` event. "
                "NOTE: This might be intentional."
            )

    def _on_testified(self, _app, test_result: TestResult):
        self._testified.add(test_result.name)

    def build(self):
        self._app.build(filenames=[str(self._app.srcdir / 'index.rst')])

    def has_testified(self, *test_names: str) -> bool:
        return bool(set(test_names) & self._testified)

    def did_not_testify(self) -> bool:
        return self._testified == set()

    @property
    def config(self) -> Config:
        return self._app.config
