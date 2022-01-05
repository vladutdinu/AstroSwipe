import unittest
from unittest.mock import MagicMock
import requests

token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwZXJzb24iOnsidW5pcXVlX2lkIjoiNGMzZjFlNmNmOGYwNjliZjRiZjIxMjNjNGQxNjBhYTgzNWU3OWNlOTU1ZTQ5ODEwODA5MGQ1NWEwYzlkNmJhNiIsImVtYWlsIjoicG9wYW1vcmVuYTNAZ21haWwuY29tIiwicGFzc3dvcmQiOiI1Yzc3ZDdmZDhmNTFlZDBjMmE5MTNlNDYzMjZmZjZkMmVhMmU5NWM4ZWNmMTY2N2M3MmViNzJjY2MzZmMyYjQ2IiwiZmlyc3RfbmFtZSI6ImFzZHNhZCIsImxhc3RfbmFtZSI6ImFzZGFzIiwiY291bnRyeSI6ImRzYSIsImNpdHkiOiJkYXMiLCJzZXgiOiJNIiwicHJlZmZlcmVkX3pvZGlhY19zaWduIjoiR2VtaW5pIiwiem9kaWFjX3NpZ24iOiJBcmllcyIsInBlcnNvbmFsX2JpbyI6ImFzZGFzIiwiYWdlIjoyMiwiYWN0aXZhdGVkIjpmYWxzZSwibGlrZV9uciI6MTAsInVzZXJfdHlwZSI6IkIiLCJwcmVmX2FnZTEiOjEsInByZWZfYWdlMiI6MSwic3VwZXJfbGlrZSI6MiwiaWQiOjEzfSwiZXhwaXJlcyI6MTY0MTQxNjY1OC43Nzg0MzY0fQ.AcxPIGF_4R4CLGu6F1g4gNkygfcYY9kmtbz8YEspD-I"
class RegistrationTest(unittest.TestCase):

    def PasswordsNotMatch(self):
        reg ='{"email": "popamorena3@gmail.com","password": "kid","conf_password": "kd"}'
        res='{"message":"Passwords does not match"}'
        response = requests.post("http://localhost:8000/register_step1", data = reg)
        try:
            self.assertEqual(response.content.decode('utf-8'), res)
            print("Test 1 succesful")
        except:
            print("Test 1 failed")

    def UserAlreadyInDatabase(self):
        reg ='{"email": "popamorena3@gmail.com","password": "kid","conf_password": "kid"}'
        res='{"message":"USER ALREADY IN DATABASE"}'
        response = requests.post("http://localhost:8000/register_step1", data = reg)
        try:
            self.assertEqual(response.content.decode('utf-8'), res)
            print("Test 2 succesful")
        except:
            print("Test 2 failed")


    def code_verifFaild(self):
        res='{"detail":"Method Not Allowed"}'
        response = requests.post("http://localhost:8000/code_verif?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwZXJzb24OnsidW5pcXVlX2lkIjoiNGMzZjFlNmNmOGYwNjliZjRiZjIxMjNjNGQxNjBhYTgzNWU3OWNlOTU1ZTQ5ODEwODA5MGQ1NWEwYzlkNmJhNiIsImVtYWlsIjoicG9wYW1vcmVuYTNAZ21haWwuY29tIiwicGFzc3dvcmQiOiI1Yzc3ZDdmZDhmNTFlZDBjMmE5MTNlNDYzMjZmZjZkMmVhMmU5NWM4ZWNmMTY2N2M3MmViNzJjY2MzZmMyYjQ2IiwiZmlyc3RfbmFtZSI6Ik1vcmVuYSIsImxhc3RfbmFtZSI6IlBvcGEiLCJjb3VudHJ5IjoiUm9tYW5pYSIsImNpdHkiOiJCYWNhdSIsInNleCI6IkYiLCJwcmVmZmVyZWRfem9kaWFjX3NpZ24iOiIiLCJ6b2RpYWNfc2lnbiI6IkdlbWluaSIsInBlcnNvbmFsX2JpbyI6IkRvcmVzYyB1biBiYXJiYXQgbWVzdGVyIiwiYWdlIjoyMSwiYWN0aXZhdGVkIjp0cnVlLCJsaWtlX25yIjoxMCwidXNlcl90eXBlIjoiUCIsInByZWZfYWdlMSI6MSwicHJlZl9hZ2UyIjoxLCJzdXBlcl9saWtlIjoyLCJpZCI6MTJ9LCJleHBpcmVzIjoxNjM3ODAyMTk1Ljg0OTQwODF9.8y64AjgQfjklIfDNwVqqLJTFVuoVRZLLSWWBcg4X6l4")
        try:
            print(response.content.decode('utf-8'))
            self.assertEqual(response.content.decode('utf-8'), res)
            print("Test 3 succesful")
        except:
            print("Test 3 failed")


    def get_personsWorks(self):
        reg ='{"email": "popamorena3@gmail.com","password": "kid","conf_password": "kid"}'
   
        response = requests.post("http://localhost:8000/get_persons?token="+token)
        try:
            print(response.status_code)
            self.assertEqual(response.status_code, 200)
            print("Test 4 succesful")
        except:
            print("Test 4 failed")


    def get_personsFaild(self):
        reg ='{"email": "popamorena3@gmail.com","password": "kid","conf_password": "kid"}'
   
        response = requests.post("http://localhost:8000/get_persons?token=0")
        try:
            print(response.status_code)
            self.assertEqual(response.status_code, 401)
            print("Test 5 succesful")
        except:
            print("Test 5 failed")


    def get_zodiacWorks(self):
        reg ='{"email": "popamorena3@gmail.com","password": "kid","conf_password": "kid"}'

        response = requests.post("http://localhost:8000/get_zodiac?sign=taurus&token="+token)
        try:
            print(response.status_code)
            self.assertEqual(response.status_code, 200)
            print("Test 6 succesful")
        except:
            print("Test 6 failed")

    def get_zodiacFaild(self):
        reg ='{"email": "popamorena3@gmail.com","password": "kid","conf_password": "kid"}'
        
        response = requests.post("http://localhost:8000/get_zodiac?sign=taurus&token=0")
        try:
            print(response.status_code)
            self.assertEqual(response.status_code, 401)
            print("Test 7 succesful")
        except:
            print("Test 7 failed")       

    def get_matchesWorks(self):
        reg ='{"email": "popamorena3@gmail.com","password": "kid","conf_password": "kid"}'

        response = requests.post("http://localhost:8000/get_zodiac?token="+token)
        try:
            print(response.status_code)
            self.assertEqual(response.status_code, 200)
            print("Test 8 succesful")
        except:
            print("Test 8 failed")

    def get_matchesFaild(self):
        reg ='{"email": "popamorena3@gmail.com","password": "kid","conf_password": "kid"}'

        response = requests.post("http://localhost:8000/get_zodiac?token=0")
        try:
            print(response.status_code)
            self.assertEqual(response.status_code, 401)
            print("Test 9 succesful")
        except:
            print("Test 9 failed")

    def get_persons_by_sexWorks(self):
        reg ='{"email": "popamorena3@gmail.com","password": "kid","conf_password": "kid"}'

        response = requests.post("http://localhost:8000/get_zodiac?token="+token +"&sex=Female")
        try:
            print(response.status_code)
            self.assertEqual(response.status_code, 200)
            print("Test 10 succesful")
        except:
            print("Test 10 failed")

if __name__ == '__main__':
        reg = RegistrationTest()
        reg.PasswordsNotMatch()
        reg.UserAlreadyInDatabase()
        reg.code_verifFaild()
        reg.get_personsWorks()
        reg.get_personsFaild()
        reg.get_zodiacWorks()
        reg.get_zodiacFaild()
        reg.get_matchesWorks()
        reg.get_matchesFaild()
        reg.get_persons_by_sexWorks()
        