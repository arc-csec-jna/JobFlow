from app.database import SessionLocal
from app.repositories.job_repository import JobRepository
from app.repositories.ExecutionRepository import ExecutionRepository
from app.repositories.log_repository import LogRepository
from app.services.job_services import JobService
from app.services.scheduler_service import SchedulerService

db= SessionLocal()

job_repository = JobRepository(db)
execution_repository = ExecutionRepository(db)
log_repository = LogRepository(db)
job_service = JobService(job_repository=job_repository, execution_repository=execution_repository, log_repository=log_repository)
sch_service = SchedulerService(job_repository,job_service)
sch_service.start_scheduler()

#poll available jobs
#send data to dispatcher