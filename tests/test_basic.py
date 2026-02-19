import pytest
from fastapi.testclient import TestClient


def test_health_check():
    """测试健康检查接口"""
    from api.main import app
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
