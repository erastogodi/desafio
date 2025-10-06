def test_register_and_login_flow(client):
    r = client.post("/auth/register", json={
        "username": "alice",
        "email": "alice@example.com",
        "password": "s3nh4"
    })
    assert r.status_code in (200, 201)
    r = client.post("/auth/login", json={
        "username_or_email": "alice",
        "password": "s3nh4"
    })
    assert r.status_code == 200
    assert "access_token" in r.json()
