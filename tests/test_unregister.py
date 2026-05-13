"""
Tests for DELETE /activities/{activity_name}/unregister endpoint using AAA (Arrange-Act-Assert) pattern.
"""
import pytest


def test_unregister_participant_success(client):
    """
    Test successful removal of a participant from an activity.
    
    AAA Pattern:
    - Arrange: client ready, participant in activity
    - Act: call DELETE /activities/{activity}/unregister with participant email
    - Assert: response 200, participant removed from list
    """
    # Arrange
    activity_name = "Chess Club"
    email = "test_remove@mergington.edu"
    
    # First, sign up the participant
    client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    
    # Verify participant was removed
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email not in activities[activity_name]["participants"]


def test_unregister_activity_not_found(client):
    """
    Test unregister fails with 404 when activity doesn't exist.
    
    AAA Pattern:
    - Arrange: client ready, invalid activity name
    - Act: call DELETE with non-existent activity
    - Assert: response 404, detail message "Activity not found"
    """
    # Arrange
    invalid_activity = "Non Existent Activity"
    email = "student@mergington.edu"
    
    # Act
    response = client.delete(
        f"/activities/{invalid_activity}/unregister",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Activity not found"


def test_unregister_not_registered(client):
    """
    Test unregister fails with 400 when participant not in activity.
    
    AAA Pattern:
    - Arrange: client ready, participant not in activity
    - Act: call DELETE with non-registered email
    - Assert: response 400, detail message "Student not signed up for this activity"
    """
    # Arrange
    activity_name = "Basketball Team"
    email = "notregistered@mergington.edu"
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Student not signed up for this activity"


def test_unregister_and_resign_up(client):
    """
    Test that a student can unregister and sign up again.
    
    AAA Pattern:
    - Arrange: client ready, student signed up
    - Act: unregister, then sign up again
    - Assert: participant in list after second signup
    """
    # Arrange
    activity_name = "Gym Class"
    email = "toggle_signup@mergington.edu"
    
    # Sign up
    client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Act - unregister
    response1 = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    assert response1.status_code == 200
    
    # Act - sign up again
    response2 = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    assert response2.status_code == 200
    
    # Assert
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email in activities[activity_name]["participants"]
