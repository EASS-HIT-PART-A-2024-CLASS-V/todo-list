import pytest
from unittest.mock import patch, MagicMock
from app import add_task, update_task

API_BASE_URL = "http://localhost:8080"


class MockResponse:
    def __init__(self, status_code):
        self.status_code = status_code


@pytest.fixture
def mock_client(mocker):
    mock_response = MagicMock()
    mock_response.status_code = 200
    with patch('httpx.Client') as MockClient:
        mock_instance = MockClient.return_value.__enter__.return_value
        mock_instance.post.return_value = mock_response
        mock_instance.put.return_value = mock_response
        yield mock_instance


def test_add_task(mock_client):
    status_code = add_task("Test Title", "Test Description", "High", "2023-01-01")
    assert status_code == 200
    mock_client.post.assert_called_once_with(f"{API_BASE_URL}/todo/addtask", json={
        "title": "Test Title",
        "description": "Test Description",
        "priority": "High",
        "due_date": "2023-01-01"
    })


def test_update_task(mock_client):
    status_code = update_task(0, "Updated Title", "Updated Description", "Medium", "2023-02-01")
    assert status_code == 200
    mock_client.put.assert_called_once_with(f"{API_BASE_URL}/todo/updatesingletask", json={
        "id": 0,
        "title": "Updated Title",
        "description": "Updated Description",
        "priority": "Medium",
        "due_date": "2023-02-01"
    })