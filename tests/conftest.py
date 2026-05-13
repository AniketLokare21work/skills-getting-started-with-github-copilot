import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def reset_activities():
    """
    Reset activities to initial state before each test.
    This fixture captures the initial state and restores it after each test.
    """
    # Store initial activities state
    initial_state = {
        activity_name: {
            "description": activity["description"],
            "schedule": activity["schedule"],
            "max_participants": activity["max_participants"],
            "participants": activity["participants"].copy()
        }
        for activity_name, activity in activities.items()
    }
    
    yield
    
    # Restore initial state after test
    activities.clear()
    activities.update(initial_state)


@pytest.fixture
def client(reset_activities):
    """
    Provide a TestClient instance with reset activities for each test.
    """
    return TestClient(app)
