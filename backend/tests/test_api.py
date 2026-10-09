from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to VerityAI API"}

# Note: Integration testing of database and auth requires test DB setup fixture.
# These will be expanded in Phase 2 with DB overrides.
def test_register_user_missing_fields():
    response = client.post("/api/v1/register", json={"email": "test@example.com"})
    assert response.status_code == 422 # Unprocessable Entity due to missing password
