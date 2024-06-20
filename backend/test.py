from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_add_task():
    global task_json_for_tests
    response = client.post("/todo/addtask?title=test&description=test&priority=3&due_date=2024-12-31")
    assert response.status_code == 200
    assert response.json()["title"] == "test"


def test_get_single_task():
    response = client.get("/todo/getsingletask?id=0")
    assert response.status_code == 200
    assert response.json()["title"] == "test"


def test_get_full_list():
    response = client.get("/todo/getfullist")
    assert response.status_code == 200


def test_update_task():
    response = client.put("/todo/updatesingletask?id=0&priority=1&due_date=2024-12-30")
    assert response.status_code == 200
    assert response.json()["priority"] == "1"


def test_delete_single_task():
    response = client.delete("/todo/deletesingletask?id=0")
    assert response.status_code == 200


def test_delete_all_list():
    response = client.delete("/todo/deletefulllist")
    assert response.status_code == 200
