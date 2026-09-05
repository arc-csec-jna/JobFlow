from app.services.retry_policy import RetryPolicy

class DummyJob:
    def __init__(self, retry_count,max_retries):
        self.retry_count = retry_count
        self.max_retries = max_retries

def test_should_retry_when_retry_at_limit():
    policy = RetryPolicy()
    job = DummyJob(retry_count=3, max_retries=3)
    result = policy.should_retry(job)

    assert result == False, "Expected should_retry to return False when retry_count is equal to max_retries"

def test_should_not_retry_when_retry_over_limit():
    policy = RetryPolicy()
    job = DummyJob(retry_count=4, max_retries=3)
    result = policy.should_retry(job)

    assert result == False, "Expected should_retry to return False when retry_count is greater than max_retries"