from fastapi import FastAPI, HTTPException
from app.schemas.job import JobCreate ,JobUpdate
from app.models.job import Job
from app.models.execution import Execution
from app.models.logs import Log
from app.database import Base, engine
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