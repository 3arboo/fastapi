from typing import Optional
from pydantic import BaseModel
class Clientmodel(BaseModel):
    id:int
    client_name: str
    post_url: str
    price: float
    days_name: int
    is_finished: bool

