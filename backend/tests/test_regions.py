from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_list_regions_ok():
    r = client.get("/regions")
    assert r.status_code == 200
    assert isinstance(r.json(), list)

def test_get_region_404():
    r = client.get("/regions/__nope__")
    assert r.status_code == 404