


class DummyJob:
    def __init__(self, job_id, title, enabled=True,next_run_at=None,job_type="dummy", payload=None,status="PENDING",schedule_interval_seconds=60,max_retries = 3,retry_count=0):
        self.id = job_id
        self.title = title
        self.enabled = enabled
        self.next_run_at = next_run_at
        self.job_type = job_type
        self.payload = payload
        self.schedule_interval_seconds = schedule_interval_seconds
        self.priority = "MEDIUM"
        self.retry_count = retry_count
        self.status = status
        self.max_retries = max_retries
        self.user_id = 0  # Assign a default user_id for testing purposes
        self.user = 'admin'  # Assign a default user object for testing purposes
        if payload is None:
            self.payload = {}

class DummyJobRepository:
    def __init__(self,job=None):
        self.job = job or []

    def get_job_runnable(self,current_time):
        # Return a list of dummy jobs for testing
        return self.job
    
    def get_job_by_id(self, job_id):
        for job in self.job:
            if job.id == job_id:
                return job
        return None
    
    def create_job(self, job_data):
        job = DummyJob(
            job_id=len(self.job) + 1,
            title=job_data.title,
            enabled=job_data.enabled,
            next_run_at=job_data.next_run_at,
            job_type=job_data.job_type,
            payload=job_data.payload,
            status=job_data.status,
        )
        self.job.append(job)
        return job
    
    def update_job_status(self, job_id, status):
        job = self.get_job_by_id(job_id)
        if job:
            job.status = status
        return job

    def update_job(self,job_id,job_data):
        job = self.get_job_by_id(job_id)
        if not job:
            return None
        for key,value in job_data.items():
            setattr(job,key,value)
            
        return self.job
    
    def update_retry_count(self,job_id,retry_count):
        return retry_count
    
    def update_next_run_at(self,job_id,next_run):
        return 
    
class DummyDispatcher:
    def __init__(self):
        self.submitted_jobs = []
        
    def submit(self, func, *args, **kwargs):
        self.submitted_jobs.append((func, args, kwargs))
        return DummyFuture()  # Return a dummy future object

class DummyFuture:
    def result(self):
        return None  # Simulate a successful execution

class DummyExecutionRepository:
    def __init__(self):
        self.executions = []
        
    def create_execution(self, execution):
        self.executions.append(execution)
        return execution
    
    def get_execution_by_id(self, execution_id):
        for execution in self.executions:
            if execution.id == execution_id:
                return execution
        return None

    def get_execution_by_job_id(self, job_id):
        for execution in self.executions:
            if execution.job_id == job_id:
                return execution
        return None
    
    def execute_job(self, job):
        # Simulate job execution logic
        return {"status": "FAILED", "attempt": 1}

    def update_execution(self, exec_id, exec_data):
        execution = self.get_execution_by_id(exec_id)
        if not execution:
            return None
        for key, value in exec_data.items():
            setattr(execution, key, value)
        return execution
        
class Dummyretry_policy:
    def should_retry(self, job):
        return job.retry_count < job.max_retries

class DummyExecutor:
    def __init__(self,result):
        self.result = result

    def execute(self, job):
        return self.result

class DummyLogRepository:
    def __init__(self):
        self.logs = []
        
    def create_log(self, log):
        self.logs.append(log)
        return log