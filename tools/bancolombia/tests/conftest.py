import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))

from make_fixtures import DUMMY_PASSWORD, build_all  # noqa: E402


@pytest.fixture(scope="session")
def fixtures(tmp_path_factory):
    return build_all(tmp_path_factory.mktemp("statements"))


@pytest.fixture
def password_env(monkeypatch):
    monkeypatch.setenv("BANCOLOMBIA_PDF_PASSWORD", DUMMY_PASSWORD)
