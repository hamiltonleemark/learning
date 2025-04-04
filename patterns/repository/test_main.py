"""
Unit test of main.
"""
import pytest
from main import Repository

# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=redefined-outer-name

class TestRepository:
    def __init__(self):
        self.data_store = {}

    def save(self, data: dict) -> None:
        self.data_store.update(data)

    def get_data(self):
        return self.data_store

@pytest.fixture
def repo():
    return TestRepository()

def test_save_single_item(repo):
    repo.save({'key1': 'value1'})
    assert repo.get_data() == {'key1': 'value1'}

def test_save_multiple_items(repo):
    repo.save({'key1': 'value1'})
    repo.save({'key2': 'value2'})
    assert repo.get_data() == {'key1': 'value1', 'key2': 'value2'}

def test_overwrite_item(repo):
    repo.save({'key1': 'value1'})
    repo.save({'key1': 'new_value'})
    assert repo.get_data() == {'key1': 'new_value'}

def test_save_empty_dict(repo):
    repo.save({})
    assert repo.get_data() == {}
