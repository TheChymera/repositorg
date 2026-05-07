# tests/conftest.py
from pathlib import Path
import pytest

@pytest.fixture
def example_data():
    return Path(__file__).parent / "example_data"
