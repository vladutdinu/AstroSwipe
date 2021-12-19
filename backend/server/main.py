from enum import unique
from typing import List, Optional
from fastapi import Depends, FastAPI, BackgroundTasks
from fastapi.param_functions import Query
from fastapi.middleware.cors import CORSMiddleware
from neomodel import config, db
import os
import uvicorn
import hashlib
import json
import requests
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from neomodel import Q
from fastapi_utils.tasks import repeat_every
from starlette.responses import JSONResponse
from server.neo4j_model.person import Person
from server.neo4j_model.zodiac import Zodiac
from server.fastapi_model.person_model import PersonModel
from server.fastapi_model.zodiac_model import ZodiacModel
from server.fastapi_model.match_model import MatchModel
from server.fastapi_model.bio_model import BioModel
from server.fastapi_model.like_model import LikeModel
from server.fastapi_model.login_model import LoginModel
from server.fastapi_model.register_model import RegisterModel
import server.utils.utils as utl

STATUS_CODES = {
    "FOUND_USER_CODE": 230,
    "FOUND_USER_MESSAGE": "USER ALREADY IN DATABASE",
    "ACTIVATED_USER_CODE": 231,
    "ACTIVATED_USER_MESSAGE": "USER HAS BEEN ACTIVATED",
    "LIKED_USER_CODE": 232,
    "LIKED_USER_MESSAGE": "USER HAS SUCESSFULY LIKED ANOTHER USER",
    "UNMATCH_USER_CODE": 233,
    "UNMATCH_USER_MESSAGE": "USER HAS SUCESSFULY UNMATCH ANOTHER USER",
    "NOT_ENOUGH_LIKES_CODE": 490,
    "NOT_ENOUGH_LIKES_MESSAGE": "USER DOES NOT HAVE ENOUGH LIKES",
    "NOT_ACTIVATED_USER_CODE": 491,
    "NOT_ACTIVATED_USER_MESSAGE": "USER HAS NOT ACTIVATED"
}

app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
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
This is your verification link: 
{}

