from fastapi import FastAPI, HTTPException
from app.schemas.job import JobCreate ,JobUpdate
from app.core.database import Base, engine
from fastapi import Depends
from app.services.job_services import JobService
from app.dependencies import get_job_service

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return {"message":"Job runner API"}

@app.post("/jobs")
def create_job(job: JobCreate,service: JobService = Depends(get_job_service)):
    return service.create_job(job)

@app.put("/jobs/{job_id}")
def update_job(
    job_id: int,
    job_data: JobUpdate,
    service: JobService = Depends(get_job_service)
):
    return service.update_job(job_id, job_data)

@app.get("/jobs")
def get_jobs(service: JobService = Depends(get_job_service)):
    return service.get_jobs()

@app.get("/jobs/{job_id}")
def get_job(job_id: int, service: JobService = Depends(get_job_service)):
    return service.get_job_by_id(job_id)

@app.delete("/jobs/{job_id}")
def delete_job(job_id: int, service: JobService = Depends(get_job_service)):
    return service.delete_job(job_id)

@app.patch("/jobs/{job_id}/status")
def update_job_status(
    job_id: int,
    status: str,
    service: JobService = Depends(get_job_service)
):
    return service.update_job_status(job_id, status)

# ===================================================================================================================
@app.post("/jobs/{job_id}/run")
def run_job(job_id: int, service: JobService = Depends(get_job_service)):
    return service.run_job(job_id)


@app.get("/jobs/{job_id}/executions")
def get_executions_by_job_id(job_id: int, service: JobService = Depends(get_job_service)):
    job = service.get_job_by_id(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return service.get_executions_by_job_id(job_id)

@app.get("/executions/{execution_id}/logs")
def get_logs_by_execution_id(execution_id: int, service: JobService = Depends(get_job_service)):
    execution = service.get_executions_by_execution_id(execution_id)
    if not execution:
        raise HTTPException(status_code=404, detail="Execution not found")
    return service.get_logs_by_execution_id(execution_id)

@app.get("/executions/{execution_id}")
def get_execution_by_id(execution_id: int, service: JobService = Depends(get_job_service)):
    execution = service.get_executions_by_execution_id(execution_id)
    if not execution:
        raise HTTPException(status_code=404, detail="Execution not found")
    return execution