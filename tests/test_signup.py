from urllib.parse import quote

import src.app as app_module


def signup_path(activity_name: str) -> str:
    return f"/activities/{quote(activity_name, safe='')}/signup"


def test_signup_success_adds_participant(client):
    response = client.post(signup_path("Chess Club"), params={"email": "new.student@mergington.edu"})

    assert response.status_code == 200
    assert response.json()["message"] == "Signed up new.student@mergington.edu for Chess Club"
    assert "new.student@mergington.edu" in app_module.activities["Chess Club"]["participants"]


def test_signup_fails_when_already_registered(client):
    response = client.post(signup_path("Chess Club"), params={"email": "michael@mergington.edu"})

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"


def test_signup_fails_when_activity_is_full(client):
    activity = app_module.activities["Chess Club"]
    activity["max_participants"] = len(activity["participants"])

    response = client.post(signup_path("Chess Club"), params={"email": "capacity.test@mergington.edu"})

    assert response.status_code == 400
    assert response.json()["detail"] == "Activity is full"


def test_signup_fails_when_activity_does_not_exist(client):
    response = client.post(signup_path("Nonexistent Activity"), params={"email": "ghost@mergington.edu"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
