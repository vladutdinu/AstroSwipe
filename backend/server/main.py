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


app = FastAPI()

config.DATABASE_URL = 'neo4j+s://{}:{}@{}:{}'.format(os.environ['USER'], os.environ['PASSWORD'], os.environ['SERVER'], os.environ['PORT_NEO'])

db.set_connection(config.DATABASE_URL)
        
@app.get('/')
async def home() -> JSONResponse:
    return JSONResponse("hello world")

@app.post("/create_person")
async def create_student(person: PersonModel) -> JSONResponse:
    person_to_add = person
    person_to_add.unique_id = str(hashlib.sha256(person.email.encode('utf-8')).hexdigest())
    with db.transaction:
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
                age = person_to_add.age
            ).save()
            z = Zodiac.nodes.get(zodiac_sign=person_to_add.zodiac_sign)   
        z.person.connect(p)

        
@app.post("/create_zodiac")
async def create_zodiac(zodiac_sign: ZodiacModel) -> JSONResponse:
    with db.transaction:
        try:
            z = Zodiac.nodes.get(zodiac_sign=zodiac_sign.zodiac_sign)   
        except:
            z = Zodiac(zodiac_sign=zodiac_sign.zodiac_sign).save()


@app.get("/get_zodiac")
async def get_zodiacs(sign) -> JSONResponse:
    with db.transaction:
        zodiacs = Zodiac(zodiac_sign=sign)
        return JSONResponse(zodiacs.__properties__)

@app.get("/get_persons")
async def get_persons() -> JSONResponse:
    with db.transaction:
        persons = Person.nodes.all()
        return_value = {}
        for person in persons:
            return_value.update(person.__dict__)
        return JSONResponse(return_value)

@app.post("/match")
async def match(matches: MatchModel) -> JSONResponse:
    with db.transaction:
       p = Person.nodes.get(unique_id=matches.uuid1)
       p1 = Person.nodes.get(unique_id=matches.uuid2)

       p.matched.connect(p1)

@app.post("/unmatch")
async def unmatch(matches: MatchModel) -> JSONResponse:
    with db.transaction:
       p = Person.nodes.get(unique_id=matches.uuid1)
       p1 = Person.nodes.get(unique_id=matches.uuid2)

       p.matched.disconnect(p1)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info")