import jwt

def create_access_token(payload,secret_key):
    token = jwt.encode(payload,secret_key,algorithm="HS256")
    return token

def decode_access_token(token,secret_key):
    values = jwt.decode(token,secret_key,algorithms=["HS256"])
    return values

#some token related helpers
