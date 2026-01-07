import urllib.parse

from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Basketball Team" in data


def test_signup_and_unregister():
    activity = "Chess Club"
    email = "test_student@example.com"

    # Ensure test email is not present before starting
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # Signup (encode activity name for URL)
    path = f"/activities/{urllib.parse.quote(activity)}/signup?email={urllib.parse.quote(email)}"
    resp = client.post(path)
    assert resp.status_code == 200
    assert email in activities[activity]["participants"]

    # Duplicate signup should return 400
    resp_dup = client.post(path)
    assert resp_dup.status_code == 400

    # Unregister
    del_path = f"/activities/{urllib.parse.quote(activity)}/participants?email={urllib.parse.quote(email)}"
    resp_del = client.delete(del_path)
    assert resp_del.status_code == 200
    assert email not in activities[activity]["participants"]

    # Unregistering again should yield 404
    resp_del2 = client.delete(del_path)
    assert resp_del2.status_code == 404


def test_signup_nonexistent_activity():
    resp = client.post("/activities/NoSuchActivity/signup?email=a@b.com")
    assert resp.status_code == 404
