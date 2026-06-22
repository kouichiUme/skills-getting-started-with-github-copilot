from urllib.parse import quote

import src.app as app_module


def unregister_path(activity_name: str) -> str:
    return f"/activities/{quote(activity_name, safe='')}/participants"


def signup_path(activity_name: str) -> str:
    return f"/activities/{quote(activity_name, safe='')}/signup"


def test_unregister_success_removes_participant(client):
    response = client.delete(
        unregister_path("Chess Club"), params={"email": "michael@mergington.edu"}
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Unregistered michael@mergington.edu from Chess Club"
    assert "michael@mergington.edu" not in app_module.activities["Chess Club"]["participants"]


def test_unregister_fails_for_non_member(client):
    response = client.delete(
        unregister_path("Chess Club"), params={"email": "not.registered@mergington.edu"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"


def test_unregister_fails_for_missing_activity(client):
    response = client.delete(
        unregister_path("Nonexistent Activity"), params={"email": "anyone@mergington.edu"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_then_signup_again_succeeds(client):
    remove_response = client.delete(
        unregister_path("Chess Club"), params={"email": "michael@mergington.edu"}
    )
    add_response = client.post(signup_path("Chess Club"), params={"email": "michael@mergington.edu"})

    assert remove_response.status_code == 200
    assert add_response.status_code == 200
    assert "michael@mergington.edu" in app_module.activities["Chess Club"]["participants"]
