from pydantic import BaseModel, EmailStr
from typing import Optional


class BasePersonSchema(BaseModel):
    name: str
    age: int


class PersonCreateSchema(BasePersonSchema):
    email: EmailStr
    password: str


class PersonUpdateSchema(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class PersonResponseSchema(BasePersonSchema):
    id: int
    email: EmailStr
