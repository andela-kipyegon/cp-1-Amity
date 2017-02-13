import random
import os
from termcolor import colored
from app.person import Staff, Fellow
from app.room import Office, LivingSpace
from app.models import PersonTbl, RoomTbl
import app.database

class Amity(object):
    """class that amity to create instance of the program"""


    def __init__(self):
        """constructor for the class amity"""
        self.all_people = []
        self.all_rooms = []
        self.unallocated_office = []
        self.unallocated_living_space = []
        self.file_input = 'storage/file/people.txt'

    def create_room(self, rm_name, rm_type):
        """creates the room which may be instance of office or living space
        params rm_name - name of the room
        params rm_type - type of the Room

        returns success or true msg
        """

        # checks if the room name is null
        if not rm_name or any(char.isdigit() for char in rm_name):
            msg = colored("Enter Valid Room Name", "red")
            return msg

        # checks the room_type
        if rm_type not in ["office", "living_space"]:
            msg = colored("Enter valid room type", "red")
            return msg

        exists = False

        # checks if room exists
        for room in self.all_rooms:
            if rm_name.lower() == room.room_name and not exists:
                exists = True

        # adds the room
        if exists:
            msg = colored("✘ Room already exists", "red")
            return msg
        else:
            if rm_type == "office":
                office = Office(rm_name)
                self.all_rooms.append(office)
                self.auto_allocate("office", rm_name)
                return "Office added successfully"
            else:
                living_space = LivingSpace(rm_name.lower())
                self.all_rooms.append(living_space)
                self.auto_allocate("living_space", rm_name)
                return "Living space added successfully"

    def auto_allocate(self, rm_type, rm_name):
        """fxn to autolocate people if room is created and unallocated people existed

        params rm_name: name of the room created
        params rm-type: type of the room created

        """

        # checks room_type and calls allocate fxn
        if rm_type == "office" and len(self.unallocated_office) > 0:
            occupants = 0
            for person in self.all_people:
                if person.name in self.unallocated_office and occupants < 6:
                    self.unallocated_office.remove(person.name)
                    person.office = rm_name.lower()
                    occupants += 1
            for room in self.all_rooms:
                if rm_name == room.room_name:
                    room.occupants = occupants


        elif len(self.unallocated_living_space) > 0 and len(self.unallocated_living_space):
            occupants = 0
            for person in self.all_people:
                if person.name in self.unallocated_living_space and occupants < 4:
                    self.unallocated_living_space.remove(person.name)
                    person.living_space = rm_name.lower()
                    occupants += 1
            for room in self.all_rooms:
                if rm_name == room.room_name:
                    room.occupants = occupants

    def add_person(self, name, job_type, accomodation="N"):
        """fxn to add person to amity program

        param name: Takes the name of the person
        param job_type: Takes the job_type of the person
        param accomodation: cheks whether wants accomodation

        returns success or error msg
        """

        # checks if name is null
        if not name or any(char.isdigit() for char in name):
            msg = colored("✘ Enter a valid name", "red", attrs=["bold"])
            return msg

        # checks job type
        if job_type.lower() not in ["fellow", "staff"]:
            msg = colored("✘ Enter a valid job type", "red", attrs=["bold"])
            return  msg

        # checks if person exists
        exists = False
        for i in range(0, len(self.all_people)):
            if  name.lower() == self.all_people[i].name and not exists:
                exists = True

        # allocates room to person
        if exists:
            msg = colored("✘ Person already exists", "red", attrs=["bold"])
            return msg
        else:
            if job_type.lower() == "fellow":
                fellow = Fellow(name.lower(), accomodation)
                self.all_people.append(fellow)
                msg = "✔ "
                return msg + self.allocate(name, job_type, accomodation)
            else:
                staff = Staff(name.lower())
                self.all_people.append(staff)
                msg = "✔ "
                return msg + self.allocate(name, job_type)

    def search_room_availability(self, accomodation):
        """fxn to search room

        param accomodation: takes accomodation either office or living_space

        returns a list of available spaces
        """

        # checks room availabilty
        if accomodation == "office":
            office_with_spaces = []

            for space in self.all_rooms:
                try:
                    occupants = int(space.occupants)
                except ValueError:
                    occupants = 0
                if  occupants < 6 and space.rm_type == "office":
                    office_with_spaces.append(space.room_name)
            return office_with_spaces

        elif accomodation == "living_space":
            living_with_spaces = []

            for space in self.all_rooms:
                try:
                    occupants = int(space.occupants)
                except ValueError:
                    occupants = 0
                if  occupants < 4 and space.rm_type == "living_space":
                    living_with_spaces.append(space.room_name)
            return living_with_spaces

    def allocate(self, name, job_type, accomodation="N"):
        """fxn to allocate new person automatically called by add_person fxn

        param name: name of the person to be allocated a room
        param job_type: occupation of the person to be allocated
        param accomodation: checks on wants accoomodation

        returns relevant msg depending if fellow or staff

        """

        # allocation fellow and staff
        if job_type.lower() == "staff" or (job_type.lower() == "fellow" and accomodation == "N"):

        # allocate staff to office
            try:
                selected_office = random.choice(self.search_room_availability("office"))
                for office in self.all_rooms:
                    if office.room_name == selected_office:
                        office.occupants += 1
                self.all_people[-1].office = selected_office
                msg = "{} created successfully and allocated office"
                return msg.format(self.all_people[-1].job_type)
            except IndexError:
                self.unallocated_office.append(name.lower())
                msg = "Created {} successfully but no office is available"
                return msg.format(self.all_people[-1].job_type)
        else:

            try:
                selected_office = random.choice(self.search_room_availability("office"))
                for office in self.all_rooms:
                    if office.room_name == selected_office:
                        office.occupants += 1

                try:
                    selected_living_space = random.choice(
                        self.search_room_availability("living_space"))
                    for living_space in self.all_rooms:
                        if living_space.room_name == selected_living_space:
                            living_space.occupants += 1
                    self.all_people[-1].living_space = selected_living_space
                    self.all_people[-1].office = selected_office
                    return "Fellow created successfully and allocated office and living space"
                except IndexError:
                    self.all_people[-1].office = selected_office
                    self.unallocated_living_space.append(name.lower())
                    return "Fellow created successfully and allocated office only"

            except IndexError:
                try:
                    selected_living_space = random.choice(\
                        self.search_room_availability("living_space"))
                    for living_space in self.all_rooms:
                        if living_space.room_name == selected_living_space:
                            living_space.occupants += 1
                    self.all_people[-1].living_space = selected_living_space
                    self.unallocated_office.append(name.lower())
                    return "Fellow created successfully and allocated living space only"
                except IndexError:
                    self.unallocated_office.append(name.lower())
                    self.unallocated_living_space.append(name.lower())
                    return "fellow created Successfully and no Living_space and Office available "

    def reallocate(self, name, rm_name):
        """fxn to reallocate person" to another Room

        param name: name of the person to be reallocated
        param rm_name: name of the room the person should be reallocated to

        returns success or error message

        """

        for person in self.all_people:

            #checks if person exists
            if person.name == name.lower():
                # checks if room is available

                for room in self.all_rooms:
                    if room.room_name == rm_name.lower():
                        room_type = room.rm_type
                        room_index = self.all_rooms.index(room)
                        old_room = getattr(person, room_type)

                        if  old_room == rm_name:
                            msg = "✘ Person is already in room "
                            msg = colored(msg, "red", attrs=["bold"])
                            return msg
                        elif person.job_type == "fellow" and person.accomodation == "N":
                            msg ="✘ Fellow does not want living space"
                            msg = colored(msg, "red", attrs=["bold"])
                            return msg     
                        elif person.job_type == "staff" and room_type == "living_space":
                            msg = " ✘ Cannot allocate staff living space"
                            msg = colored(msg, "red", attrs=["bold"])
                            return msg
                        elif room.occupants >= 6 and room.rm_type == "office":
                            msg = "✘ Office is already full"
                            msg = colored(msg, "red", attrs=["bold"])
                            return msg
                        elif room.occupants >= 4 and room.rm_type == "living_space":
                            msg ="✘ Living space is already full"
                            msg = colored(msg, "red", attrs=["bold"])
                            return msg
                        else:

                            #increase occupant in new rooms
                            self.all_rooms[room_index].occupants += 1
                            setattr(person, room_type, rm_name)

                            # reduce occupants in old room
                            for room in self.all_rooms:
                                if old_room == room.room_name:
                                    room.occupants -= 1
                            msg = "✔ Person has been reallocated to " + rm_name.lower()
                            msg = colored(msg, "green", attrs=["bold"])
                            return msg
                
                msg = "✘  Room does not exist"
                msg = colored(msg, "red", attrs=["bold"])
                return msg
        msg = "✘  Person does not exist"
        msg = colored(msg, "red", attrs=["bold"])        
        return msg


    def load_people(self):
        """fxn to load people from people.txt in storage file
        
        returns success or error msg
        """

        # open people.txt
        try:
            with open(os.path.expanduser(self.file_input)) as people_file:
                people = people_file.readlines()

                # message
                count = 0

                # checks file contents
                if len(people) == 0:
                    return "The file has no contents"
                else:
                    for line in people:
                        line = line.replace('\n', '')
                        person = line.split(' ')
                        if len(person) == 4 and person[2].lower() == "fellow":
                            accomodation = 'N'
                            name = person[0] + "_" + person[1]
                            job_type = person[2]
                            accomodation = person[3]
                            msg = self.add_person(name, job_type, accomodation)
                            if msg != colored("✘ Person already exists", "red", attrs=["bold"]):
                                count += 1
                        elif len(person) == 3 and person[2].lower() in ["staff", "fellow"]:
                            accomodation = 'Y'
                            name = person[0] + "_" + person[1]
                            job_type = person[2]
                            msg = self.add_person(name, job_type, accomodation)
                            if msg != colored("✘ Person already exists", "red", attrs=["bold"]):
                                count += 1
                        elif count != 0:
                            msg = "line  {} hasFile has Wrong Format".format(count+1)
                            msg = colored(msg, "red", attrs=["bold"])

                    msg = "✔ " + str(count) + " people added"
                    msg = colored(msg, "green", attrs=["bold"])        
                    return msg
        except:
            msg = "✘ Error in fetching file"
            msg = colored(msg, "red", attrs=["bold"])
            return msg

    def print_allocations(self, filename=None):
        """fxn that prints unallocated

        params filename: optional if one wants to save allocations to txt file

        """
        if len(self.all_rooms) != 0:
            allocations = []

            # get list from all people
            for room in self.all_rooms:
                occupants = []
                allocations.append({room.room_name:occupants})
                for person in self.all_people:
                    if person.office == room.room_name:
                        occupants.append(person.name)
                    if person.living_space == room.room_name:
                        occupants.append(person.name)
                    allocations[-1][room.room_name] = occupants

            # output
            output = "ROOM ALLOCATIONS"
            # printing or display on screen
            for room in allocations:
                output += "\n\n" + ("_" * 90)
                for name, people in room.items():
                    output += "\n" + name.upper() + "\n" + ("_" * 90) + "\n\n"
                    for person in people:
                        person = person.upper()
                        name = person.split('_')
                        if people.index(person.lower()) != len(people)-1:
                            output += name[0] + " " + name[1] + ","
                        else:
                            output += name[0] + " " + name[1]

            return self.output(output, filename)
        return self.output("NO ROOMS")

    def print_unallocated(self, filename=None):
        """fxn to print unallocated person
        
         params filename: optional if one wants to save unallocated to txt file
        """

        output = ""
        # unallocated office
        output += "\t\t" + ("_"*30) + "\n"
        output += "\t\t" + "UNALLOCATED OFFICE" + "\n" + "\t\t" + ("_" * 30) + "\n\n"
        for person in self.unallocated_office:
            person = person.split('_')
            output += "\t\t" + person[0] + " " + person[1] + "\n"

        # unallocated living space
        output += "\t\t" + ("_"*30) + "\n"
        output += "\t\t" + "UNALLOCATED LIVING SPACE" + "\n" + "\t\t" + ("_" * 30) + "\n\n"
        for person in self.unallocated_living_space:
            person = person.split('_')
            output += "\t\t" + person[0] + " " + person[1] + "\n"

        return self.output(output, filename)

    def output(self, output, filename=None):
        """fxn for display or print to screen
         
         param ouput: has the contented to be displayed or printed
         params filename: optional if one wants to save contents to txt file 

        """

        # print or display
        if filename:
            filepath = os.path.expanduser("~/Desktop/Amity/storage/file/" + filename + ".txt")
            files = open(filepath, "w")
            files.write(output)
            files.close()
            return " ✓ File allocations in storage/file "
        else:
            return output

    def print_room(self, rm_name):
        """fxn to print room members

        param rm_name: takes which room is to be printed
        
        """

        output = ""
        # checks all people
        for room in self.all_rooms:
            if room.room_name == rm_name.lower():
                room_type = room.rm_type
                output += "\t\t" + ("_" * 30) + "\n\n" + "\t\t"
                output += room.room_name.upper()
                output += " MEMBERS" + "\n" + "\t\t" + ("_" * 30) + "\n\n"
                for person in self.all_people:
                    if rm_name == getattr(person, room_type):
                        name = person.name.upper()
                        name = name.split('_')
                        output += "\t\t" + name[0] + " " + name[1] + "\n"
                return self.output(output)

        msg = colored(" ✘ Room does not exist", "red",attrs=["bold"])
        return msg

    def load_state(self, dbase):
        """fxn to load state
        
        params dbase: takes the name of the database to be loaded

        returns success msg or error msgs
        """

        # locate db file
        dbase = dbase + ".db"

        if os.path.exists("storage/database/" + dbase):
            try:
                people = app.database.load_persons(dbase)
                rooms = app.database.load_rooms(dbase)

                # clear data structures
                self.all_people = []
                self.all_rooms = []
                self.unallocated_office = []
                self.unallocated_living_space = []

                # populate all people
                for person in people:
                    if person.job_type.lower() == "staff":
                        staff = Staff(person.name)
                        staff.living_space = person.allocated_living_space
                        staff.job_type = person.job_type
                        staff.office = person.allocated_office
                        self.all_people.append(staff)
                    else:
                        fellow = Fellow(person.name, person.is_accomodated)
                        fellow.living_space = person.allocated_living_space
                        fellow.job_type = person.job_type
                        fellow.office = person.allocated_office
                        self.all_people.append(fellow)
                    
                    # populate unallocated    
                    if person.allocated_office is None:
                        self.unallocated_office.append(person.name)
                    if person.allocated_living_space is None and person.is_accomodated == "Y":
                        self.unallocated_living_space.append(person.name)    

                # populate all rooms
                for room in rooms:
                    if room.room_type == "office":
                        office = Office(room.room_name)
                        office.occupants = room.no_of_occupants
                        self.all_rooms.append(office)
                    else:
                        living_space = LivingSpace(room.room_name)
                        living_space.occupants = room.no_of_occupants
                        self.all_rooms.append(living_space)
               
                msg = "✔ Loaded Successfully"
                msg = colored(msg, "green", attrs=["bold"])
                return msg

            except:
                msg = "✘ Error in loading contents"
                msg = colored(msg, "red", attrs=["bold"])
                return msg
        else:
            msg = "✘ Database not found"
            msg = colored(msg, "red", attrs=["bold"])
            return msg

    def save_state(self, dbase="amity"):
        """fxn to save state
        
        params dbase: database name of the db to be stored

        return success or error msg
        """

        dbase = dbase + ".db"

        # delete if path exist
        if os.path.exists("storage/database/"+dbase):
            os.remove("storage/database/"+dbase)

        try:
            # commit rooms
            for room in self.all_rooms:
                info = RoomTbl(room_name=room.room_name,
                               room_type=room.rm_type, no_of_occupants=room.occupants)
                app.database.insert_room(dbase, info)

            # commit people
            for person in self.all_people:
                info = PersonTbl(name=person.name,
                                 job_type=person.job_type, is_accomodated=person.accomodation,
                                 allocated_office=person.office,
                                 allocated_living_space=person.living_space)
                app.database.insert_room(dbase, info)
            msg = "✔ Save state is succesful"
            msg = colored(msg, "green", attrs=["bold"])
            return msg
        except:
            msg = "✘ Error in saving database"
            msg = colored(msg, "green", attrs=["bold"])
            return msg
