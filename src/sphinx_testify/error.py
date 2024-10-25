from sphinx.errors import SphinxError


class TestNotFoundError(SphinxError):
    __test__ = False

    def __init__(self, test_name: str):
        super().__init__(
            f"Could not find test \"{test_name}\""
        )
