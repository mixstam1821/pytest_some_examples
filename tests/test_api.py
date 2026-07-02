"""
Testing a FastAPI service with TestClient - relevant if the interview
touches your Xenia backend work.
"""


def test_health_check(api_client):
    response = api_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_get_known_product(api_client):
    response = api_client.get("/products/MTG-FCI-001")
    assert response.status_code == 200
    body = response.json()
    assert body["instrument"] == "FCI"


def test_get_unknown_product_returns_404(api_client):
    response = api_client.get("/products/DOES-NOT-EXIST")
    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"
