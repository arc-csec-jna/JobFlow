from app.security.token import create_access_token,decode_access_token

def test_create_and_decode_access_token():
    payload = {
        "user_id":123,
        "role":"admin"
    }
    secret_key = "test_secret_key_that_is_at_least_32_bytes"
    token = create_access_token(payload,secret_key)
    decoded = decode_access_token(token,secret_key)

    assert decoded == payload
