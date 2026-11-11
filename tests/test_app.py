import os
import tempfile
import pytest
from app import app as flask_app
from database import init_db

@pytest.fixture
def client():
    handle, path = tempfile.mkstemp(suffix=".db")
    os.close(handle)
    init_db(path)
    flask_app.config["TESTING"] = True
    flask_app.config["DATABASE_PATH"] = path
    # Routes use the module-level DATABASE value, so point it at this test database.
    import app as app_module
    old_path = app_module.DATABASE
    app_module.DATABASE = path
    with flask_app.test_client() as test_client:
        yield test_client
    app_module.DATABASE = old_path
    os.unlink(path)

def test_home_page_loads(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Employees" in response.data

def test_add_employee(client):
    response = client.post("/add", data={
        "name": "Asha Rao", "email": "asha@example.com",
        "department": "IT", "designation": "Trainee", "salary": "25000"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Asha Rao" in response.data

def test_delete_employee(client):
    client.post("/add", data={"name": "Ravi", "email": "ravi@example.com"})
    import app as app_module
    from database import get_db
    db = get_db(app_module.DATABASE)
    employee_id = db.execute("SELECT id FROM employees WHERE name='Ravi'").fetchone()["id"]
    db.close()
    response = client.post(f"/delete/{employee_id}", follow_redirects=True)
    assert response.status_code == 200
    assert b"Ravi" not in response.data
