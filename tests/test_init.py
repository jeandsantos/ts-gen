from importlib.metadata import version

import ts_gen


class TestVersion:
    def test_version_matches_installed_metadata(self) -> None:
        assert ts_gen.__version__ == version("ts-gen")
