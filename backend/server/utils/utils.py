from server.neo4j_model.person import Person
from starlette.responses import JSONResponse
import hashlib
from server.fastapi_model.person_model import PersonModel
import jwt
import time
from fastapi.encoders import jsonable_encoder
def check_admin(key):
    ok = 0
    try:
        admin_persons = Person.nodes.filter(user_type='A')
        for person_iter in admin_persons:
            if str(hashlib.sha256((person_iter.unique_id+ 'admin').encode('utf-8')).hexdigest()) == key:
                ok = 1
    except:  
        return JSONResponse(
            status_code=401,
            content={
                "message":"User is not in DB"
            }
        )
    return ok
def check_basic(key):
    ok = 0
    try:
        admin_persons = Person.nodes.filter(user_type='B')
        for person_iter in admin_persons:
            if str(hashlib.sha256((person_iter.unique_id+ 'basic').encode('utf-8')).hexdigest()) == key:
                ok = 1
    except:  
        return JSONResponse(
            status_code=401,
            content={
                "message":"User is not in DB"
            }
        )
    return ok

def check_premium(email, key):
    ok = 0
    try:
        admin_persons = Person.nodes.filter(email=email)
        for person_iter in admin_persons:
            if str(hashlib.sha256((person_iter.unique_id+ 'premium').encode('utf-8')).hexdigest()) == key:
                ok = 1
    except:  
        return JSONResponse(
            status_code=401,
            content={
                "message":"User is not in DB"
            }
        )
    return ok

def decodeJWT(token: str, JWT_SECRET) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return None

def signJWT(person: Person, JWT_SECRET) -> dict:
    payload = {
        "person": jsonable_encoder(person),
        "expires": time.time() + 600
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')

    return token