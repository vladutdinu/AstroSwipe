from enum import unique
from fastapi import Depends, FastAPI
from neomodel import config, db
import os
import uvicorn
import hashlib
import json
from starlette.responses import JSONResponse
from server.neo4j_model.person import Person
from server.neo4j_model.zodiac import Zodiac
from server.fastapi_model.person_model import PersonModel
from server.fastapi_model.zodiac_model import ZodiacModel
from server.fastapi_model.match_model import MatchModel
from server.fastapi_model.login_model import LoginModel
import server.utils.utils as utl

app = FastAPI()

config.DATABASE_URL = 'neo4j+s://{}:{}@{}:{}'.format(os.environ['USER'], os.environ['PASSWORD'], os.environ['SERVER'], os.environ['PORT_NEO'])

db.set_connection(config.DATABASE_URL)
        
@app.get('/')
async def home() -> JSONResponse:
    return JSONResponse("hello world")

@app.get('/login')
async def home(login_model: LoginModel) -> JSONResponse:
    email_hash = str(hashlib.sha256(login_model.email.encode('utf-8')).hexdigest())
    with db.transaction:
        try:
            p = Person.nodes.get(unique_id=email_hash)
            if(p.get_user_type_display() == 'admin'):
                print(p.nodes[0], login_model.email, str(hashlib.sha256((email_hash+ 'admin').encode('utf-8')).hexdigest()))
                return JSONResponse(
                    {
                        "key":str(hashlib.sha256((email_hash+ 'admin').encode('utf-8')).hexdigest())
                    }
                )
            elif(p.get_user_type_display() == 'basic'):
                return JSONResponse(
                    {
                        "key":str(hashlib.sha256((email_hash+ 'basic').encode('utf-8')).hexdigest())
                    }
                )
            elif(p.get_user_type_display() == 'premium'):
                return JSONResponse(
                    {
                        "key":str(hashlib.sha256((email_hash+ 'premium').encode('utf-8')).hexdigest())
                    }
                )
        except:
            return JSONResponse(
                status_code=401,
                content={
                    "message":"User is not in DB"
                }
            )

@app.post("/create_person")
async def create_person(person: PersonModel, key) -> JSONResponse:
    person_to_add = person
    person_to_add.unique_id = str(hashlib.sha256(person.email.encode('utf-8')).hexdigest())
    if utl.check_admin(key) == 1:
        try:
            p = Person.nodes.get(unique_id=person_to_add.unique_id)
            z = Zodiac.nodes.get(zodiac_sign=person_to_add.zodiac_sign)
        except:
            p = Person(
                unique_id = person_to_add.unique_id,
                email = person_to_add.email,
                first_name = person_to_add.first_name,
                last_name = person_to_add.last_name,
                zodiac_sign = person_to_add.zodiac_sign,
                personal_bio = person_to_add.personal_bio,
                age = person_to_add.age,
                user_type = person_to_add.user_type
            ).save()
            z = Zodiac.nodes.get(zodiac_sign=person_to_add.zodiac_sign)  
            #print(p.get_user_type_display()) 
        z.person.connect(p)
    else:
        return JSONResponse(
            status_code=401,
            content={
                "message":"User is not in DB"
            }
        )

        
@app.post("/create_zodiac")
async def create_zodiac(zodiac_sign: ZodiacModel, key: str) -> JSONResponse:
    with db.transaction:
        if utl.check_admin(key) == 1:
            try:
                z = Zodiac.nodes.get(zodiac_sign=zodiac_sign.zodiac_sign)   
            except:
                z = Zodiac(zodiac_sign=zodiac_sign.zodiac_sign).save()
        else:
            return JSONResponse(
                status_code=401,
                content={
                    "message":"User is not in DB"
                }
            )

@app.get("/get_zodiac")
async def get_zodiacs(sign, key) -> JSONResponse:
    with db.transaction:
        if utl.check_admin(key) == 1:
            zodiacs = Zodiac.nodes.get(zodiac_sign=sign)
            return JSONResponse(zodiacs.__properties__)
        else:
            return JSONResponse(
                status_code=401,
                content={
                    "message":"User is not in DB"
                }
            )

@app.get("/get_persons")
async def get_persons(key) -> JSONResponse:
    with db.transaction:
        if utl.check_admin(key) == 1:
            persons = Person.nodes.all()
            return_value = []
            for person in persons:
                return_value.append(person.__properties__)
            
            return JSONResponse(return_value)
        else:
            return JSONResponse(
                status_code=401,
                content={
                    "message":"User is not in DB"
                }
            )

@app.post("/match")
async def match(matches: MatchModel) -> JSONResponse:
    with db.transaction:
       p = Person.nodes.get(unique_id=str(hashlib.sha256(matches.email1.encode('utf-8')).hexdigest()))
       p1 = Person.nodes.get(unique_id=str(hashlib.sha256(matches.email2.encode('utf-8')).hexdigest()))
       p.matched.connect(p1)

@app.post("/unmatch")
async def unmatch(matches: MatchModel) -> JSONResponse:
    with db.transaction:
       p = Person.nodes.get(unique_id=str(hashlib.sha256(matches.email1.encode('utf-8')).hexdigest()))
       p1 = Person.nodes.get(unique_id=str(hashlib.sha256(matches.email2.encode('utf-8')).hexdigest()))
       p.matched.disconnect(p1)

@app.get("/get_matches")
async def get_matches(email, key) -> JSONResponse:
    with db.transaction:
        if utl.check_admin(key) == 1:
            try:
                matches = Person.nodes.get(unique_id=str(hashlib.sha256(email.encode('utf-8')).hexdigest()))
                result = []
                for match in matches.matched:
                    result.append(match.__properties__)
                return JSONResponse(
                    status_code=200,
                    content = result,
                    headers={
                        "type":"admin"
                    })
            except:
                return JSONResponse(
                    status_code=401,
                    content = {"message":"User is not in DB"},
                )
        if utl.check_premium(email, key) == 1:
            try:
                matches = Person.nodes.get(unique_id=str(hashlib.sha256(email.encode('utf-8')).hexdigest()))
                result = []
                for match in matches.matched:
                    result.append(match.__properties__)
                return JSONResponse(
                    status_code=200,
                    content = result,
                    headers={
                        "type":"premium"
                    })
            except:
                return JSONResponse(
                    status_code=401,
                    content = {"message":"User is not in DB"},
                )
        elif utl.check_basic(key) == 1:
            print(0)
            try:
                matches = Person.nodes.get(unique_id=str(hashlib.sha256(email.encode('utf-8')).hexdigest()))
                result = []
                for match in matches.matched:
                    result.append(match.__properties__)
                return JSONResponse(
                    status_code=200,
                    content = result,
                    headers={
                        "type":"basic"
                    })
            except:
                return JSONResponse(
                    status_code=401,
                    content = {"message":"User is not in DB"},
                )
        else:
            return JSONResponse(
                status_code=401,
                content={
                    "message":"User is not in DB"
                }
            )

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info")