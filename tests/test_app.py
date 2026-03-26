import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    # Arrange: (No setup needed, just use the client)
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_and_prevent_duplicate():
    # Arrange
    activity = "Chess Club"
    email = "testuser@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]
    # Act (again): intentar registrar el mismo email
    response_dup = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert response_dup.status_code == 400
    assert "Student already signed up for this activity" in response_dup.json()["detail"]

def test_remove_participant():
    # Arrange
    activity = "Chess Club"
    email = "testuser@mergington.edu"
    # Act
    response = client.delete(f"/activities/{activity}/participant", params={"email": email})
    # Assert
    assert response.status_code == 200
    assert f"Removed {email}" in response.json()["message"]
    # Act: intentar eliminar de nuevo
    response_not_found = client.delete(f"/activities/{activity}/participant", params={"email": email})
    # Assert
    assert response_not_found.status_code == 404
    assert "Participant not found" in response_not_found.json()["detail"]

def test_signup_activity_not_found():
    # Arrange
    activity = "Nonexistent Club"
    email = "nobody@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]

def test_remove_participant_activity_not_found():
    # Arrange
    activity = "Nonexistent Club"
    email = "nobody@mergington.edu"
    # Act
    response = client.delete(f"/activities/{activity}/participant", params={"email": email})
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
