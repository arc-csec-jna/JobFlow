
from fastapi import Depends,APIRouter, HTTPException
from app.services.job_services import JobService

from app.dependencies import get_job_service

router = APIRouter()

@router.get("/executions/{execution_id}/logs")
def get_logs_by_execution_id(execution_id: int, service: JobService = Depends(get_job_service)):
    execution = service.get_executions_by_id(execution_id)
    if not execution:
        raise HTTPException(status_code=404, detail="Execution not found")
    return service.get_logs_by_execution_id(execution_id)

@router.get("/executions/{execution_id}")
def get_execution_by_id(execution_id: int, service: JobService = Depends(get_job_service)):
    execution = service.get_executions_by_id(execution_id)
    if not execution:
        raise HTTPException(status_code=404, detail="Execution not found")
    return execution