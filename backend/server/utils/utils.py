from server.neo4j_model.person import Person
from starlette.responses import JSONResponse
import hashlib
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

def check_if_user_exists(key):
    pass