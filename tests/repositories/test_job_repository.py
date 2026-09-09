import datetime

from app.models.job import Job
from app.repositories.job_repository import JobRepository


def test_create_job(db_session):
    job_repo = JobRepository(db_session)

    job = Job(
    title="Disabled Job",
    job_type="database_backup",
    payload={},
)
    created_job = job_repo.create_job(job)

    assert created_job.id is not None
    assert created_job.title == "Disabled Job"

def test_get_job_runnable_return_religible(db_session):
    job_repo = JobRepository(db_session)

    now = datetime.datetime.now(tz=datetime.timezone.utc)

    due_job = Job(
        title="Due Job",
        job_type="database_backup",
        payload={},
        next_run_at=now - datetime.timedelta(minutes=1),
        enabled=True,
    )

    disabled_job = Job(
        title="Disabled Job",
        job_type="database_backup",
        payload={},
        next_run_at=now - datetime.timedelta(minutes=1),
        enabled=False,
    )

    future_job = Job(
        title="Future Job",
        job_type="database_backup",
        payload={},
        next_run_at=now + datetime.timedelta(minutes=1),
        enabled=True,
    )
    unscheduled_job = Job(
        title="Unscheduled Job",
        job_type="database_backup",
        payload={},
        next_run_at=None,
        enabled=True,
    )

    db_session.add_all([due_job, disabled_job, future_job, unscheduled_job])
    db_session.commit()

    result = job_repo.get_job_runnable(now)

    assert due_job in result
    assert disabled_job not in result
    assert future_job not in result
    assert unscheduled_job not in result



def test_update_retry_count(db_session):
    job_repo = JobRepository(db_session)

    job = Job(
        title="Retry Job",
        job_type="database_backup",
        payload={},
        retry_count=0,
    )
    db_session.add(job)
    db_session.commit()

    updated_job = job_repo.update_retry_count(job.id, 3)

    assert updated_job.retry_count == 3

def test_update_next_run_at (db_session):
    job_repo = JobRepository(db_session)

    job = Job(
        title="Retry Job",
        job_type="database_backup",
        payload={},
        retry_count=0,
    )
    db_session.add(job)
    db_session.commit()

    updated_job = job_repo.update_next_run_at(job.id, datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(minutes=5))

    assert updated_job.next_run_at is not None

def test_update_job_status(db_session):
    job_repo = JobRepository(db_session)

    job = Job(
        title="Status Job",
        job_type="database_backup",
        payload={},
        status="pending",
    )
    db_session.add(job)
    db_session.commit()

    updated_job = job_repo.update_job_status(job.id, "completed")

    assert updated_job.status == "completed"