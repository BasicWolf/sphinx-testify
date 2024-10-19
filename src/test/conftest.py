import pytest
from pathlib import Path

pytest_plugins = ('sphinx.testing.fixtures',)

# Exclude 'fixtures' dirs for pytest test collector
collect_ignore = ['fixtures']


@pytest.fixture(scope='session')
def rootdir() -> Path:
    return Path(__file__).parent.resolve() / 'fixtures'
