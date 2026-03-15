import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    # Arrange: No special setup needed
    
    # Act: Make a GET request to /activities
    response = client.get("/activities")
    
    # Assert: Check the response status and structure
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "description" in data["Chess Club"]
    assert "participants" in data["Chess Club"]

def test_signup_for_activity():
    # Arrange: No special setup needed
    
    # Act: Attempt to sign up a new participant
    response = client.post("/activities/Chess Club/signup?email=test@mergington.edu")
    
    # Assert: Check the signup response
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Signed up test@mergington.edu for Chess Club" in data["message"]
    
    # Act: Fetch activities to verify the participant was added
    response = client.get("/activities")
    
    # Assert: Verify the participant is in the list
    data = response.json()
    assert "test@mergington.edu" in data["Chess Club"]["participants"]

def test_signup_already_signed_up():
    # Arrange: Sign up a participant first
    client.post("/activities/Chess Club/signup?email=duplicate@mergington.edu")
    
    # Act: Try to sign up the same participant again
    response = client.post("/activities/Chess Club/signup?email=duplicate@mergington.edu")
    
    # Assert: Check for the expected error
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "already signed up" in data["detail"]

def test_signup_activity_not_found():
    # Arrange: No special setup needed
    
    # Act: Try to sign up for a non-existent activity
    response = client.post("/activities/Nonexistent Activity/signup?email=test@mergington.edu")
    
    # Assert: Check for the expected error
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Activity not found" in data["detail"]

def test_unregister_from_activity():
    # Arrange: Sign up a participant first
    client.post("/activities/Programming Class/signup?email=unregister@mergington.edu")
    
    # Act: Unregister the participant
    response = client.delete("/activities/Programming Class/signup?email=unregister@mergington.edu")
    
    # Assert: Check the unregister response
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Unregistered unregister@mergington.edu from Programming Class" in data["message"]
    
    # Act: Fetch activities to verify the participant was removed
    response = client.get("/activities")
    
    # Assert: Verify the participant is no longer in the list
    data = response.json()
    assert "unregister@mergington.edu" not in data["Programming Class"]["participants"]

def test_unregister_not_signed_up():
    # Arrange: No special setup needed
    
    # Act: Try to unregister a participant who is not signed up
    response = client.delete("/activities/Chess Club/signup?email=notsigned@mergington.edu")
    
    # Assert: Check for the expected error
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "not signed up" in data["detail"]

def test_unregister_activity_not_found():
    # Arrange: No special setup needed
    
    # Act: Try to unregister from a non-existent activity
    response = client.delete("/activities/Nonexistent Activity/signup?email=test@mergington.edu")
    
    # Assert: Check for the expected error
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Activity not found" in data["detail"]

def test_root_redirect():
    # Arrange: No special setup needed
    
    # Act: Make a GET request to the root
    response = client.get("/")
    
    # Assert: Check that it redirects (note: TestClient may not fully handle static file redirects)
    assert response.status_code == 200