def test_health_endpoint(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert "vector_store_ready" in body
    assert "embedding_model" in body
    assert "gemini_model" in body
