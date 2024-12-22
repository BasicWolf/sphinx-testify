# Copyright: (c) 2024, Zaur Nasibov <zaur@zaurnasibov.com>
# GNU General Public License v3.0+
# See COPYING or https://www.gnu.org/licenses/gpl-3.0.txt

import pytest

from sphinx_testify import TestNotFoundError, TestFailedError
from .conftest import TestifySphinxTestApp


@pytest.mark.sphinx('html', testroot='basic-configuration')
def test_basic_configuration(test_app: TestifySphinxTestApp):
    test_app.build()


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
        match=(
            'Could not testify with "test_name_which_is_not_in_test_results" - '
            'I didn\'t find it among test results.\\n'
            'It could be a typo in test name, or test hierarchy names '
            '\\(modules, classes etc.\\).'
        )
    ):
        test_app.build()


@pytest.mark.sphinx('html', testroot='test-failed')
def test_raise_error_when_test_failed(test_app: TestifySphinxTestApp):
    with pytest.raises(
        TestFailedError,
        match='Test failed: "testsuite.testclass.a_test_which_should_have_passed"'
    ):
        test_app.build()


@pytest.mark.sphinx('html', testroot='skip-testify')
def test_skip_testifying(test_app: TestifySphinxTestApp):
    test_app.build()
    assert test_app.did_not_testify()


@pytest.mark.sphinx('html', testroot='many-sources')
def test_testify_from_many_sources(test_app: TestifySphinxTestApp):
    test_app.build()
    assert test_app.has_testified(
        'a_testsuite.a_testclass.a_test',
        'another_testsuite.another_testclass.another_test'
    )


@pytest.mark.sphinx('html', testroot='configuration-testify-from-parameter-missing')
def test_pass_when_testify_from_config_parameter_is_missing(
    test_app: TestifySphinxTestApp,
):
    test_app.build()
    assert test_app.config.testify_from == []
