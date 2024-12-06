This is the list of tests that have not yet been automated.



### testify_from configuration is empty/missing

**What should happen?**
Log a warning when `testify_from` configuration parameter is empty or missing.

We expect that `testify_from` should containt at least one entry with
path to a test report file. However, it can be empty when the documentation
has just been established and there are no test reports available.
A warning explicitly reminds to fulfil it later.

**Why can't we automate?**
For some reason, I wasn't able to make pytest's caplog fixture to capture logs
from Sphinx.

**How to test?**
Delete the configuration parameter from the `conf.py` and ensure that the
warning message appears.
