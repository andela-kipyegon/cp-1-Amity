from app.person import Person,Staff,Fellow
from app.room import Room,Office,Living_space
import random

class Amity(object):
	"""class that amity to create instance of the program"""

	def __init__(self):
		"""constructor for the class amity"""
		self.no_of_people = []
		self.no_of_rooms = []
		self.all_people = []
		self.all_rooms = []
		self.unallocated_office = []
		self.unallocated_living_space = []
		self.office_with_spaces = []
		self.living_with_spaces = []
		self.file_input = 'C:\Amity\storage\/file\people.txt'

	def create_room(self,rm_name,rm_type):
		"""creates the room """

		#checks if the room name is null
		if rm_name == "":
			return "Enter Valid Room Name"
		exists = False

		#checks if room exists
		for room in self.all_rooms:
			if rm_name == room["room"] and not exists:
				exists = True

		#adds the room
		if exists:
			return "Room Already Exists"
		else:
			if rm_type == "office":
			   office = Office(rm_name)
			   new_room = {"room":office.room_name,"occupants":0,"type":"office"}
			   self.all_rooms.append(new_room)
			   return "Office Added Successfully"
			else:
			   living_space = Living_space(rm_name)
			   new_room = {"room":living_space.room_name,"occupants":0,"type":"living_space"}
			   self.all_rooms.append(new_room)
			   return "Living Space Added Successfully"


	def add_person(self,name,job_type,accomodation = "N" ):
		"""fxn to add person"""

		#checks if name is null
		if name == "":
			return "Enter a valid name"

		#checks job type
		if job_type.lower() not in ["fellow","staff"]:
			return "Enter valid a job type "

		#checks person
		exists = False
		for i in range(0,len(self.all_people)):
			if  name.lower() == self.all_people[i]["name"] and not exists:
				exists = True

		#allocates room to person
		if exists :
			return "Person already exists"
		else:
			if job_type.lower() == "fellow":
			   fellow = Fellow(name,job_type,accomodation)
			   new_fellow = {"name":fellow.name,"job_type":fellow.job_type.lower(),"accomodation":fellow.accomodation.upper()}
			   self.all_people.append(new_fellow)
			   return self.allocate(name,job_type,accomodation)
			else:
			   staff = Staff(name,job_type)
			   new_staff = {"name":staff.name,"job_type":staff.job_type.lower(),"accomodation":None}
			   self.all_people.append(new_staff)
			   return self.allocate(name,job_type,accomodation)

	def allocate(self,name,job_type,accomodation):
		"""fxn to allocate new person"""

		#checks room availabilty
		if len(self.office_with_spaces) == 0:
			for spaces in self.all_rooms:
				if spaces["occupants"] < 6 and spaces["type"] == "office":
					self.office_with_spaces.append(spaces["room"])

		# allocation fellow and staff
		if job_type.lower() == "staff":

			# allocate staff to 																																																																								`````````````````````````````````````````````````````````````````````````````````````````````````````````````````		query																																																																																											\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\				`						``				1W																																																																																																																																																				`````````````````
			try:
				self.selected_office = random.choice(self.office_with_spaces)
				for office in self.all_rooms:
					if office["room"] == self.selected_office:
						office["occupants"] += 1
						br
				self.all_people[-1].update({"office":self.selected_office,"living_space":None})
				return "Staff allocated Office"
			except:
				self.all_people[-1].update({"office":None,"living_space":None})
				self.unallocated_office.append(name)
				return "No Rooms are available"

		elif job_type.lower() == "fellow" and accomodation == "N" :
			try:
				self.selected_office = random.choice(self.office_with_spaces)
				for office in self.all_rooms:
					if office["room"] == self.selected_office:
						office["occupants"] += 1
				self.all_people[-1].update({"office":self.selected_office,"living_space":None})
				return "Fellow allocated Room"
			except:
				self.all_people[-1].update({"office":None,"living_space":None})
				self.unallocated_office.append(name)
				return "No Office available"

		else:
			if len(self.living_with_spaces) == 0:
				for spaces in self.all_rooms:
					if spaces["occupants"] < 4 and spaces["type"] == "living_space":
						self.living_with_spaces.append(spaces["room"])

			try:
				selected_office = random.choice(self.office_with_spaces)
				for office in self.all_rooms:
					if office["room"] == selected_office:
						office["occupants"] += 1

				try:
					selected_living_space = random.choice(self.living_with_spaces)
					for living_space in self.all_rooms:
						if living_space["room"] == selected_living_space:
							living_space["occupants"] += 1
					self.all_people[-1].update({"office":selected_office,"living_space":selected_living_space})
					return "Allocated Office and Room "
				except:
					self.unallocated_living_space.append(name)
					return"Allocated office only"

			except:
				try:
					selected_living_space = random.choice(self.living_with_spaces)
					for living_space in self.all_rooms:
						if living_space["room"] == selected_living_space:
							living_space["occupants"] += 1
					self.all_people[-1].update({"office":None,"living_space":selected_living_space})
					self.living_with_spaces.remove(selected_living_space)
					return "Fellow allocated Room only"
				except :
					self.all_people[-1].update({"office":None,"living_space":None})
					self.unallocated_office.append(name)
					self.unallocated_living_space.append(name)
					return "No Room and Office available "+str(e)

	def reallocate(self,name,rm_name):
		"""fxn to reallocate person"""

		# variables for argument validation
		room_exists = False
		person_exists = False

		# checks if room is available
		for room in self.all_rooms:
			if room["room"] == rm_name and not room_exists:
				room_index = self.all_rooms.index(room)
				room_exists = True
				room_type = room["type"]
				if room["occupants"] >= 6 and room["type"] == "office":
					return "Office is already full"
				elif room["occupants"] >= 4 and room["type"] == "living_space":
					return "Living Space is already full"


		# allocation if room exists
		if room_exists:
			for person in self.all_people:

				#checks if person exists
				if person["name"] == name.lower():
					person_exists = True
					old_room = person[room_type]

					# no staff alllocation to room
					if old_room == rm_name:
						return "Person is already in room "
					elif person["job_type"] == "staff" and room_type == "living_space":
						return "Cannot Allocate Staff living space"
					else:

						#increase occupant in new rooms
						self.all_rooms[room_index]["occupants"] += 1
						person[room_type] = rm_name

						# reduce occupants in old room
						for room in self.all_rooms:
							if old_room  ==  room["room"]:
								 room["occupants"] -= 1

						return "Person has been reallocated"

			return "Person does not exist"
		else:
			return "Room does not exist"

	def load_people(self):

		try:
			with open(self.file_input) as people_file:
				people = people_file.readlines()

				if len(people) == 0:
					return "The file has no contents"
				else:
					for line in people:
						line = line.replace('\n','')
						person = line.split(' ')
						if len(person) < 4:
							accomodation = 'N'
							name = person[0] + " " + person[1]
							job_type = person[2]
							self.add_person(name, job_type, accomodation)
						else:
							accomodation = 'Y'
							name = person[0] + " " + person[1]
							job_type = person[2]
							self.add_person(name, job_type,accomodation)
					return "file loaded successfully"
		except:
			return "Error in fetching file"

	def print_allocations(self):
		allocations = []

		for room in self.all_rooms:
			occupants = []
			allocations.append({room["room"]:occupants})
			for person in self.all_people:
				if person['office'] == room["room"]:
					occupants.append(person["name"])
				if person['living_space'] == room["room"]:
					occupants.append(room["room"])
				allocations[-1][room["room"]] = occupants

		return allocations

	def load_state(self,database):
		if os.path.exists(database):
			try:
				self.load_contents(database)
			except Exception as Error:
				return "Error in loading contents"
				print (error)
		else:
			return "Database not found"


	def save_state(self):
		if os.path.exists(database):
			return "Database Name Already exists Choose a name and try again"
		else:
			try:
				model.create_database(database)
				self.save_contents(database)
			except Exception as Error:
				print (error)

	def load_contents(self,database):
		engine = create_engine('sqlite:///' + database)
		engine.echo = False
		Session = sessionmaker()
		Session.configure(bind=engine)
		session = Session()

		self.rooms = session.query(Room).all()
		self.rooms_with_spaces = []

	def save_contents(self,database):
		pass

amity = Amity()
print (amity.add_person("olive","fellow","N"))
print (amity.add_person("olive","fellow","Y"))
print (amity.add_person("maggy","fellow","Y"))
#print (amity.add_person("brian","fellow","Y"))
print (amity.reallocate("oliver","oculus2"))
print (amity.all_rooms)
