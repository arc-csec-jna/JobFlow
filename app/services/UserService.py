from datetime import datetime,timezone

from app.models.User import User
from app.repositories.UserRepository import UserRepository

from app.schemas.User import UserCreate, UserUpdate,UserResponse

from app.security.password import hash_password,verify_password

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def create_user(self, user_create: UserCreate) -> UserResponse:
        password_hash = hash_password(user_create.password)

        user = User(
            username=user_create.username,
            email=user_create.email,
            password_hash=password_hash,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        created_user = self.user_repository.create_user(user)
        return UserResponse.model_validate(created_user)

    def get_user_by_id(self, user_id: int) -> UserResponse:
        user = self.user_repository.get_user_by_id(user_id)
        if user:
            return UserResponse.model_validate(user)
        raise ValueError("User not found")

    def update_user(self, user_id: int, user_update: UserUpdate) -> UserResponse:
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        
        for field, value in user_update.model_dump(exclude_unset=True).items():
            setattr(user, field, value)
        
        updated_user = self.user_repository.update_user(user)
        return UserResponse.model_validate(updated_user)

    def delete_user(self, user_id: int) -> None:
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        
        self.user_repository.delete_user(user)

    def authenticate_user_by_email(self, email: str, password: str) -> UserResponse:
        user = self.user_repository.get_user_by_email(email)
        if not user or not verify_password(password, user.password_hash):
            raise ValueError("Invalid email or password")
        return UserResponse.model_validate(user)
    
    def authenticate_user_by_username(self, username: str, password: str) -> UserResponse:
        user = self.user_repository.get_user_by_username(username)
        if not user or not verify_password(password, user.password_hash):
            raise ValueError("Invalid username or password")
        return UserResponse.model_validate(user)