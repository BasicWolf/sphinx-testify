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


For example, a unit test verifies only the users of certain age can access the system.
The test results are available in JUnit XML format:

.. code-block:: xml

   <testcase
       classname="test"
       name="test_user_younger_than_18_cannot_log_in"/>

This behaviour is documented and testified as follows:

.. code-block:: rest

   Users under 18 are not allowed to log in.

   .. testify::
      test_user_younger_than_18_cannot_log_in

.. the test names are added to the document as target output comments (e.g. <!-- test_name --> in HTML)
.. the :warn: setting does not fail the test build
