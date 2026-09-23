import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone

from app.core.config import settings
from app.repositories.job_repository import JobRepository
from app.services.job_services import JobService
from app.workers import worker

import logging

logger = logging.getLogger(__name__)

class SchedulerService:
    def __init__(self, job_repository: JobRepository,job_service:JobService,dispatcher=None):
        self.job_repository = job_repository
        self.job_service = job_service
        self.dispatcher = dispatcher or ThreadPoolExecutor(max_workers=settings.MAX_WORKERS)
        self.shutdown_requested = False

    #run the jobs collectedfor scheduling on the database
    def run_pending_job(self) -> dict: 
        current_time =datetime.now(tz=timezone.utc)
        print("Checking for runnable jobs.")
        jobs = self.job_repository.get_job_runnable(current_time)
        print(f"found {len(jobs)} runnable jobs.")
        futures = []
        for job in jobs:
            print(
                f"Dispatching Job {job.id} | {job.title}"
                )
            futures.append(self.dispatcher.submit(worker.execute,job.id,"SCHEDULER"))
        message = {
                    "jobs_found": len(jobs),
                    "jobs_executed":len(futures)
                    }
        return message
    
    def start_scheduler(self):
        try:
            while not self.shutdown_requested:
                stats= self.run_pending_job()
                print(  f"[Scheduler] Cycle complete | "
                    f"Found: {stats['jobs_found']} | "
                    f"Submitted: {stats['jobs_executed']}"
                    )
                logger.info("Scheduler Started")
                time.sleep(settings.SCHEDULER_POLL_INTERVAL)
        except KeyboardInterrupt:
            self.shutdown()
        finally:
            self.dispatcher.shutdown(wait=True)
            print("Scheduler stopped")
            logger.info("Scheduler stopped")

    def shutdown(self):
        print("Shutdown Requested")
        logger.info("Scheduler Shutdown")
        self.shutdown_requested = True
 