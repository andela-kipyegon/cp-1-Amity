"""database operations file"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import PersonTbl, RoomTbl, BASE


def save_database(database):
    """fxn that creates database"""

    engine = create_engine('sqlite:///' + database, echo=False)
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    BASE.metadata.create_all(engine)
    return session


def load_database(database):
    """fxn for loading database"""

    engine = create_engine('sqlite:///' + database, echo=False)
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    return session


def load_persons(database):
    """fxn to load people"""

    return load_database(database).query(PersonTbl).all()

def load_rooms(database):
    """fxn to load the rooms"""

    return load_database(database).query(RoomTbl).all()

def insert_person(database, person_info):
    """fxn to save people"""

    db_session = save_database(database)
    db_session.add(person_info)
    db_session.commit()
    db_session.close()

def insert_room(database, room_info):
    """fxn to save people"""

    db_session = save_database(database)
    db_session.add(room_info)
    db_session.commit()
    db_session.close()
