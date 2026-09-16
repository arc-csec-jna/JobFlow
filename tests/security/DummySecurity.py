class DummyUser:
    def __init__(self, id: int, username: str, email: str, password_hash: str,created_at, role: str = "user"):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.created_at = created_at
        self.role = role