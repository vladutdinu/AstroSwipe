from server.neo4j_model.person import Person
from starlette.responses import JSONResponse
import hashlib
from server.fastapi_model.person_model import PersonModel
import jwt
import time
from fastapi.encoders import jsonable_encoder

def decodeJWT(token: str, JWT_SECRET) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return None

def signJWT(person: Person, JWT_SECRET) -> dict:
    payload = {
        "person": person.__properties__,
        "expires": time.time() + 600
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')

    return token