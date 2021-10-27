from enum import unique
from fastapi import Depends, FastAPI
from neomodel import config, db
import os
import uvicorn
import hashlib
import json
import requests
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from starlette.responses import JSONResponse
from server.neo4j_model.person import Person
from server.neo4j_model.zodiac import Zodiac
from server.fastapi_model.person_model import PersonModel
from server.fastapi_model.zodiac_model import ZodiacModel
from server.fastapi_model.match_model import MatchModel
from server.fastapi_model.like_model import LikeModel
from server.fastapi_model.login_model import LoginModel

import server.utils.utils as utl

STATUS_CODES = {
    "FOUND_USER_CODE": 230,
    "FOUND_USER_MESSAGE": "USER ALREADY IN DATABASE",
    "ACTIVATED_USER_CODE": 231,
    "ACTIVATED_USER_MESSAGE": "USER HAS BEEN ACTIVATED"
}

app = FastAPI()
conf = ConnectionConfig(
    MAIL_USERNAME=os.environ['FASTAPI_USER'],
    MAIL_PASSWORD=os.environ['FASTAPI_PASS'],
    MAIL_FROM="astroswipe2021@gmail.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)
config.DATABASE_URL = 'neo4j+s://{}:{}@{}:{}'.format(
    os.environ['USER'], os.environ['PASSWORD'], os.environ['SERVER'], os.environ['PORT_NEO'])

db.set_connection(config.DATABASE_URL)
html = """
Thanks for registering to Astro swipe!
This is your verification link: {}/code_verif?token={}

Please click on the link to complete the registration
"""


@app.post('/register')
async def simple_send(person: PersonModel) -> JSONResponse:
    uuid = str(hashlib.sha256(person.email.encode('utf-8')).hexdigest())
    with db.transaction:
        try:
            p = Person.nodes.get(unique_id=uuid)
            z = Zodiac.nodes.get(zodiac_sign=person.zodiac_sign)
            return JSONResponse(
                status_code=STATUS_CODES['FOUND_USER_CODE'],
                content={
                    "message": STATUS_CODES['FOUND_USER_MESSAGE']
                }
            )
        except:
            p = Person(
                unique_id=person.unique_id,
                email=person.email,
                first_name=person.first_name,
                last_name=person.last_name,
                zodiac_sign=person.zodiac_sign,
                personal_bio=person.personal_bio,
                age=person.age,
                user_type=person.user_type
            ).save()
            z = Zodiac.nodes.get(zodiac_sign=person.zodiac_sign)
        z.person.connect(p)

    token = utl.signJWT(person, os.environ['JWT_SECRET_FASTAPI'])

    message = MessageSchema(
        subject="Astroswipe account validation",
        recipients=[person.email],
        body=html.format(os.environ['FASTAPI_URL'], token)
    )
    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})


@app.get('/code_verif')
async def code_verif(token: str) -> JSONResponse:
    payload = utl.decodeJWT(token, os.environ['JWT_SECRET_FASTAPI'])
    if payload is not None:
        uuid = str(hashlib.sha256(
            payload['person']['email'].encode('utf-8')).hexdigest())
        with db.transaction:
            p = Person.nodes.get(unique_id=uuid)
            z = Zodiac.nodes.get(zodiac_sign=payload['person']['zodiac_sign'])
            p.activated = True
            return JSONResponse(
                status_code=STATUS_CODES["ACTIVATED_USER_CODE"],
                content={"message": STATUS_CODES["ACTIVATED_USER_MESSAGE"]}
            )
    else:
        return JSONResponse(
            status_code=404,
            content={"message": "Wrong URL"}
        )


@app.get('/')
async def home() -> JSONResponse:
    return JSONResponse("hello world")


@app.get('/login')
async def home(login_model: LoginModel) -> JSONResponse:
    email_hash = str(hashlib.sha256(
        login_model.email.encode('utf-8')).hexdigest())
    with db.transaction:
        try:
            p = Person.nodes.get(unique_id=email_hash)
            token = utl.signJWT(p, os.environ['JWT_SECRET_FASTAPI'])
            return JSONResponse(
                status_code=200,
                content={
                    "token": str(token, "utf-8")
                }
            )
        except:
            return JSONResponse(
                status_code=401,
                content={
                    "message": "User is not in DB"
                }
            )


@app.post("/create_person")
async def create_person(person: PersonModel, token) -> JSONResponse:
    person_to_add = person
    person_to_add.unique_id = str(hashlib.sha256(
        person.email.encode('utf-8')).hexdigest())
    payload = utl.decodeJWT(token, os.environ['JWT_SECRET_FASTAPI'])
    if payload is not None:
        if payload['person']['user_type'] == 'A':
            try:
                p = Person.nodes.get(unique_id=person_to_add.unique_id)
                z = Zodiac.nodes.get(zodiac_sign=person_to_add.zodiac_sign)
            except:
                p = Person(
                    unique_id=person_to_add.unique_id,
                    email=person_to_add.email,
                    first_name=person_to_add.first_name,
                    last_name=person_to_add.last_name,
                    zodiac_sign=person_to_add.zodiac_sign,
                    personal_bio=person_to_add.personal_bio,
                    age=person_to_add.age,
                    user_type=person_to_add.user_type
                ).save()
                z = Zodiac.nodes.get(zodiac_sign=person_to_add.zodiac_sign)
                # print(p.get_user_type_display())
            z.person.connect(p)
        else:
            return JSONResponse(
                status_code=403,
                content={
                    "message": "User does not have the privileges to create users"
                }
            )
    else:
        return JSONResponse(
            status_code=401,
            content={
                "message": "User is not in database"
            }
        )


