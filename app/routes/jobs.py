from fastapi import Depends,APIRouter, HTTPException
from app.schemas.job import JobCreate, JobResponse, JobUpdate

from app.dependencies import get_job_service
from app.services.job_services import JobService
from app.enums.JobStatus import JobStatus
router = APIRouter()

@router.get("/")
def root():
    return {"message":"Job runner API"}

@router.post("/jobs",response_model=JobResponse)
def create_job(job: JobCreate,service: JobService = Depends(get_job_service)):
    return service.create_job(job)

@router.put("/jobs/{job_id}",response_model=JobResponse)
def update_job(
    job_id: int,
    job_data: JobUpdate,
    service: JobService = Depends(get_job_service)
):
    return service.update_job(job_id, job_data)

@router.get("/jobs",response_model=list[JobResponse])
def get_jobs(service: JobService = Depends(get_job_service)):
    return service.get_jobs()

@router.get("/jobs/{job_id}",response_model=JobResponse)
def get_job(job_id: int, service: JobService = Depends(get_job_service)):
    return service.get_job_by_id(job_id)

@router.delete("/jobs/{job_id}")
def delete_job(job_id: int, service: JobService = Depends(get_job_service)):
    return service.delete_job(job_id)

@router.patch("/jobs/{job_id}/status",response_model=JobResponse)
def update_job_status(
    job_id: int,
    status: JobStatus,
    service: JobService = Depends(get_job_service)
):
    return service.update_job_status(job_id, status)

# ===================================================================================================================
@router.post("/jobs/{job_id}/run")
def run_job(job_id: int, service: JobService = Depends(get_job_service)):
    return service.run_job(job_id)


@router.get("/jobs/{job_id}/executions")
def get_executions_by_job_id(job_id: int, service: JobService = Depends(get_job_service)):
    job = service.get_job_by_id(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return service.get_executions_by_job_id(job_id)

