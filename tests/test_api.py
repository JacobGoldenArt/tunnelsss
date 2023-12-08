from fastapi.testclient import TestClient
from app.models.index import TunnelCreate, TunnelRead
from app.main import app
import logging

log = logging.getLogger(__name__)

client = TestClient(app)


def test_delete_blocks3():
    response = client.delete("/blocks/delete")
    assert response.status_code == 200


def test_delete_tunnel():
    response = client.delete("/tunnels/delete")
    assert response.status_code == 200


def test_create_tunnel():
    tunnel_test = TunnelCreate()
    response = client.post("/tunnels/create", json=tunnel_test.dict())
    assert response.status_code == 200


def test_read_tunnel():
    response = client.get("/tunnels")
    assert response.status_code == 200
    # 3assert response.json() == TunnelRead(id="tunnels:main", child_blocks=[])


def test_create_block():
    response = client.post(
        "/blocks/create",
        json={
            "name": "testbbb",
            "type": "testbbb",
        },
    )
    assert response.status_code == 200
    # data = response.json()
    # assert data[0]["name"] == "testbbb"
    # assert data[0]["type"] == "testbbb"


def test_delete_blocks():
    response = client.delete("/blocks/delete")
    assert response.status_code == 200
