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
