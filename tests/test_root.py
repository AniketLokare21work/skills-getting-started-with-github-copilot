"""
Tests for GET / endpoint using AAA (Arrange-Act-Assert) pattern.
"""
import pytest


def test_root_redirect_to_static(client):
    """
    Test GET / redirects to /static/index.html.
    
    AAA Pattern:
    - Arrange: client ready
    - Act: call GET / with follow_redirects=False
    - Assert: response 307 or 302, Location header points to /static/index.html
    """
    # Arrange
    # (client fixture handles setup)
    
    # Act
    response = client.get("/", follow_redirects=False)
    
    # Assert
    assert response.status_code in [307, 302]
    assert "location" in response.headers
    assert response.headers["location"] == "/static/index.html"


def test_root_redirect_with_follow(client):
    """
    Test GET / can be followed to reach redirect target.
    
    AAA Pattern:
    - Arrange: client ready
    - Act: call GET / with follow_redirects=True
    - Assert: response 200 from final destination (or appropriate error)
    """
    # Arrange
    # (client fixture handles setup)
    
    # Act
    response = client.get("/", follow_redirects=True)
    
    # Assert
    # Note: Static files are mounted, so redirect should succeed
    # Response code should be 200 for successful redirect
    assert response.status_code == 200
