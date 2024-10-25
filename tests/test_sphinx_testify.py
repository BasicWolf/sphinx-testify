import pytest

from sphinx_testify import TestNotFoundError
from .conftest import TestifySphinxTestApp


@pytest.mark.sphinx('html', testroot='single-passed-test')
def test_testify_single_passed_test_case(test_app: TestifySphinxTestApp):
    test_app.build()

    assert test_app.has_testified(
        'testsuite.testclass.test_only_registered_users_have_access'
    )


@pytest.mark.sphinx('html', testroot='test-missing-from-results')
def test_raise_error_when_test_result_not_found(test_app: TestifySphinxTestApp):
    with pytest.raises(
        TestNotFoundError,
        match='Could not find test "test_name_which_is_not_in_test_results"'
    ):
        test_app.build()
