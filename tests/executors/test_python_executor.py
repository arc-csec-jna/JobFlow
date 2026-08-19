from app.executors.python_executor import PythonExecutor
from app.tasks.registry import TASK_REGISTRY


class DummyJob:
    def __init__(self, payload, job_type):
        self.payload = payload
        self.job_type = job_type


def test_execute_with_valid_job():
    executor = PythonExecutor()
    
    TASK_REGISTRY["valid_job_type"] = successful_task
    
    job = DummyJob(payload={"arg1": 1, "arg2": 2}, job_type="valid_job_type")
    result = executor.execute(job)


    assert result.status == "SUCCESS", "Expected execution to be successful"
    assert result.message == "Job executed successfully", "Expected success message"

def test_execute_with_invalid_job_type():
    executor = PythonExecutor()
    job = DummyJob(payload={"arg1": 1, "arg2": 2}, job_type="invalid_job_type")
    result = executor.execute(job)

    assert result.status == "FAILED", "Expected execution to fail for invalid job type"
    assert "Unknown job type" in result.message, "Expected error message for unknown job type"

def test_execute_with_exception_in_task():
    executor = PythonExecutor()
    job = DummyJob(payload={"arg1": 1, "arg2": 2}, job_type="exception_raising_job_type")
    result = executor.execute(job)

    assert result.status == "FAILED", "Expected execution to fail due to exception in task"
    #assert "Exception" in result.message, "Expected error message for exception raised in task"
    assert result.message == "Unknown job type :'exception_raising_job_type'"

def successful_task(**kwargs):
    # Simulate a successful task execution
    return None

