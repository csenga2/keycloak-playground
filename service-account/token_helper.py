import jwt
from datetime import datetime, timedelta
import time
import uuid


def create_signed_jwt(client_name, realm_name, private_key):
    now = datetime.now()
    now_plus_10 = now + timedelta(minutes=10)

    return jwt.encode({"jti": str(uuid.uuid4()),
                       "iss": client_name,
                       "aud": "http://localhost:8080/realms/" + realm_name,
                       "sub": client_name,
                       "exp": time.mktime(now_plus_10.timetuple()),
                       "nbf": time.mktime(now.timetuple())
                       }, private_key, headers={"id": str(uuid.uuid4())},
                      algorithm="RS256")


def create_signed_jwt_with_kid(client_name, realm_name, private_key, kid):
    now = datetime.now()
    now_plus_10 = now + timedelta(minutes=10)

    return jwt.encode({"jti": str(uuid.uuid4()),
                       "iss": client_name,
                       "aud": "http://localhost:8080/realms/" + realm_name,
                       "sub": client_name,
                       "exp": time.mktime(now_plus_10.timetuple()),
                       "nbf": time.mktime(now.timetuple())
                       }, private_key, headers={"id": str(uuid.uuid4()),
                                                "kid": kid},
                      algorithm="RS256")
