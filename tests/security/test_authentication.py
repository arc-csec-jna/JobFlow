
from tests.security.DummySecurity import DummyUser
from app.services.UserService import UserService
from tests.security.DummyRepo import DummyUserRepository
from app.security.password import hash_password

def test_authentication_by_email():
    # Create a dummy user

    email = "testuser@example.com"
    password = "hashedpassword"


    dummyrepo = DummyUserRepository()
    user_service = UserService(dummyrepo)

    dummy_user = DummyUser(id=1, username="testuser", email=email, password_hash=hash_password(password), created_at="2024-06-01", role="user")

    dummyrepo.create_user(dummy_user)
    authenticated_user = user_service.authenticate_user_by_email(email=email, password=password)

    assert authenticated_user is not None
    assert authenticated_user.email == email