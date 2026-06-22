def test_get_activities_returns_required_fields(client):
    response = client.get("/activities")

    assert response.status_code == 200
    activities = response.json()

    assert isinstance(activities, dict)
    assert len(activities) >= 1

    required_fields = {"description", "schedule", "max_participants", "participants"}
    for details in activities.values():
        assert required_fields.issubset(details.keys())
        assert isinstance(details["participants"], list)


def test_get_activities_contains_seed_data(client):
    activities = client.get("/activities").json()

    assert "Chess Club" in activities
    assert "michael@mergington.edu" in activities["Chess Club"]["participants"]
