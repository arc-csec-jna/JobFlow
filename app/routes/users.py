from fastapi import Depends,APIRouter,HTTPException
from app.schemas.User import UserCreate,UserResponse,UserUpdate

from app.dependencies import get_user_service
from app.services.UserService import UserService

router = APIRouter()

@router.post("/users",response_model = UserResponse)
def create_user(user:UserCreate,service:UserService=Depends(get_user_service)):
    return service.create_user(user)

@router.get("/users/{user_id}",response_model=UserResponse)
def get_user_by_id(user_id:int,service:UserService=Depends(get_user_service)):
    return service.get_user_by_id(user_id)

@router.put("/users/{user_id}",response_model=UserResponse)
def update_user(
        user_id:int,
        user_data:UserUpdate,
        service:UserService=Depends(get_user_service)
        ):
    return service.update_user(user_id,user_data)

@router.delete("/users/{user_id}")
def delete_user(user_id:int, service:UserService=Depends(get_user_service)):
   service.delete_user(user_id)
   return {"message":"User deleted successfully"}