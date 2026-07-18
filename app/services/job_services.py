import datetime

from fastapi import HTTPException
from app.models.execution import Execution
from app.models.job import Job
from app.models.logs import Log
from app.repositories.job_repository import JobRepository
from app.repositories.ExecutionRepository import ExecutionRepository
from app.repositories.log_repository import LogRepository
from app.schemas import job
from app.schemas.job import JobCreate
from datetime import datetime
from app.executors.python_executor import PythonExecutor
import time

class JobService:
    def __init__(self, job_repository: JobRepository, execution_repository: ExecutionRepository, log_repository: LogRepository):
        self.job_repository = job_repository
        self.execution_repository = execution_repository
        self.log_repository = log_repository

    def get_executions_by_execution_id(self, execution_id):
        execution = self.execution_repository.get_execution_by_id(execution_id)
        if not execution:
            raise HTTPException(status_code=404, detail="Execution not found")
        return execution
    
    def get_executions_by_job_id(self, job_id):
        job = self.job_repository.get_job_by_id(job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        return self.execution_repository.get_executions_by_job_id(job_id)
    
    def get_logs_by_execution_id(self, execution_id):
        execution = self.execution_repository.get_execution_by_id(execution_id)
        if not execution:
            raise HTTPException(status_code=404, detail="Execution not found")
        return self.log_repository.get_logs_by_execution_id(execution_id)
    
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
        max_attempts = 1 + job.max_retries
        # Update the job status to "running"
        self.job_repository.update_job_status(job_id, "RUNNING")
        python_executor = PythonExecutor()

        #---------------------------------------------------------------------------------------- Attempt loop ------------------------------------------------------------------------------------
        for attempt in range(1,max_attempts + 1):
            # create an execution record object
            execution = Execution(job_id = job.id, status = "RUNNING", started_at = datetime.now(), attempt_number = attempt)
            execution_record = self.execution_repository.create_execution(execution)
            # Write execution started on logs
            self.log_repository.create_log(Log(execution_id=execution_record.id,level = "INFO", message=f"Job {job.id} attempt {attempt} started."))
        #===================================================================================== EXECUTION LOGIC ==========================================================================================
            execution_result = python_executor.execute(job)
        #================================================================================================================================================================================================
            if execution_result.status == "SUCCESS":
                self._complete_execution(execution_record,"SUCCESS",None,f"Job {job.id} attempt {attempt} SUCCESS",)
                self.job_repository.update_job_status(job_id,"SUCCESS")
                message = (f"Job {job.id} execution SUCCESS.")                
                return {"message": message,"execution_id": execution_record.id}
            else:
                self._complete_execution(
                execution_record,
                "FAILED",
                execution_result.message,
                f"Job {job.id} attempt {attempt} FAILED",
                )
                if attempt < max_attempts:
                    self.log_repository.create_log(
                        Log(
                            execution_id=execution_record.id,
                            level="INFO",
                            message=f"Retrying... ({attempt + 1}/{max_attempts})"
                        )
                    )
                continue
        #Max attempts reached
        self.log_repository.create_log(
            Log(
                execution_id=execution_record.id,
                level="ERROR",
                message="Maximum retry attempts reached."
            )
        )
        self.job_repository.update_job_status(job_id, "FAILED")
        message = (f"Job {job.id} failed after {max_attempts} attempts.")

        return {"message": message,"execution_id": execution_record.id}
    
    def _complete_execution(
        self,
        execution_record,
        status,
        error_message,
        log_message,
        ):
        # Update execution to success or failure based on the result of the job execution
        execution_data_dict = {"status": status, "error_message": error_message, "finished_at": datetime.now()}
        # Update the job status to "completed" or "failed" based on the execution result
        self.execution_repository.update_execution(execution_record.id,execution_data_dict)
        # Write completion status on logs
        self.log_repository.create_log(Log(execution_id=execution_record.id, level = "INFO" if status == "SUCCESS" else "WARNING", message=log_message,timestamp = datetime.now()))
                   