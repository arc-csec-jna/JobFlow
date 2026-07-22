from app.models.execution import Execution
from app.models.job import Job
from app.models.logs import Log
from app.repositories.job_repository import JobRepository
from app.services.job_services import JobService
from datetime import datetime,timedelta
import time

class SchedulerService:
    def __init__(self, job_repository: JobRepository,job_service:JobService):
        self.job_repository = job_repository
        self.job_service = job_service

    #run the jobs collectedfor scheduling on the database
    def run_pending_job(self):
        current_time =datetime.now()
        print("Checking for runnable jobs.")
        jobs = self.job_repository.get_job_runnable(current_time)
        print(f"found {len(jobs)} runnable jobs.")
        jobcnt = 0
        for job in jobs:
            print(
                    f"Running Job {job.id} | "
                    f"{job.title} | "
                    f"next_run_at={job.next_run_at}"
                )
            jobcnt += 1
            self.job_service.run_job(job.id,trigger = "SCHEDULER")
        message = {
            "jobs_found": len(jobs),
            "jobs_executed":jobcnt
            }
        return message
    
    def start_scheduler(self,enabled=True):
        while enabled:
            stats= self.run_pending_job()
            print(  f"[Scheduler] Cycle complete | "
                f"Found: {stats['jobs_found']} | "
                f"Executed: {stats['jobs_executed']}"
                )
            time.sleep(5)

