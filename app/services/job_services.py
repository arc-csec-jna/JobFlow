from fastapi import HTTPException
from app.models.execution import Execution
from app.models.job import Job
from app.models.logs import Log
from app.repositories.job_repository import JobRepository
from app.repositories.ExecutionRepository import ExecutionRepository
from app.repositories.log_repository import LogRepository
from app.schemas import job
from app.schemas.job import JobCreate
import time

class JobService:
    def __init__(self, job_repository: JobRepository, execution_repository: ExecutionRepository, log_repository: LogRepository):
        self.job_repository = job_repository
        self.execution_repository = execution_repository
        self.log_repository = log_repository

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
        job_data_dict = job_data.model_dump(exclude_unset=True)
        job = self.job_repository.update_job(job_id, job_data_dict)

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
    
    def get_jobs(self):
        return self.job_repository.get_jobs()
    
    def update_job_status(self, job_id, status):
        return self.job_repository.update_job_status(job_id, status)

# ===================================================================================================================
#ORCHESTRATION SERVICE
    def run_job(self, job_id):
        # Find the Job
        job = self.get_job_by_id(job_id)
        
        # Check business logic
        if job.status == "RUNNING":
            raise HTTPException(status_code=400, detail="Job is already running")
         
        # create an execution record
        execution = Execution(job_id = job.id, status = "RUNNING")
        execution_record = self.execution_repository.create_execution(execution)

        # Update the job status to "running"
        self.job_repository.update_job_status(job_id, "RUNNING")

        # Write execution started on logs
        self.log_repository.create_log(Log(execution_id=execution_record.id,level = "INFO", message=f"Job {job.id} started execution."))
        # Simulate job execution (this could be a call to an external service, a subprocess, etc.)
        time.sleep(2)
        self.log_repository.create_log(Log(execution_id=execution_record.id, level = "INFO", message=f"Job {job.id} completed execution."))

        # Update execution to success or failure based on the result of the job execution
        if job.status == "RUNNING":
            execution_data_dict = {"status": "SUCCESS", "result": "Job executed successfully"}
        else:
            execution_data_dict = {"status": "FAILED", "result": "Job execution failed"}
        self.execution_repository.update_execution(execution_record.id,execution_data_dict)

        # Update the job status to "completed" or "failed" based on the execution result
        self.job_repository.update_job_status(job_id, execution_data_dict["status"])
        # Write completion status on logs
        self.log_repository.create_log(Log(execution_id=execution_record.id, level = "INFO", message=f"Job {job.id} execution {execution_data_dict['status']}."))
        # return execution
        return {"message": f"Job {job.id} execution {execution_data_dict['status']}.", "execution_id": execution_record.id}
    