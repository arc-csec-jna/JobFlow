from app.models.execution import Execution
from app.models.job import Job
from app.models.logs import Log
from app.repositories.job_repository import JobRepository
from app.services.job_services import JobService
from datetime import datetime,timedelta
import time
from concurrent.futures import ThreadPoolExecutor
from app.workers import worker

class SchedulerService:
    def __init__(self, job_repository: JobRepository,job_service:JobService):
        self.job_repository = job_repository
        self.job_service = job_service

    #run the jobs collectedfor scheduling on the database
    def run_pending_job(self):
        current_time =datetime.now()
        print("Checking for runnable jobs.")
        jobs = self.job_repository.get_job_runnable(current_time)

        print(f"found {len(jobs)} runnable jobs.")#<<<<<<<<<<<
        with ThreadPoolExecutor(max_workers=4) as dispatcher:
            futures = []
            for job in jobs:
                print(
                        f"Dispatching Job {job.id} | {job.title}"
                    )
                futures.append(dispatcher.submit(worker.execute,job.id,"SCHEDULER"))
            message = {
                "jobs_found": len(jobs),
                "jobs_executed":len(futures)
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

 