from fastapi import FastAPI
from app.routes.jobs import router as jobs_router
from app.routes.executions import router as exec_router
from app.routes.users import router as user_router
from app.routes.auth_route import router as auth_router
from app.core.database import Base, engine
from app.core.logging import log_setup
import logging

Base.metadata.create_all(bind=engine)
log_setup()


logger = logging.getLogger(__name__)
logger.info("JobFlow Application Started")
 
app = FastAPI()

app.include_router(jobs_router)
app.include_router(exec_router)
app.include_router(user_router)
app.include_router(auth_router)