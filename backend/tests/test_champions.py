from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_list_champions_success():
    resp = client.get("/api/champions")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) > 0

    champ = data[0]
    assert "id" in champ
    assert "name" in champ
    assert "title" in champ
    assert "tags" in champ
    assert isinstance(champ["tags"], list)

def test_get_champion_success():
    resp = client.get("/api/champions/karma")
    assert resp.status_code == 200
    champ = resp.json()

    assert champ["id"].lower() == "karma"
    assert "title" in champ
    assert "tags" in champ
    assert "lore" in champ
    assert "skins" in champ
    assert isinstance(champ["skins"], list)
    if champ["skins"]:
        skin = champ["skins"][0]
        assert "id" in skin
        assert "name" in skin
        assert "splash" in skin

def test_get_champion_not_found():
    resp = client.get("/api/champions/nopechampion")
    assert resp.status_code == 404
    body = resp.json()
    assert body["detail"] == "Champion 'nopechampion' not found"