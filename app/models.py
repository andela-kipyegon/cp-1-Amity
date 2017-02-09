""" Models representing the tables in amity"""
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base


BASE = declarative_base()

class PersonTbl(BASE):
    """Class for person"""
    __tablename__ = "person"

    person_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(10), nullable=False)
    job_type = Column(String(10), nullable=False)
    is_accomodated = Column(String(3), default=False)
    allocated_living_space = Column(String(10))
    allocated_office = Column(String(10))

class RoomTbl(BASE):
    """class for room table"""
    __tablename__ = "rooms"

    room_id = Column(Integer, primary_key=True, autoincrement=True)
    room_name = Column(String(20), nullable=False)
    room_type = Column(String(10), nullable=False)
    no_of_occupants = Column(Integer)
