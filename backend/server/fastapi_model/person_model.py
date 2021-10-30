from pydantic.main import BaseModel
from typing import Optional
import hashlib
class PersonModel(BaseModel):
    unique_id : Optional[str] = None
    email : str
    first_name : str
    last_name : str
    country : str
    city : str
    sex : str
    zodiac_sign : str
    personal_bio : str
    age : int
    user_type: str