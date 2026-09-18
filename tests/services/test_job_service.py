from app.contracts.execution_result import ExecutionResult
from app.services.job_services import JobService
from tests.schedule_dummies import (
    DummyExecutionRepository,
    DummyExecutor,
    DummyJob,
    DummyJobRepository,
    DummyLogRepository,
    Dummyretry_policy,
)
from tests.security.DummySecurity import DummyUser
from datetime import datetime,timezone
import pytest
from fastapi import HTTPException


def test_create_job(db_session):
    job_data = DummyJob(job_id=1,title="Test Job", enabled=True, next_run_at=None, job_type="dummy", payload={}, status="PENDING",schedule_interval_seconds=60)
    job_repo = DummyJobRepository(job=[job_data])
    exec_repo = DummyExecutionRepository()
    ret_policy = Dummyretry_policy()
    exec_utor = DummyExecutor(ExecutionResult(status="SUCCESS",message="Job Executed Successfully"))
    job_service = JobService(job_repo, exec_repo, None, ret_policy,exec_utor)
    dummy_user = DummyUser(
                id=1,
                username="testuser",
                email="test@example.com",
                password_hash="dummy_hash",
                created_at=datetime.now(timezone.utc)
            )
    created_job = job_service.create_job(job_data,dummy_user.id)

    assert created_job.title == "Test Job"
    assert created_job.enabled == True
    assert created_job.payload == {}
    assert created_job.status == "PENDING"

def test_run_job_success(db_session):
    job_data = DummyJob(job_id=1,title="Test Job", enabled=True, next_run_at=None, job_type="dummy", payload={}, status="PENDING",schedule_interval_seconds=60,user_id=1)
    job_repo = DummyJobRepository(job=[job_data])
    exec_repo = DummyExecutionRepository()
    ret_policy = Dummyretry_policy()
    log_repo = DummyLogRepository()
    exec_utor = DummyExecutor(ExecutionResult(status="SUCCESS",message="Job Executed Successfully"))
    job_service = JobService(job_repo, exec_repo, log_repo, ret_policy,exec_utor)

    # Simulate a successful execution
    job_service.run_job(job_data.id,1)
    executions = exec_repo.get_execution_by_job_id(job_data.id)
    assert executions.status == "SUCCESS"

def test_run_job_failed_and_schedules_retry(db_session):
  #job created _> execution failed -> retry -> success
    created_job = DummyJob(job_id=1,title="Test Job", enabled=True, next_run_at=None, job_type="dummy", payload={}, status="PENDING",schedule_interval_seconds=60, user_id=1)
    job_repo = DummyJobRepository(job=[created_job])
    execution_repo = DummyExecutionRepository()
    retry_policy = Dummyretry_policy()
    log_repo = DummyLogRepository()
    exec_utor = DummyExecutor(ExecutionResult(status="FAILED",message="Job Failed Successfully"))
    job_service = JobService(job_repo, execution_repo, log_repo, retry_policy,exec_utor) # Simulate a failed execution

    job_service.run_job(created_job.id,1)
    executions = execution_repo.get_execution_by_job_id(created_job.id)

    assert executions.status == "FAILED"
    assert created_job.status == "PENDING"
    assert created_job.next_run_at is not None  # Job should still be enabled for retry

def test_run_job_max_retries_reached():
    #job created _> execution failed -> retry -> success
        created_job = DummyJob(job_id=1,title="Test Job", enabled=True, next_run_at=None, job_type="dummy", payload={}, status="PENDING",schedule_interval_seconds=60,max_retries=3,retry_count=3,user_id=1)
        job_repo = DummyJobRepository(job=[created_job])
        execution_repo = DummyExecutionRepository()
        retry_policy = Dummyretry_policy()
        log_repo = DummyLogRepository()
        exec_utor = DummyExecutor(ExecutionResult(status="FAILED",message="Job Failed Successfully"))
        job_service = JobService(job_repo, execution_repo, log_repo, retry_policy,exec_utor) # Simulate a failed execution
    
        job_service.run_job(created_job.id,1)
        executions = execution_repo.get_execution_by_job_id(created_job.id)
    
        assert executions.status == "FAILED"
        assert created_job.status == "FAILED"
        assert created_job.enabled is False


def test_access_Job_diff_user():

    created_job = DummyJob(job_id=1,title="Test Job", enabled=True, next_run_at=None, job_type="dummy", payload={}, status="PENDING",schedule_interval_seconds=60,max_retries=3,retry_count=3,user_id=2)
    auth_user = DummyUser(1,username="user1",email="test@test.com",password_hash="dummypass",created_at=datetime.now(timezone.utc),role="admin")
    job_repo = DummyJobRepository(job=[created_job])
    execution_repo = DummyExecutionRepository()
    retry_policy = Dummyretry_policy()
    log_repo = DummyLogRepository()
    exec_utor = DummyExecutor(ExecutionResult(status="FAILED",message="Job Failed Successfully"))
    job_service = JobService(job_repo, execution_repo, log_repo, retry_policy,exec_utor)


    with pytest.raises(HTTPException) as exc:
        job_service.get_job_by_id(created_job.id,auth_user.id)

    assert exc.value.status_code == 403

    