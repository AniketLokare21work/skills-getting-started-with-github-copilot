"""
Tests for POST /activities/{activity_name}/signup endpoint using AAA (Arrange-Act-Assert) pattern.
"""
import pytest


def test_signup_new_student_success(client):
    """
    Test successful signup for a new student.
    
    AAA Pattern:
    - Arrange: client ready, activity exists, email not yet registered
    - Act: call POST /activities/Chess Club/signup with new email
    - Assert: response 200, participant added to list
    """
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity_name in data["message"]
    
    # Verify participant was added
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email in activities[activity_name]["participants"]


def test_signup_activity_not_found(client):
    """
    Test signup fails with 404 when activity doesn't exist.
    
    AAA Pattern:
    - Arrange: client ready, invalid activity name
    - Act: call POST with non-existent activity
    - Assert: response 404, detail message "Activity not found"
    """
    # Arrange
    invalid_activity = "Non Existent Activity"
    email = "student@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{invalid_activity}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Activity not found"


def test_signup_already_registered(client):
    """
    Test signup fails with 400 when student already signed up.
    
    AAA Pattern:
    - Arrange: client ready, participant already in activity
    - Act: call POST with same email twice
    - Assert: second response 400, detail message "Student already signed up"
    """
    # Arrange
    activity_name = "Chess Club"
    email = "duplicate@mergington.edu"
    
    # First signup (should succeed)
    client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Act - attempt duplicate signup
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Student already signed up"


def test_signup_multiple_students_same_activity(client):
    """
    Test multiple students can sign up for the same activity.
    
    AAA Pattern:
    - Arrange: client ready, activity exists
    - Act: sign up multiple students
    - Assert: all participants added successfully
    """
    # Arrange
    activity_name = "Programming Class"
    emails = ["student1@mergington.edu", "student2@mergington.edu", "student3@mergington.edu"]
    
    # Act
    for email in emails:
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        assert response.status_code == 200
    
    # Assert
    activities_response = client.get("/activities")
    activities = activities_response.json()
    for email in emails:
        assert email in activities[activity_name]["participants"]
