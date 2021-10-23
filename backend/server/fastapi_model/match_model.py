from pydantic.main import BaseModel


class MatchModel(BaseModel):
    email1 : str
    email2 : str
