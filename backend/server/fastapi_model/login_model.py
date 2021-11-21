from pydantic.main import BaseModel


class LoginModel(BaseModel):
    email : str
    password: str