@app.post("/create_zodiac")
async def create_zodiac(zodiac_sign: ZodiacModel, token: str) -> JSONResponse:
    with db.transaction:
        payload = utl.decodeJWT(token, os.environ['JWT_SECRET_FASTAPI'])
        if payload is not None:
            if payload['person']['user_type'] == 'A':
                try:
                    z = Zodiac.nodes.get(zodiac_sign=zodiac_sign.zodiac_sign)
                except:
                    z = Zodiac(zodiac_sign=zodiac_sign.zodiac_sign).save()
        else:
            return JSONResponse(
                status_code=401,
                content={
                    "message": "User is not in DB"
                }
            )


@app.get("/get_zodiac")
async def get_zodiacs(sign, token) -> JSONResponse:
    with db.transaction:
        payload = utl.decodeJWT(token, os.environ['JWT_SECRET_FASTAPI'])
        if payload is not None:
            if payload['person']['user_type'] == 'A':
                zodiacs = Zodiac.nodes.get(zodiac_sign=sign)
            return JSONResponse(zodiacs.__properties__)
        else:
            return JSONResponse(
                status_code=401,
                content={
                    "message": "User is not in DB"
                }
            )


@app.get("/get_persons")
async def get_persons(token) -> JSONResponse:
    with db.transaction:
        payload = utl.decodeJWT(token, os.environ['JWT_SECRET_FASTAPI'])
        if payload is not None:
            if payload['person']['user_type'] == 'A':
                persons = Person.nodes.all()
                return_value = []
                for person in persons:
                    return_value.append(person.__properties__)

                return JSONResponse(return_value)
        else:
            return JSONResponse(
                status_code=401,
                content={
                    "message": "User is not in DB"
                }
            )

@app.get("/get_persons_by_zodiac")
async def get_persons(token, zodiac) -> JSONResponse:
    with db.transaction:
        payload = utl.decodeJWT(token, os.environ['JWT_SECRET_FASTAPI'])
        if payload is not None:
            if payload['person']['user_type'] == 'A':
                persons = Person.nodes.filter(zodiac_sign=zodiac)
                return_value = []
                for person in persons:
                    return_value.append(person.__properties__)
                return JSONResponse(return_value)
        else:
            return JSONResponse(
                status_code=401,
                content={
                    "message": "User is not in DB"
                }
            )


@app.post("/like")
async def match(likes: LikeModel, token) -> JSONResponse:
    with db.transaction:
        payload = utl.decodeJWT(token, os.environ['JWT_SECRET_FASTAPI'])
        if payload is not None:
            p = Person.nodes.filter(unique_id=str(
                hashlib.sha256(likes.email1.encode('utf-8')).hexdigest()))
            p1 = Person.nodes.filter(unique_id=str(
                hashlib.sha256(likes.email2.encode('utf-8')).hexdigest()))
            p[0].likes.connect(p1[0])

            if p[0] in p1[0].likes and p1[0] in p[0].likes:
                p[0].matched.connect(p1[0])


@app.post("/unmatch")
async def unmatch(matches: MatchModel, token) -> JSONResponse:
    with db.transaction:
        payload = utl.decodeJWT(token, os.environ['JWT_SECRET_FASTAPI'])
        if payload is not None:
            p = Person.nodes.get(unique_id=str(hashlib.sha256(
                matches.email1.encode('utf-8')).hexdigest()))
            p1 = Person.nodes.get(unique_id=str(hashlib.sha256(
                matches.email2.encode('utf-8')).hexdigest()))
            p.matched.disconnect(p1)
            p[0].likes.disconnect(p1[0])
            p1[0].likes.disconnect(p[0])


@app.get("/get_matches")
async def get_matches(token) -> JSONResponse:
    with db.transaction:
        payload = utl.decodeJWT(token, os.environ['JWT_SECRET_FASTAPI'])
        if payload is not None:
            if payload['person']['user_type'] == 'A':
                try:
                    matches = Person.nodes.get(unique_id=str(
                        hashlib.sha256(payload['person']['email'].encode('utf-8')).hexdigest()))
                    result = []
                    for match in matches.matched:
                        result.append(match.__properties__)
                    return JSONResponse(
                        status_code=200,
                        content=result,
                        headers={
                            "type": "admin"
                        })
                except:
                    return JSONResponse(
                        status_code=401,
                        content={"message": "User is not in DB"},
                    )

            if payload['person']['user_type'] == 'P':
                try:
                    matches = Person.nodes.get(unique_id=str(
                        hashlib.sha256(payload['person']['email'].encode('utf-8')).hexdigest()))
                    result = []
                    for match in matches.matched:
                        result.append(match.__properties__)
                    return JSONResponse(
                        status_code=200,
                        content=result,
                        headers={
                            "type": "premium"
                        })
                except:
                    return JSONResponse(
                        status_code=401,
                        content={"message": "User is not in DB"},
                    )

            if payload['person']['user_type'] == 'B':
                try:
                    matches = Person.nodes.get(unique_id=str(
                        hashlib.sha256(payload['person']['email'].encode('utf-8')).hexdigest()))
                    result = []
                    for match in matches.matched:
                        result.append(match.__properties__)
                    return JSONResponse(
                        status_code=200,
                        content=result,
                        headers={
                            "type": "basic"
                        })
                except:
                    return JSONResponse(
                        status_code=401,
                        content={"message": "User is not in DB"},
                    )
        else:
            return JSONResponse(
                status_code=401,
                content={
                    "message": "User is not in DB"
                }
            )

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info")
