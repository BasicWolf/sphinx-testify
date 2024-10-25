Sphinx Testify
==============

``Testify`` is an extension to Sphinx which enables
writing `TODO: testified documentation <http://example.com>`_.


.. toctree::
   :maxdepth: 2
   :caption: Contents:


``Testify`` provides a Sphinx directive, which verifies
whether the given unit tests succeeded and fails the documentation build
otherwise.


For example, a unit test verifies that only registered users
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

This behaviour is documented and testified as follows:

.. code-block:: rest

   Access to the system is restricted to registered users.

   .. testify::
      testsuite.testclass.test_only_registered_users_have_access

.. testify::
   pytest.tests.test_sphinx_testify.test_testify_single_passed_test_case

Testify raises an error if the test was not found, e.g. it is mispelled
or missing from the test results XML report.

.. testify::
   pytest.tests.test_sphinx_testify.test_raise_error_when_test_result_not_found

.. the test names are added to the document as target output comments (e.g. <!-- test_name --> in HTML)
.. the :warn: setting does not fail the test build
