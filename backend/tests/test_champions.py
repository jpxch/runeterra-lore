from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_list_champions_success():
    resp = client.get("/champions")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert all("id" in champ and "name" in champ for champ in data)

def test_get_champion_success():
    resp = client.get("/champions/karma")
    assert resp.status_code == 200
    champ = resp.json()
    assert champ["id"] == "karma"
    assert "name" in champ
    assert "lore" in champ

def test_get_champion_not_found():
    resp = client.get("/champions/nopechampion")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Champion 'nopechampion' not found"