from app.core.database import SessionLocal
from app.repositories.job_repository import JobRepository
from app.repositories.ExecutionRepository import ExecutionRepository
from app.repositories.log_repository import LogRepository
from app.services.job_services import JobService
import threading


def execute(job_id:int,trigger:str):
    
    thread_name = threading.current_thread().name
    db= SessionLocal()

    try:
        job_repository = JobRepository(db)
        execution_repository = ExecutionRepository(db)
        log_repository = LogRepository(db)
        job_service = JobService(job_repository=job_repository, execution_repository=execution_repository, log_repository=log_repository)

    
        print(f"Worker-{thread_name} executing Job number:{job_id}")
        job_service.run_job(job_id,trigger)
        print(f"Worker-{thread_name} finished Job number:{job_id}")
    except Exception as e:
        print(f"Worker-{thread_name} encountered error on Job number:{job_id}: {e}")
    finally:
        db.close()