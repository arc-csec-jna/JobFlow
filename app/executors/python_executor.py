from app.tasks.registry import TASK_REGISTRY
from app.contracts.execution_result import ExecutionResult

class PythonExecutor:
    def execute(self, job):
        # Implement the logic to execute the Python job here
        try:
            # we are going to have a folder where functions live
            payload = job.payload
            job_type = job.job_type
            # Assuming the payload contains the function name and arguments

            # Retrieve the function from the registry
            task = TASK_REGISTRY.get(job_type)
            if not task:
                raise ValueError(f"Unknown job type :'{job_type}'")
            task(**payload)

            return ExecutionResult(status="SUCCESS", message="Job executed successfully")
        except Exception as e:
            return ExecutionResult(status="FAILED", message=str(e))
