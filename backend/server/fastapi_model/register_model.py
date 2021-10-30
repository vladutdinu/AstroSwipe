from pydantic.main import BaseModel


class RegisterModel(BaseModel):
    email : str
    password: str
    conf_password: str
