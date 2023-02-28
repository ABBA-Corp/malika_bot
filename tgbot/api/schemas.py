from pydantic import BaseModel


class Order(BaseModel):
    name: str
    number: str
    card: str
    time: str
    model: str
    phone: str
    color: str
    type: str
