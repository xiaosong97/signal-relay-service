import os
import pytest
from fastapi.testclient import TestClient

# 强制使用 test 环境（内存 SQLite），必须在导入app.main之前设置
os.environ["APP_ENV"] = "test"

from app.main import app  # noqa: E402


@pytest.fixture
def client():
    """
    每个 test 使用一个全新的 TestClient
    """
    with TestClient(app) as c:
        yield c


def test_health_check(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_create_and_list_events(client):
    # 1. 创建事件
    payload = {
        "type": "test_event",
        "payload": {"msg": "hello test"},
    }

    resp = client.post("/events", json=payload)
    assert resp.status_code == 200

    data = resp.json()
    assert data["type"] == "test_event"
    assert data["payload"]["msg"] == "hello test"
    assert "id" in data

    # 2. 查询事件
    resp = client.get("/events")
    assert resp.status_code == 200

    items = resp.json()
    assert isinstance(items, list)
    assert len(items) == 1
    assert items[0]["type"] == "test_event"
