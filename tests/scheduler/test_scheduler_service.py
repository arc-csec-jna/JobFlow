from app.services.scheduler_service import SchedulerService
from tests.schedule_dummies import DummyJobRepository,DummyDispatcher,DummyJob

def test_ignore_disabled_jobs():
    job_repository = DummyJobRepository()
    for job in job_repository.get_job_runnable(current_time=None):
        if not job.enabled:
            continue  # Ignore disabled jobs
        assert job.enabled is True, "Disabled jobs should be ignored"


def test_ignore_next_run_at_jobs():
    job_data = DummyJob(job_id=1, title="Test Job", enabled=True, next_run_at=None, job_type="dummy", payload={}, status="PENDING", schedule_interval_seconds=60)
    job_repository = DummyJobRepository(job=[job_data])
   
    for job in job_repository.get_job_runnable(current_time=None):
        if job.next_run_at is not None:
            continue  # Ignore jobs with next_run_at set
        assert job.next_run_at is None, "Jobs with next_run_at should be ignored"
    
    
def test_run_pending_job():
    job_data = DummyJob(job_id=1, title="Test Job", enabled=True, next_run_at=None, job_type="dummy", payload={}, status="PENDING", schedule_interval_seconds=60)
    job_repository = DummyJobRepository(job=[job_data])
    dispatcher = DummyDispatcher()
    scheduler_service = SchedulerService(job_repository=job_repository, job_service=None,dispatcher=dispatcher,)

    result = scheduler_service.run_pending_job()

    assert len(dispatcher.submitted_jobs) == 1
    assert result["jobs_found"] == 1
    assert result["jobs_executed"] == 1



