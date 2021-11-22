from pydantic.main import BaseModel


class BioModel(BaseModel):
    country : str
    city: str
    personal_bio: str
    preffered_zodiac_sign: str
    pref_age1: int
    pref_age2: int
