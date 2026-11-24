def test_health_check(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "devtrack-api"}


def test_project_and_task_flow(client):
    project_response = client.post(
        "/api/projects",
        json={"name": "Course planner", "description": "A test project"},
    )
    assert project_response.status_code == 201
    project = project_response.json()

    task_response = client.post(
        "/api/tasks",
        json={
            "title": "Add the first screen",
            "project_id": project["id"],
            "priority": "high",
        },
    )
    assert task_response.status_code == 201
    task = task_response.json()
    assert task["project_name"] == "Course planner"
    assert task["completed"] is False

    filtered = client.get("/api/tasks", params={"status": "todo"})
    assert filtered.status_code == 200
    assert [item["id"] for item in filtered.json()] == [task["id"]]

    update_response = client.patch(
        f"/api/tasks/{task['id']}",
        json={"status": "done", "priority": "low"},
    )
    assert update_response.status_code == 200
    assert update_response.json()["completed"] is True
    assert update_response.json()["status"] == "done"

    dashboard = client.get("/api/dashboard").json()
    assert dashboard == {
        "project_count": 1,
        "task_count": 1,
        "open_count": 0,
        "completed_count": 1,
        "completion_rate": 100.0,
    }


def test_deleting_project_keeps_tasks(client):
    project = client.post("/api/projects", json={"name": "Temporary project"}).json()
    task = client.post(
        "/api/tasks",
        json={"title": "Keep this task", "project_id": project["id"]},
    ).json()

    deleted = client.delete(f"/api/projects/{project['id']}")
    assert deleted.status_code == 204

    tasks = client.get("/api/tasks").json()
    remaining = next(item for item in tasks if item["id"] == task["id"])
    assert remaining["project_id"] is None
    assert remaining["project_name"] is None


def test_rejects_task_for_missing_project(client):
    response = client.post(
        "/api/tasks",
        json={"title": "Orphan at creation", "project_id": 9999},
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Project not found"


def test_rejects_assigning_task_to_missing_project(client):
    task = client.post("/api/tasks", json={"title": "Keep project-free"}).json()

    response = client.patch(
        f"/api/tasks/{task['id']}",
        json={"project_id": 9999},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Project not found"
    unchanged = client.get("/api/tasks").json()[0]
    assert unchanged["project_id"] is None


def test_rejects_null_for_required_task_update_fields(client):
    task = client.post("/api/tasks", json={"title": "A valid task"}).json()

    for field in ("title", "status", "priority"):
        response = client.patch(
            f"/api/tasks/{task['id']}",
            json={field: None},
        )
        assert response.status_code == 422


def test_validates_task_fields(client):
    response = client.post("/api/tasks", json={"title": "", "priority": "urgent"})
    assert response.status_code == 422


def test_missing_task_returns_404(client):
    response = client.patch("/api/tasks/9999", json={"status": "done"})
    assert response.status_code == 404
