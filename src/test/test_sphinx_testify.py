import pytest
from sphinx.testing.util import SphinxTestApp


@pytest.mark.sphinx('html', testroot='single-passed-test')
def test_testify_case(app: SphinxTestApp):
    testified_only_adult_users_have_access = False

    def _on_testified(_app, test_name: str):
        nonlocal testified_only_adult_users_have_access
        if test_name == 'asuite.aclass.test_only_adult_users_have_access':
            testified_only_adult_users_have_access = True
    app.connect('testify-testified', _on_testified)

    app.build(filenames=[str(app.srcdir / 'index.rst')])

    assert testified_only_adult_users_have_access
