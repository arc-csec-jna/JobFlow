from fastapi.testclient import TestClient
from app.main import app
from app.core.database import get_db
from app.services.job_services import JobService
from sqlalchemy.orm import Session
from app.models.job import Job
from app.models.execution import Execution  
#API > JobCreate > get Job service >  get_db() > JobService > Job Repo > PostgreSQL DB


client = TestClient(app)

def test_create_job(db_session):
    def override_get_db():
        yield db_session
    app.dependency_overrides[get_db] = override_get_db
    response = client.post("/jobs",
                           json={
                                "title": "Test API Job",
                                "job_type": "dummy",
                                "payload": {},
                                "max_retries": 3,
                                "priority": "MEDIUM",
                                "status": "PENDING", 
                              })
    job = db_session.query(Job).filter(Job.id == response.json()["id"]).first()
    assert response.status_code == 200
    assert job is not None
    #assert job.title == response["title"]

def test_find_job_by_id(db_session):
    def override_get_db():
           yield db_session
    app.dependency_overrides[get_db] = override_get_db
    response = client.post("/jobs",
                              json={
                                   "title": "Test API Job",
                                   "job_type": "dummy",
                                   "payload": {},
                                   "max_retries": 3,
                                   "priority": "MEDIUM",
                                   "status": "PENDING", 
                                 })

    job_id = response.json()["id"]
    id_get_response = client.get(f"/jobs/{job_id}")
    assert id_get_response.status_code == 200
    assert id_get_response.json()["id"] == job_id

def test_jobid_not_found(db_session):
    def override_get_db():
           yield db_session
    app.dependency_overrides[get_db] = override_get_db 
    response = client.get("/jobs/99999")
    assert response.status_code == 404

def test_jobs_not_found(db_session):
    def override_get_db():
           yield db_session
    app.dependency_overrides[get_db] = override_get_db
    response_getjobs = client.get("/jobs")
    assert response_getjobs.status_code == 200
    assert response_getjobs.json() == []

def test_jobs_found(db_session):
    def override_get_db():
           yield db_session
    app.dependency_overrides[get_db] = override_get_db
    response = client.post("/jobs",
                              json={
                                   "title": "Test API Job",
                                   "job_type": "dummy",
                                   "payload": {},
                                   "max_retries": 3,
                                   "priority": "MEDIUM",
                                   "status": "PENDING", 
                                 })
    response_getjobs = client.get("/jobs")
    jobs = response_getjobs.json()
    job_id = response.json()["id"]
    assert any(job["id"] == job_id for job in jobs)
    assert response_getjobs.status_code == 200

def test_update_job(db_session):
    def override_get_db():
        yield db_session
    app.dependency_overrides[get_db] = override_get_db
    response = client.post("/jobs",
                              json={
                                   "title": "Test API Job",
                                   "job_type": "dummy",
                                   "payload": {},
                                   "max_retries": 3,
                                   "priority": "MEDIUM",
                                   "status": "PENDING", 
                                 })
    job_id = response.json()["id"]
    update = client.put(f"/jobs/{job_id}",
                        json={
                             "title" : "Test Update API job"
                        }
                        )
    job = db_session.query(Job).filter(Job.id == job_id).first()
    update_job_id = job.id
    preset_id = response.json()["id"]
    assert update.status_code == 200
    assert  update_job_id == preset_id


def test_update_job_status(db_session):
    def override_get_db():
        yield db_session
    app.dependency_overrides[get_db] = override_get_db
    response = client.post("/jobs",
                            json={
                                "title": "Test API Job",
                                "job_type": "dummy",
                                "payload": {},
                                "max_retries": 3,
                                "priority": "MEDIUM",
                                "status": "PENDING", 
                            })
    #update the created job status
    job_id = response.json()["id"]
    update_status = client.patch(f"/jobs/{job_id}/status",params={"status": "SUCCESS"})
    
    job = db_session.query(Job).filter(Job.id == job_id).first()
    body = update_status.json()

    assert update_status.status_code == 200
    assert job_id == job.id
    assert job.status == "SUCCESS"


