from app.core.database import SessionLocal
from app.repositories.ExecutionRepository import ExecutionRepository
from app.repositories.job_repository import JobRepository
from app.repositories.log_repository import LogRepository
from app.services.job_services import JobService
from app.services.retry_policy import RetryPolicy
from app.services.scheduler_service import SchedulerService

db= SessionLocal()

job_repository = JobRepository(db)
execution_repository = ExecutionRepository(db)
log_repository = LogRepository(db)
retry_policy = RetryPolicy()
job_service = JobService(job_repository=job_repository, execution_repository=execution_repository, log_repository=log_repository,retry_policy=retry_policy)
sch_service = SchedulerService(job_repository,job_service)
sch_service.start_scheduler()

