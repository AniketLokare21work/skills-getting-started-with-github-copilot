"""
Tests for GET /activities endpoint using AAA (Arrange-Act-Assert) pattern.
"""
import pytest


def test_get_activities_success(client):
    """
    Test GET /activities returns all activities with correct structure.
    
    AAA Pattern:
    - Arrange: client is ready with activities loaded
    - Act: call GET /activities
    - Assert: response 200, activities dict returned, fields present
    """
    # Arrange
    # (client fixture handles setup)
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    activities = response.json()
    assert isinstance(activities, dict)
    assert len(activities) > 0
    
    # Verify each activity has required fields
    for activity_name, activity_details in activities.items():
        assert isinstance(activity_name, str)
        assert "description" in activity_details
        assert "schedule" in activity_details
        assert "max_participants" in activity_details
        assert "participants" in activity_details
        assert isinstance(activity_details["participants"], list)


def test_get_activities_contains_chess_club(client):
    """
    Test that activities list includes expected activity (Chess Club).
    
    AAA Pattern:
    - Arrange: client is ready
    - Act: call GET /activities
    - Assert: response contains Chess Club activity
    """
    # Arrange
    # (client fixture handles setup)
    
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    assert "Chess Club" in activities
    assert activities["Chess Club"]["description"] == "Learn strategies and compete in chess tournaments"
