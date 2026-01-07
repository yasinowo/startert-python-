from sqlalchemy import Column, Integer, String
from database.database import Base


class PersonModel(Base):
    __tablename__ = "persons"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    email = Column(String, unique=True, index=True)
    password = Column(String)
