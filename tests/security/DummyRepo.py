from tests.security.DummySecurity import DummyUser

class DummyUserRepository:
    def __init__(self):
        self.users = {}

    def create_user(self, user: DummyUser):
        self.users[user.id] = user
        return user

    def get_user_by_email(self, email: str):
        for user in self.users.values():
            if user.email == email:
                return user
        return None