def test_delete_job(db_session):
    def override_get_db():
        yield db_session
    app.dependency_overrides[get_db] = override_get_db
    response = client.post("/jobs",
                                json={
                                    "title": "Test API Job",
                                    "job_type": "dummy",
                                    "payload": {},
                                    "max_retries": 3,
                                    "priority": "MEDIUM",
                                    "status": "PENDING", 
                                })
    #try and delete the job and see the returns
    job_id = response.json()["id"]
    delete = client.delete(f"/jobs/{job_id}")
    job = db_session.query(Job).filter(Job.id == job_id).first()

    assert delete.status_code == 200
    assert job is None
    assert delete.json()["message"] == "Job deleted successfully"

def test_delete_nonexistent_job(db_session):
    def override_get_db():
           yield db_session
    app.dependency_overrides[get_db] = override_get_db 
    response = client.delete("/jobs/99999")
    assert response.status_code == 404

def test_run_job_fail(db_session):
        def override_get_db():
            yield db_session
        app.dependency_overrides[get_db] = override_get_db
        response = client.post("/jobs",
                                json={
                                    "title": "Test API Job",
                                    "job_type": "fail",
                                    "payload": {},
                                    "max_retries": 3,
                                    "priority": "MEDIUM",
                                    "status": "PENDING", 
                                })
        job_id = response.json()["id"]
        run_response = client.post(f"/jobs/{job_id}/run")
        assert run_response.status_code == 200


def test_run_job_success(db_session):
        def override_get_db():
            yield db_session
        app.dependency_overrides[get_db] = override_get_db
        response = client.post("/jobs",
                                json={
                                    "title": "Test API Job",
                                    "job_type": "cleanup",
                                    "payload": {"directory": "/tmp/test", "days_old": 7},
                                    "max_retries": 3,
                                    "priority": "MEDIUM",
                                    "status": "PENDING", 
                                })
        job_id = response.json()["id"]
        run_response = client.post(f"/jobs/{job_id}/run")
        execution = (
             db_session.query(Execution).filter(Execution.job_id == job_id).first()
        )

        assert run_response.status_code == 200
        assert execution is not None

def test_get_job_executions_byjobid(db_session):
        def override_get_db():
            yield db_session
        app.dependency_overrides[get_db] = override_get_db
        response = client.post("/jobs",
                                json={
                                    "title": "Test API Job",
                                    "job_type": "cleanup",
                                    "payload": {"directory": "/tmp/test", "days_old": 7},
                                    "max_retries": 3,
                                    "priority": "MEDIUM",
                                    "status": "PENDING", 
                                })
        job_id = response.json()["id"]
        run_response = client.post(f"/jobs/{job_id}/run")
        executions_response = client.get(f"/jobs/{job_id}/executions")

        assert executions_response.status_code == 200
        assert len(executions_response.json()) > 0

def test_get_execution_logs_by_executionid(db_session):
        def override_get_db():
            yield db_session
        app.dependency_overrides[get_db] = override_get_db
        response = client.post("/jobs",
                                json={
                                    "title": "Test API Job",
                                    "job_type": "cleanup",
                                    "payload": {"directory": "/tmp/test", "days_old": 7},
                                    "max_retries": 3,
                                    "priority": "MEDIUM",
                                    "status": "PENDING", 
                                })
        job_id = response.json()["id"]
        run_response = client.post(f"/jobs/{job_id}/run")
        execution = (
             db_session.query(Execution).filter(Execution.job_id == job_id).first()
        )
        execution_id = execution.id
        logs_response = client.get(f"/executions/{execution_id}/logs")

        assert logs_response is not None
        assert logs_response.status_code == 200

def test_get_execution_Job_notexists(db_session):
        def override_get_db():
            yield db_session
        app.dependency_overrides[get_db] = override_get_db
        response = client.get("/jobs/99999/executions")
        assert response.status_code == 404

def test_get_execution_logs_notexists(db_session):
        def override_get_db():
            yield db_session
        app.dependency_overrides[get_db] = override_get_db
        response = client.get("/executions/99999/logs")
        assert response.status_code == 404
def test_get_execution_byid_notexists(db_session):
        def override_get_db():
            yield db_session
        app.dependency_overrides[get_db] = override_get_db
        response = client.get("/executions/99999")
        assert response.status_code == 404
