import pytest

from test.conftest import TestifySphinxTestApp


@pytest.mark.sphinx('html', testroot='single-passed-test')
def test_testify_single_passed_test_case(test_app: TestifySphinxTestApp):
    test_app.build()

    assert test_app.has_testified(
        'testsuite.testclass.test_only_registered_users_have_access'
    )
