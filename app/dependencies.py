from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.executors.python_executor import PythonExecutor
from app.repositories.ExecutionRepository import ExecutionRepository
from app.repositories.job_repository import JobRepository
from app.repositories.log_repository import LogRepository
from app.repositories.UserRepository import UserRepository
from app.services.job_services import JobService
from app.services.UserService import UserService
from app.services.retry_policy import RetryPolicy

from app.security.token import decode_access_token
from app.core.config import settings
from app.security.oauth2 import oauth2_scheme


import jwt

def get_job_service(db: Session = Depends(get_db)):
    job_repository = JobRepository(db)
    execution_repository = ExecutionRepository(db)
    log_repository = LogRepository(db)
    retry_policy= RetryPolicy()
    executor = PythonExecutor()
    return JobService(job_repository=job_repository, execution_repository=execution_repository, log_repository=log_repository,retry_policy=retry_policy,executor = executor)

def get_user_service(db:Session=Depends(get_db)):
    user_repository = UserRepository(db)
    return UserService(user_repository=user_repository)

def get_current_user(
                auth:str = Depends(oauth2_scheme),
                db:Session = Depends(get_db)
                ):
    try:
        payload = decode_access_token(auth,settings.JWT_SECRET)
        user_id = payload["user_id"]
        user_repository = UserRepository(db)
        user = user_repository.get_user_by_id(user_id)
        return user
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")