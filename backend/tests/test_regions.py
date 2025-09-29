from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_list_regions_ok():
    resp = client.get("/api/regions")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) > 0

    region = data[0]
    assert "id" in region
    assert "name" in region
    assert "description" in region or "champions" in region

def test_get_region_success():
    resp = client.get("/api/regions/ionia")
    assert resp.status_code == 200
    region = resp.json()

    assert region["id"].lower() == "ionia"
    assert "name" in region
    assert "description" in region

def test_get_region_404():
    resp = client.get("/api/regions/__nope__")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Region '__nope__' not found"