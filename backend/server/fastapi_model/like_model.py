from pydantic.main import BaseModel


class LikeModel(BaseModel):
    email1 : str
    email2 : str
