.. role:: code-py(code)
   :language: Python

Sphinx Testify
##############

``sphinx-testify`` is an extension to Sphinx that allows
:ref:`testifying documentation <testified-documentation>`:
ensuring that the documentation is up-to-date an aligned with the
library or application capabilities.


.. toctree::
   :maxdepth: 2
   :caption: Contents:
   :hidden:

   self
   testified-documentation

Installation
============

To install, run

.. code-block:: shell

   pip install sphinx-testify


Or get it from the source at https://github.com/basicwolf/sphinx-testify

Basic configuration
===================

.. testify::

   pytest.tests.test_sphinx_testify.test_basic_configuration

To enable ``sphinx-testify``, add it to the list of extensions in Sphinx project
``conf.py`` and add a path to JUnit XML -formatted tests result file. For example:

.. code-block:: python

   extensions = [
       'sphinx_testify'
   ]

   testify_from = [
       '/path/to/test_results.xml'
   ]


Usage
=====

``Sphinx-testify`` provides a Sphinx directive, which verifies
whether the given test succeeded and fails the documentation build
otherwise.

For example, consider a test which verifies that only registered users
can access the system.
The test results are available in JUnit XML format:

.. code-block:: xml

   <?xml version="1.0" encoding="utf-8"?>
   <testsuites>
       <testsuite name="testsuite">
           <testcase classname="testclass"
                     name="test_only_registered_users_have_access" />
       </testsuite>
   </testsuites>

You document and testify this behaviour via Sphinx as follows:

.. code-block:: rest

   Access to the system is restricted to registered users.

   .. testify::
      testsuite.testclass.test_only_registered_users_have_access

.. testify::
   pytest.tests.test_sphinx_testify.test_testify_single_passed_test_case

The directive is not rendered and does not affect the output HTML in any way.
However, documentation build fails if the specified test failed or
is missing from the test results XML report.

.. testify::
   pytest.tests.test_sphinx_testify.test_raise_error_when_test_result_not_found
   pytest.tests.test_sphinx_testify.test_raise_error_when_test_failed


A full example
--------------

Sphinx-testify does what it preaches: this very documentation is testified!
You can find out more by reading the
`source code <https://github.com/basicwolf/sphinx-testify/blob/master/docs/source/index.rst?plain=1>`_.


Test report parser
==================

The test report parser module consumes JUnit XML -formatted reports.
It aims at parsing the most common output and ignore all the unnecessary
data.

The test names used for testifying are constructed from Test Suite, Test Class
and Test Case names separated by a dot.
For example, we need to use the following long name to testify

.. code-block:: rest

  .. testify::
     pytest.tests.test_report_parser.test_parse_one_successful_testcase

based on the following ``<testcase>`` element in the report:

.. code-block:: xml

    <testsuite name="pytest">
        <testcase classname="tests.test_report_parser"
                  name="test_parse_one_successful_testcase"/>
    </testsuite>

.. testify::
   pytest.tests.test_report_parser.test_parse_one_successful_testcase

The parser can consume nested ``<testsuite>`` elements and normalizes testcase
names, so that for the following test report

.. code-block:: xml

    <testsuite name="Tests.Authentication">
        <testcase name="testCase3" classname="Tests.Authentication" />
    </testsuite>

it is enough to specify

.. code-block:: rest

  .. testify::
     Tests.Authentication.testCase3

.. testify::
   pytest.tests.test_report_parser.test_normalize_testcase_names

The parser is also tolerant for missing attributes, such as
``name`` attribute in ``<testsuite>`` or ``classname`` attribute in
``<testcase>``. However, testify raises an error if ``<testcase>`` is missing
``name`` attribute.

.. testify::
   pytest.tests.test_report_parser.test_raise_if_testcase_name_is_missing
   pytest.tests.test_report_parser.test_parse_with_missing_testsuite_name_and_testcase_classname


Configuration parameters
========================

.. confval:: testify_from
   :type: :code-py:`list[str]`

   The list of paths to test report files. The list should contain at least
   one entry.

   .. testify::
      pytest.tests.test_sphinx_testify.test_testify_from_many_sources
      pytest.tests.test_sphinx_testify.test_pass_when_testify_from_config_parameter_is_missing


.. confval:: testify_skip
   :type: :code-py:`bool`
   :default: :code-py:`False`

   Completely skip verifying testified sources. This is useful in environments
   where you are building documentation, but running tests is not feasible.

   For example, you can run tests and build documentation in CI to testify it,
   and skip tests and testifying in ReadTheDocs builder.

   Example:

   .. code-block:: python

      testify_skip = os.environ.get('READTHEDOCS') == 'True'

   .. testify::
      pytest.tests.test_sphinx_testify.test_skip_testifying
