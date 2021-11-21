from server.neo4j_model.person import Person
from starlette.responses import JSONResponse
import hashlib
from server.fastapi_model.person_model import PersonModel
import jwt
import time
import os
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
        "expires": time.time() + 3600*6
    }
    
    token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')
    return token

def give_like(p, p1):
    p.likes.connect(p1)
    if p in p1.likes and p1 in p.likes:
        p.matched.connect(p1)
    
def super_like_and_match(p, p1):
    p.likes.connect(p1)
    p.matched.connect(p1)

def like_person(likes):
    p = Person.nodes.get(unique_id=str(
        hashlib.sha256(likes.email1.encode('utf-8')).hexdigest()))
    p1 = Person.nodes.get(unique_id=str(
        hashlib.sha256(likes.email2.encode('utf-8')).hexdigest()))
    if p.user_type == "B":
        if p.like_nr > 0:
            give_like(p, p1)
            p.like_nr-=1
            p.save()
            return True
        else:
            return False
    elif p.user_type == "P" or p.user_type == "A":
        give_like(p, p1)
        
        return True
    

def super_like(likes):
    p = Person.nodes.get(unique_id=str(
        hashlib.sha256(likes.email1.encode('utf-8')).hexdigest()))
    p1 = Person.nodes.get(unique_id=str(
        hashlib.sha256(likes.email2.encode('utf-8')).hexdigest()))
    if p.user_type == "B":
        if p.super_like > 0:
            super_like_and_match(p, p1)
            p.super_like-=1
            p.save()
            return True
        else:
            return False
    elif p.user_type == "P" or p.user_type == "A":
        super_like_and_match(p, p1)
        
        return True


def unmatch_person(matches):
    p = Person.nodes.get(unique_id=str(hashlib.sha256(
        matches.email1.encode('utf-8')).hexdigest()))
    p1 = Person.nodes.get(unique_id=str(hashlib.sha256(
        matches.email2.encode('utf-8')).hexdigest()))
    p.matched.disconnect(p1)
    p.likes.disconnect(p1)
    p1.likes.disconnect(p)


def get_matches(matches):
        res = []
        for match in matches.matched:
            res.append(match.__properties__)
        if len(res) == 0:
            res.append({"message" : "This user has no matches"})
        return res

async def refresh_likes(persons):
    for pers in persons:
        if pers.like_nr != 10:
            pers.like_nr = 10
            pers.save()