# Employee Management System

A beginner-friendly DevOps mini-project built with Flask, SQLite, Docker, and Jenkins.

## Features
- Add, view, edit, and delete employee records
- Search employees by name, email, or department
- SQLite database with persistent Docker volume
- Pytest tests
- Jenkins pipeline for checkout, test, Docker build, and deployment

## 1. Run locally (Windows PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Open http://localhost:5000

If PowerShell blocks virtual-environment activation, run:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## 2. Run tests locally

```powershell
pytest -q
```

## 3. Run with Docker

Make sure Docker Desktop is running, then:

```powershell
docker compose up --build -d
```

Open http://localhost:5000

Stop the application:
```powershell
docker compose down
```

The SQLite database is stored in a named Docker volume, so the records remain when the container is stopped or recreated. To remove the database too, run:
```powershell
docker compose down -v
```

## 4. Jenkins pipeline

The included `Jenkinsfile` performs:
1. Checkout source code
2. Install Python dependencies
3. Run Pytest
4. Build a Docker image
5. Deploy with Docker Compose

### Jenkins prerequisites
The Jenkins agent must have Python 3, Docker CLI, and the Docker Compose plugin installed. The agent must also be permitted to access the Docker daemon. A Jenkins container does not automatically have access to the host Docker daemon.

Create a Pipeline job in Jenkins, connect it to this GitHub repository, and select **Pipeline script from SCM** with script path `Jenkinsfile`.

For a first local learning setup, you can run the app with Docker Compose manually, then configure Jenkins after the application and tests work.

## Project structure

```text
app.py                 Flask routes
database.py            SQLite setup
templates/             HTML pages
static/                CSS
tests/                 Automated tests
Dockerfile             Application image
docker-compose.yml     Container configuration
Jenkinsfile            CI/CD pipeline
```

## Notes
- This is a learning/demo project, not a production HR system.
- Do not use real employee personal or salary data.
- Change `SECRET_KEY` before any public deployment.
- The CDN-hosted Bootstrap stylesheet requires an internet connection in the browser.
