from fastapi import HTTPException
from app.models import job
from app.models.job import Job
from app.repositories.job_repository import JobRepository
from app.schemas.job import JobCreate

class JobService:
    def __init__(self, job_repository: JobRepository):
        self.job_repository = job_repository

    def get_job_by_id(self, job_id):
        job = self.job_repository.get_job_by_id(job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        return job

    def create_job(self, job_data:JobCreate):
        job  = Job(
            title=job_data.title,
            job_type = job_data.job_type,
            payload = job_data.payload,
        )
        return self.job_repository.create_job(job)

    def update_job(self, job_id, job_data):
        job = self.job_repository.update_job(job_id, job_data)

        if not job:
            raise HTTPException(
                status_code=404,
                detail="Job not found"
            )
        return job

    def delete_job(self, job_id):
        success = self.job_repository.delete_job(job_id)
        if not success:
            raise HTTPException(status_code=404, detail="Job not found")
        return {"message": "Job deleted successfully"}