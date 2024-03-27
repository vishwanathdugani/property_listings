from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_property_endpoint():
    response = client.post(
        "/properties/",
        json={
            "longitude": 123.456,
            "latitude": 78.910,
            "zip": "12345",
            "house_no": "123",
            "dir": "N",
            "street": "Main",
            "suffix": "St",
            "apt": "1A",
            "city": "Anytown"
        },
    )
    assert response.status_code == 201
    assert response.json()["zip"] == "12345"


def test_read_property_listings_endpoint():
    response = client.get("/properties_listings/")
    assert response.status_code == 200
    assert isinstance(response.json()["data"], list)
