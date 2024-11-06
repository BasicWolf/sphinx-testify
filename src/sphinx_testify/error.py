# Copyright: (c) 2024, Zaur Nasibov <zaur@zaurnasibov.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from sphinx.errors import SphinxError


class TestFailedError(SphinxError):
    __test__ = False

    def __init__(self, test_name: str):
        super().__init__(
            f"Test failed: \"{test_name}\""
        )


class NameAttributeMissingError(SphinxError):
    __test__ = False

    def __init__(self):
        super().__init__(
            "\"name\" attribute is missing or empty in <testcase> tag"
        )


class TestNotFoundError(SphinxError):
    __test__ = False

    def __init__(self, test_name: str):
        super().__init__(
            f"Could not find test \"{test_name}\""
        )
