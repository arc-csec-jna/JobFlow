from enum import StrEnum


class JobStatus(StrEnum):
    PENDING ="PENDING"
    RUNNING ="RUNNING"
    SUCCESS="SUCCESS"
    FAILED="FAILED"