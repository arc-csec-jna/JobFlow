from app.core.database import get_db
from app.repositories.ExecutionRepository import ExecutionRepository
from app.repositories.job_repository import JobRepository
from app.repositories.log_repository import LogRepository
from app.services.job_services import JobService
from sqlalchemy.orm import Session
from fastapi import Depends
from app.services.retry_policy import RetryPolicy


def get_job_service(db: Session = Depends(get_db)):
    job_repository = JobRepository(db)
    execution_repository = ExecutionRepository(db)
    log_repository = LogRepository(db)
    retry_policy= RetryPolicy()
    return JobService(job_repository=job_repository, execution_repository=execution_repository, log_repository=log_repository,retry_policy=retry_policy)