from datetime import datetime,timezone, timedelta

from fastapi import HTTPException

from app.core.config import settings
from app.enums import Priority
from app.enums.JobStatus import JobStatus
from app.executors.python_executor import PythonExecutor
from app.models.execution import Execution
from app.models.job import Job
from app.models.logs import Log
from app.repositories.ExecutionRepository import ExecutionRepository
from app.repositories.job_repository import JobRepository
from app.repositories.log_repository import LogRepository
from app.schemas.job import JobCreate


class ExecutionContext:
    def __init__(
            self,
            job,
            executor,
            execution_record,
            attempt = 1,
            max_attempts = 3,
            trigger = "MANUAL",
                 ):
        self.job = job
        self.executor = executor
        self.execution_record = execution_record
        self.attempt = attempt
        self.max_attempts = max_attempts
        self.trigger = trigger
        
        
class JobService:
    def __init__(
            self, job_repository: JobRepository,
            execution_repository: ExecutionRepository,
            log_repository: LogRepository,
            retry_policy,
            executor:PythonExecutor,
            ):
        self.job_repository = job_repository
        self.execution_repository = execution_repository
        self.log_repository = log_repository
        self.retry_policy = retry_policy
        self.executor = executor

    def get_executions_by_id(self, execution_id):
        execution = self.execution_repository.get_execution_by_id(execution_id)
        if not execution:
            raise HTTPException(status_code=404, detail="Execution not found")
        return execution
    
    def get_executions_by_job_id(self, job_id,user_id):
        job = self.job_repository.get_job_by_id(job_id)

        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        if job.user_id != user_id:
            raise HTTPException(status_code=403, detail="Not authorized")
        
        return self.execution_repository.get_executions_by_job_id(job_id)
    
    def get_logs_by_execution_id(self, execution_id):
        execution = self.execution_repository.get_execution_by_id(execution_id)
        if not execution:
            raise HTTPException(status_code=404, detail="Execution not found")
        return self.log_repository.get_logs_by_execution_id(execution_id)
    
    def get_job_by_id(self, job_id,user_id):
        job = self.job_repository.get_job_by_id(job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        if job.user_id != user_id:
            raise HTTPException(status_code=403, detail="Job not found")
        return job

    def create_job(self, job_data:JobCreate,user_id):
        job  = Job(
            title=job_data.title,
            job_type = job_data.job_type,
            payload = job_data.payload,
            schedule_interval_seconds=job_data.schedule_interval_seconds,
            next_run_at=job_data.next_run_at,
            enabled=job_data.enabled,
            priority=Priority[job_data.priority.upper()].value,
            status=getattr(JobStatus,job_data.status.upper()),
            user_id=user_id
        )
        return self.job_repository.create_job(job)

    def update_job(self, job_id, user_id, job_data):
        verify= self.job_repository.get_job_by_id(job_id)
        if not verify:
            raise HTTPException(status_code=404, detail="Job not found")
        if verify.user_id != user_id:
            raise HTTPException(status_code=403, detail="not authorized")
        job_data_dict = job_data.model_dump(exclude_unset=True)
        job = self.job_repository.update_job(job_id, job_data_dict)

        if not job:
            raise HTTPException(
                status_code=404,
                detail="Job update failed"
            )
        return job

    def delete_job(self, job_id,user_id):

        verify= self.job_repository.get_job_by_id(job_id)

        if not verify:
            raise HTTPException(status_code=404, detail="Job not found")
        if verify.user_id != user_id:
            raise HTTPException(status_code=403, detail="not authorized")
        
        success = self.job_repository.delete_job(job_id)

        if not success:
            raise HTTPException(status_code=404, detail="Job not found")
        return {"message": "Job deleted successfully"}
    
    def get_jobs(self,user_id):
        return self.job_repository.get_jobs(user_id)
    
    def update_job_status(self, job_id,user_id, status):
        verify= self.job_repository.get_job_by_id(job_id)
        if not verify:
            raise HTTPException(status_code=404, detail="Job not found")
        if verify.user_id != user_id:
            raise HTTPException(status_code=403, detail="not authorized")
        update = self.job_repository.update_job_status(job_id, status)
        return update
          
        
    def update_next_run(self,job,next_run):
        return self.job_repository.update_next_run_at(job.id,next_run)

    def update_enabled(self,job):
        return self.job_repository.enable_disable_job(job.id)
    

# ===================================================================================================================
#ORCHESTRATION SERVICE
    def run_job(self, job_id, user_id, trigger = "MANUAL"):

        exec_ctx = self._prepare_execution(job_id, user_id,trigger)
        exec_ctx.execution_result = self._execute_task(exec_ctx)
        if exec_ctx.execution_result.status == "SUCCESS":
            self._handle_success(exec_ctx)
        else:
            self._handle_failure(exec_ctx, exec_ctx.execution_result.message)
  
    def _complete_execution(
        self,
        execution_record,
        status,
        error_message,
        log_message,
        ):
        # Update execution to success or failure based on the result of the job execution
        execution_data_dict = {"status": status, "error_message": error_message, "finished_at": datetime.now(tz=timezone.utc)}
        # Update the job status to "completed" or "failed" based on the execution result
        self.execution_repository.update_execution(execution_record.id,execution_data_dict)
        # Write completion status on logs
        self.log_repository.create_log(Log(execution_id=execution_record.id, level = "INFO" if status == "SUCCESS" else "WARNING", message=log_message,timestamp = datetime.now(tz=timezone.utc)))

    def _prepare_execution(self, job_id, user_id, trigger): #<< this is where I create the execution context and check if the job is already running
            job = self.get_job_by_id(job_id,user_id)
            if not job:
                raise HTTPException(status_code=404, detail="Job not found")
            if job.user_id != user_id:
                raise HTTPException(status_code=403, detail="Not authorized")
            if job.status == "RUNNING":
                        raise HTTPException(status_code=400, detail="Job is already running")
            self.job_repository.update_job_status(job_id, "RUNNING")
        #create another execution instance indicating how many times the job has been retried and the attempt number
            execution = Execution(job_id = job.id, status = "RUNNING", started_at = datetime.now(tz=timezone.utc), attempt_number = job.retry_count + 1)
            execution_record = self.execution_repository.create_execution(execution)
            self.log_repository.create_log(Log(execution_id=execution_record.id,level = "INFO", message=f"Job {job.id} started. {trigger}"))
            
            return ExecutionContext(
                job = job,
                executor=self.executor,
                execution_record=execution_record
            )
    
    def _execute_task(self,ctx):
        ctx.execution_result = ctx.executor.execute(ctx.job)
        
        return ctx.execution_result
        
    def _handle_success(self,ctx):
        self._complete_execution(ctx.execution_record,"SUCCESS",None,f"Job {ctx.job.id} SUCCESS",)
        self.job_repository.update_job_status(ctx.job.id,"SUCCESS")
                
        if (ctx.job.enabled and ctx.job.schedule_interval_seconds): #checking interval and scheduled runs
            next_run = datetime.now(tz=timezone.utc) + timedelta(seconds=ctx.job.schedule_interval_seconds)
                                    
            self.job_repository.update_next_run_at(ctx.job.id,next_run)
            if ctx.job.retry_count > 0:
                ctx.job.retry_count = 0
                self.job_repository.update_retry_count(ctx.job.id,ctx.job.retry_count)
        return {
                "message": f"Job {ctx.job.id} execution SUCCESS.",
                "execution_id": ctx.execution_record.id,
                }
    
    def _handle_failure(self,ctx,error_message):
        self._complete_execution(
         ctx.execution_record,
        "FAILED",
        error_message,
        f"Job {ctx.job.id} attempt FAILED",
        )

        if (self.retry_policy.should_retry(ctx.job)):
            self.update_job_status(ctx.job.id,ctx.job.user_id,"PENDING")
            ctx.job.status = "PENDING"
            if (ctx.job.enabled and ctx.job.schedule_interval_seconds): #checking interval and scheduled runs
                old_next_run = ctx.job.next_run_at
                next_run = datetime.now(tz=timezone.utc) + timedelta(seconds=settings.RETRY_DELAY_SECONDS)
                ctx.job.retry_count +=1
                self.job_repository.update_retry_count(ctx.job.id,ctx.job.retry_count)
                self.job_repository.update_next_run_at(ctx.job.id,next_run)
                ctx.job.next_run_at = next_run  
            return {
                        "message": f"Job {ctx.job.id} execution FAILED retry active.",
                        "execution_id": ctx.execution_record.id,
                    }
        else:
            ctx.job.status = "FAILED"
            ctx.job.enabled = False
            jobdata = {"status":  ctx.job.status,"enabled":ctx.job.enabled,}
            self.job_repository.update_job(ctx.job.id,jobdata)
            return {
                    "message": f"Job {ctx.job.id} execution permanent Failure.",
                    "execution_id": ctx.execution_record.id,
                    }