from pydantic.main import BaseModel


class ZodiacModel(BaseModel):
    zodiac_sign : str
