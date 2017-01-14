from sqlalchemy import Column,Integer,String,create_engine,Boolean,DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Person(Base):
	__tablename__ = "person"

	person_id = Column(Integer,primary_key=True)
	name = Column(String(10),nullable = False)
	job_type = Column(String(10), nullable = False)
	is_accomodated = Column(Boolean,default=False)
	allocated_room = Column(String(10))
	allocated_office  = Column(String(10))

	def __init__(self,person_id,name,job_type,is_accomodated,room,office):

		self.person_id = person_id
		self.name = name
		self.job_type = job_type
		self.is_accomodated = is_accomodated
		self.allocated_room = room
		self.allocated_office = office

class Room(Base):
	__tablename__ = "rooms"

	room_id = Column(Integer,primary_key = True)
	room_name = Column(String(20),nullable = False)
	room_type = Column(String(10),nullable = False)
	no_of_occupants = Column(Integer)

	def __init__(self,name,r_type,no_occupants):
		self.room_name = name
		self.room_type = r_type
		self.no_of_occupants = no_occupants

def create_database(database):
    engine = create_engine("sqlite:///C:/Amity/app/"+"Dojo"+".db" ,echo = False)
    Base.metadata.create_all(engine)





