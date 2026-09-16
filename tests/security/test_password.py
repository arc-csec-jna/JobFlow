from app.security.password import hash_password

def test_password_hashing():
    password = "testpassword"
    hashed_password = hash_password(password)

    assert hashed_password != password  # Ensure the password is hashed
    assert hashed_password.startswith("$argon2")

def test_password_produces_different_hashes_for_same_input():
    password = "testpassword"
    hashed_password1 = hash_password(password)
    hashed_password2 = hash_password(password)

    assert hashed_password1 != hashed_password2