Please click on the link to complete the registration
"""
@app.on_event("startup")
@repeat_every(seconds=60*60) 
async def startup_event():
    persons = Person.nodes.all()
    await utl.refresh_likes(persons)

@app.post('/register_step1')
async def register_step1(register: RegisterModel) -> JSONResponse:
    if register.password != register.conf_password:
        return JSONResponse(
            status_code=406,
            content={
                "message": "Passwords does not match"
            }
        )
    else:
        uuid = str(hashlib.sha256(register.email.encode('utf-8')).hexdigest())
        hashed_pass = str(hashlib.sha256(register.password.encode('utf-8')).hexdigest())
        with db.transaction:
            try:
                p = Person.nodes.get(unique_id=uuid)
                return JSONResponse(
                    status_code=STATUS_CODES['FOUND_USER_CODE'],
                    content={
                        "message": STATUS_CODES['FOUND_USER_MESSAGE']
                    }
                )
            except:
                p = Person(
                    unique_id=uuid,
                    email=register.email,
                    password=hashed_pass
                ).save()  

@app.post('/register_step2')
async def register_step2(person: PersonModel) -> JSONResponse:
    with db.transaction:
        uuid = str(hashlib.sha256(person.email.encode('utf-8')).hexdigest())
        p = Person.nodes.get(unique_id=uuid)
        p.first_name  =person.first_name 
        p.last_name   =person.last_name  
        p.zodiac_sign =person.zodiac_sign
        p.personal_bio=person.personal_bio
        p.age         =person.age   
        p.country     =person.country
        p.city        =person.city
        p.sex         =person.sex
        p.user_type   =person.user_type
        p.preffered_zodiac_sign = person.preffered_zodiac_sign
        p.super_like  = 2   
        z = Zodiac.nodes.get(zodiac_sign=p.zodiac_sign)
        p.save()
        z.person.connect(p)

    token = utl.signJWT(p, os.environ['JWT_SECRET_FASTAPI'])

    message = MessageSchema(
        subject="Astroswipe account validation",
        recipients=[p.email],
        body=html.format(str(token, "utf-8"))
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
            p.activated = True
            p.save()
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

@app.post('/login')
async def home(login_model: LoginModel) -> JSONResponse:
    email_hash = str(hashlib.sha256(
        login_model.email.encode('utf-8')).hexdigest())
    pass_hash = str(hashlib.sha256(
        login_model.password.encode('utf-8')).hexdigest())
    with db.transaction:
        try:
            p = Person.nodes.get(unique_id=email_hash, password=pass_hash)
            if p.activated == False:
                return JSONResponse(
                    status_code= STATUS_CODES["NOT_ACTIVATED_USER_CODE"],
                    content=STATUS_CODES["NOT_ACTIVATED_USER_MESSAGE"]
                )
            else:
                token = utl.signJWT(p, os.environ['JWT_SECRET_FASTAPI'])
                return JSONResponse(
                    status_code=200,
                    content={
                        "token": str(token, "utf-8")
                    }
                )
        except:
            return JSONResponse(
                status_code=401
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
                    preffered_zodiac_sign=person_to_add.preffered_zodiac_sign,
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
            status_code=401
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
                status_code=401
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
                status_code=401
            )

@app.get("/get_persons_by_zodiac")
async def get_persons_by_zodiac(token) -> JSONResponse:
    with db.transaction:
        payload = utl.decodeJWT(token, os.environ['JWT_SECRET_FASTAPI'])
        email_hash = str(hashlib.sha256(payload['person']['email'].encode('utf-8')).hexdigest())
        p = Person.nodes.get(unique_id=email_hash)
        if payload is not None:
            return_value = []
            persons = Person.nodes.filter(zodiac_sign=payload['person']['preffered_zodiac_sign'])
            print(p.__properties__)
            for person in persons:
                #if person.unique_id != p.likes.relationship(person).end_node().unique_id:
                    return_value.append(person.__properties__)
            return JSONResponse(return_value)
        else:
            return JSONResponse(
                status_code=401
            )

@app.get("/get_persons_by_sex")
async def get_persons_by_sex(token, sex) -> JSONResponse:
    with db.transaction:
        payload = utl.decodeJWT(token, os.environ['JWT_SECRET_FASTAPI'])
        if payload is not None:
            return_value = []
            persons = Person.nodes.filter(sex=sex)
            for person in persons:
                    return_value.append(person.__properties__)
            return JSONResponse(return_value)
        else:
            return JSONResponse(
                status_code=401
            )

@app.get("/get_persons_by_age")
async def get_persons_by_age(token) -> JSONResponse:
    with db.transaction:
        payload = utl.decodeJWT(token, os.environ['JWT_SECRET_FASTAPI'])
        if payload is not None:
            return_value = []
            p = Person.nodes.get(unique_id=str(
                hashlib.sha256(payload['person']['email'].encode('utf-8')).hexdigest()))
            
            var1 = p.pref_age1      
            var2 = p.pref_age2
            print(p)         
            for i in range(var1, var2):
                try:
                    persons = Person.nodes.filter(age = i)
                    print(persons)
                    for person in persons:
                            return_value.append(person.__properties__)
                except:
                    pass
            return JSONResponse(return_value)
        else:
            return JSONResponse(
                status_code=401
            )

@app.post("/superlike")
async def superlike(likes: LikeModel, token) -> JSONResponse:
    with db.transaction:
        payload = utl.decodeJWT(token, os.environ['JWT_SECRET_FASTAPI'])
        if payload is not None:
            if utl.super_like(likes):
                return JSONResponse(
                    status_code=STATUS_CODES['LIKED_USER_CODE'],
                    content={
                        "message": STATUS_CODES['LIKED_USER_MESSAGE'],
                        "token" : token
                    }
                )
            else:
                return JSONResponse(
                    status_code=STATUS_CODES['NOT_ENOUGH_LIKES_CODE'],
                    content={
                        "message": STATUS_CODES['NOT_ENOUGH_LIKES_MESSAGE'],
                        "token" : token
                    }
                )
        else:
            return JSONResponse(
                status_code=401
            )

@app.post("/like")
async def like(likes: LikeModel, token) -> JSONResponse:
    with db.transaction:
        payload = utl.decodeJWT(token, os.environ['JWT_SECRET_FASTAPI'])
        if payload is not None:
            like_action, matched = utl.like_person(likes)
            if like_action:
                return JSONResponse(
                    status_code=STATUS_CODES['LIKED_USER_CODE'],
                    content={
                        "message": STATUS_CODES['LIKED_USER_MESSAGE'],
                        "matched": matched,
                        "token" : token
                    }
                )
            else:
                return JSONResponse(
                    status_code=STATUS_CODES['NOT_ENOUGH_LIKES_CODE'],
                    content={
                        "message": STATUS_CODES['NOT_ENOUGH_LIKES_MESSAGE'],
                        "matched": False,
                        "token" : token
                    }
                )
        else:
            return JSONResponse(
                status_code=401
            )

@app.post("/unmatch")
async def unmatch(matches: MatchModel, token) -> JSONResponse:
    with db.transaction:
        payload = utl.decodeJWT(token, os.environ['JWT_SECRET_FASTAPI'])
        if payload is not None:
            utl.unmatch_person(matches)
            return JSONResponse(
                status_code=STATUS_CODES['UNMATCH_USER_CODE'],
                content={
                    "message": STATUS_CODES['UNMATCH_USER_MESSAGE'],
                    "token" : token
                }
            )
        else:
            return JSONResponse(
                status_code=401
            )


@app.get("/get_matches")
async def get_matches(token) -> JSONResponse:
    with db.transaction:
        payload = utl.decodeJWT(token, os.environ['JWT_SECRET_FASTAPI'])
        if payload is not None:
            matches = Person.nodes.get(unique_id=str(
                hashlib.sha256(payload['person']['email'].encode('utf-8')).hexdigest()))
            data = utl.get_matches(matches)
            return JSONResponse(
                status_code=200,
                content=data,
                headers={
                    "user_type" : payload['person']['user_type']
                }
            )
        else:
            return JSONResponse(
                status_code=401
            )

@app.post('/update_bio')
async def update_bio(token, bio_model: BioModel):
    with db.transaction:
        payload = utl.decodeJWT(token, os.environ['JWT_SECRET_FASTAPI'])
        
        if payload is not None:
            p = Person.nodes.get(unique_id=str(
                hashlib.sha256(payload['person']['email'].encode('utf-8')).hexdigest()))
            p.country = bio_model.country
            p.city = bio_model.city
            p.personal_bio = bio_model.personal_bio
            p.preffered_zodiac_sign = bio_model.preffered_zodiac_sign
            p.pref_age1 = bio_model.pref_age1
            p.pref_age2 = bio_model.pref_age2
            p.save()
            return JSONResponse(
                status_code=200,
                content={
                    "token": str(utl.signJWT(p, os.environ['JWT_SECRET_FASTAPI']), "utf-8")
                }
            )

@app.post('/become_premium')
async def become_premium(token):
    with db.transaction:
        payload = utl.decodeJWT(token, os.environ['JWT_SECRET_FASTAPI'])
        print(token)
        if payload is not None:
            p = Person.nodes.get(unique_id=str(
                hashlib.sha256(payload['person']['email'].encode('utf-8')).hexdigest()))
            print(p)
            p.user_type = 'P'
            p.super_like = 5
            p.save()
            return JSONResponse(
                status_code=200,
                content={
                    "token": str(utl.signJWT(p, os.environ['JWT_SECRET_FASTAPI']), "utf-8")
                }
            )

"""
    to do : jwt decode and code in front pe servicii pt update bio
    to do : become premium
"""


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info")