from sqlalchemy import Column, Integer, String
from ..database.db import Base

class Place(Base):
    __tablename__ = 'places'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    address = Column(String)
    photo = Column(String)
