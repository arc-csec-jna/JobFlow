
class RetryPolicy:
    def should_retry(self,job):
        return job.retry_count < job.max_retries