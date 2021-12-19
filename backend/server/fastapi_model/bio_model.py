from pydantic.main import BaseModel


class BioModel(BaseModel):
    first_name: str
    last_name: str
    country : str
    city: str
    personal_bio: str
    preffered_zodiac_sign: str
    age: int
    sex: str