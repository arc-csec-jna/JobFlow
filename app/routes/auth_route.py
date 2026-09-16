from fastapi import Depends,APIRouter,HTTPException

from app.schemas.auth import LoginRequest,LoginResponse
from app.security.token import create_access_token

from app.dependencies import get_user_service
from app.services.UserService import UserService
from app.core.config import settings

router = APIRouter()

@router.post("/login",response_model=LoginResponse)
def user_login(login_credentials:LoginRequest,service:UserService=Depends(get_user_service)):
    user = service.authenticate_user_by_username(login_credentials.username,login_credentials.password)
    payload = {
        "user_id":user.id,
        "role":user.role
    }
    token = create_access_token(payload,settings.JWT_SECRET)
    return LoginResponse(access_token=token,token_type="bearer")