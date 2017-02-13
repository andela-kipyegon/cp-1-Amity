import unittest, os
from app.amity import Amity
from termcolor import colored


class AddPersonTest(unittest.TestCase):
    """class to test fxn  add_person"""

    def setUp(self):
        """insatciates the class amity"""
        self.amity = Amity()


    def test_add_person(self):
        """fxn test add persons"""

        self.amity.add_person("oliver", "Staff")
        self.amity.add_person("hms", "Fellow")
        self.assertEqual(len(self.amity.all_people), 2, msg="Two People should be added")

    def test_add_staff(self):
        """fxn test add staff"""

        self.amity.add_person("oliver", "Staff")
        staff = [staff.name for staff in self.amity.all_people if staff.job_type == "staff"]
        self.assertIn("oliver", staff)
        self.assertEqual(len(staff), 1, msg="person not saved as staff")

    def test_add_fellow(self):
        """fxn test add staff"""

        self.amity.add_person("hms", "Fellow")
        fellow = [fellow.name for fellow in self.amity.all_people if fellow.job_type == "fellow"]
        self.assertIn("hms", fellow)
        self.assertEqual(len(fellow), 1, msg="person not saved as fellow")

    def test_argument_validation(self):
        """fxn to check job type argument"""

        self.amity.add_person("oliver", "sta")
        self.assertEqual(self.amity.add_person("oliver", "sta"),\
                         colored("✘ Enter a valid job type", "red",\
                                 attrs=["bold"]), msg="incorrect job type argument")
        self.assertEqual(self.amity.add_person("", "staff"),\
                         colored("✘ Enter a valid name", "red", attrs=["bold"]),\
                         msg="incorrect name argument")

    def test_person_exist(self):
        """fxn to check if person exists"""

        # create person and romm
        self.amity.create_room("shire", "office")
        self.amity.add_person("jackson", "staff")
        self.amity.add_person("oliver", "fellow", "N")

        # test if person already exist
        self.assertEqual(self.amity.add_person("jackson", "staff"),
                         colored("✘ Person already exists", "red", attrs=["bold"]))

class TestReallocation(unittest.TestCase):
    """class for test reallocation """

    def setUp(self):
        """fxn setUp"""

        self.amity = Amity()
        self.amity.create_room("PHP", "living_space")
        self.amity.create_room("valhalla", "office")
        self.amity.add_person("jackson", "staff")
        self.amity.add_person("gideon", "fellow", "Y")


    def test_non_existant_person(self):
        """test if one is in the system"""

        non_exist_person = self.amity.reallocate("ken", "PHP")
        self.assertEqual(non_exist_person, colored("✘  Person does not exist",\
          "red", attrs=["bold"]))

    def test_non_existant_room(self):
        """fxn to test reallocation of non existant room"""

        non_existant_room = self.amity.reallocate("jackson", "midgar")
        self.assertEqual(non_existant_room, colored("✘  Room does not exist", "red",\
                                 attrs=["bold"]))

    def test_full_room(self):
        """fxn to test reallocation in full rooms"""

        # add living space to capacity
        self.amity.add_person("oliver", "fellow", "Y")
        self.amity.add_person("ian", "fellow", "Y")
        self.amity.add_person("hms", "fellow", "Y")
        self.amity.add_person("batian", "staff")
        self.amity.add_person("olive", "staff")
        self.amity.add_person("cheru", "staaff")
        self.amity.add_person("carol", "fellow", "Y")

        #check reallocation to PHP and valhalla
        self.assertEqual(self.amity.reallocate("carol", "PHP"),\
              colored("✘ Living space is already full", "red", attrs=["bold"]))
        self.assertEqual(self.amity.reallocate("carol", "valhalla"),
              colored("✘ Office is already full", "red", attrs=["bold"]))

    def test_person_exist_scenarios(self):
        """fxn to test all person scenarios if the person exists"""

        # add new room
        self.amity.create_room("shire", "office")

        # allocate to living space
        staff_allocation = self.amity.reallocate("jackson", "PHP")
        self.assertEqual(staff_allocation, colored(" ✘ Cannot allocate staff living space", "red", attrs=["bold"]))

        # allocate to same room
        already_allocated = self.amity.reallocate("jackson", "valhalla")
        self.assertEqual(already_allocated, colored("✘ Person is already in room ", "red", attrs=["bold"]))

        # reallocate succesfully
        allocate = self.amity.reallocate("gideon", "Shire")
        self.assertEqual(allocate, colored("✔ Person has been reallocated to shire", "green", attrs=["bold"]))

class TestAllocation(unittest.TestCase):
    """class for testing fxn allocation"""

    def setUp(self):
        """instaciates the class amity"""

        self.amity = Amity()

    def test_allocation_persons(self):
        """fxn to test allocation"""

        # add room and person
        self.amity.create_room("shire", "office")
        self.amity.create_room("narnia", "living_space")
        self.amity.add_person("alex", "staff")
        self.amity.add_person("jackson", "fellow", "Y")
        self.amity.add_person("migwi", "fellow", "N")

        # check if staff assigned proper office and living space
        occupants_shire = [room.occupants
                           for room in self.amity.all_rooms if room.room_name == "shire"]
        living_space = [person.name
                        for person in self.amity.all_people if person.living_space is not None]

        self.assertIn(3, occupants_shire, msg="Should be three people")
        self.assertListEqual(living_space, ["jackson"], msg="Should be one person")
        self.assertEqual(self.amity.add_person("kanyi", "staff"),
                         "✔ staff created successfully and allocated office",
                         msg="staff should be allocated office")
        self.assertEqual(self.amity.add_person("gideon", "fellow", "Y"),
                         "✔ Fellow created successfully and allocated office and living space",
                         msg="fellow should be allocated office and living space")
        self.assertEqual(self.amity.add_person("brian", "fellow"),
                         "✔ fellow created successfully and allocated office",
                         msg="fellow should be allocated office and living space")
    
    def test_allocates_living_space_only(self):
        """test allocations if room exist only"""
        self.amity.create_room("narnia", "living_space")
        self.assertEqual(self.amity.add_person("brian", "fellow","Y"),
                         "✔ Fellow created successfully and allocated living space only")

    def test_allocates_office_only(self):
        """test allocations if office exist only"""
        self.amity.create_room("shire", "office")
        self.assertEqual(self.amity.add_person("brian", "fellow","Y"),
                         "✔ Fellow created successfully and allocated office only")

    def test_no_room(self):
        """fxn situation of no rooms scenarios"""

        # add staff and fellow and see if allocated
        self.assertEqual(self.amity.add_person("gibert", "fellow"), "✔ Created fellow successfully but no office is available")
        self.assertEqual(self.amity.add_person("ken", "staff"), "✔ Created staff successfully but no office is available")



class TestCreateRoom(unittest.TestCase):
    """class to fxn create room """

    def setUp(self):
        """instanciates amity program"""
        self.amity = Amity()
        self.amity.create_room("shire", "office")

    def test_argument(self):
        """fxn to test argument to create room fxn"""

        # checks office argument
        office = ""
        room_type = "office"
        self.assertEqual(self.amity.create_room(office, room_type), colored("Enter Valid Room Name", "red"))

        # checks room_type argument
        living_space = "haskel"
        room_type = "living_spac"
        self.assertEqual(self.amity.create_room(living_space, room_type), colored("Enter valid room type", "red"))

    def test_autoallocates(self):
        """test no of occupants of room shire is 6"""
        self.amity.add_person("oliver", "fellow", "Y")
        self.amity.add_person("ian", "fellow", "Y")
        self.amity.add_person("hms", "fellow", "Y")
        self.amity.add_person("batian", "staff")
        self.amity.add_person("olive", "staff")
        self.amity.add_person("cheru", "staff")
        self.assertEqual(self.amity.all_rooms[0].occupants, 6)

    def test_room_exists(self):
        """fxn to test if room exists"""

        room_exists = self.amity.create_room("shire", "office")
        self.assertEqual(room_exists, colored("✘ Room already exists", "red"))

    def test_room_added(self):
        """fxn to check add successfully"""

        # add office
        office = self.amity.create_room("narnia", "office")
        self.assertEqual(office, "Office added successfully")

        # add living space
        living_space = self.amity.create_room("java", "living_space")
        self.assertEqual(living_space, "Living space added successfully")

class TestLoadPeople(unittest.TestCase):
    """class for testing fxn add people"""

    def setUp(self):
        """instanciates amity"""

        self.amity = Amity()

    def test_load_people(self):
        """test it loads successfully"""

        # create two people
        output = ""
        output += "KENNETH KIPYEGON FELLOW Y\n"
        output += "NELSON MWAITA STAFF\n"

        # write to file
        files = open("/Users/Kipyegon/Desktop/Amity/storage/file/people.txt", "w")
        files.write(output)
        files.close()

        # test load people
        self.assertEqual(self.amity.load_people(), colored("✔ 2 people added", "green", attrs=["bold"]))
        os.remove("/Users/Kipyegon/Desktop/Amity/storage/file/people.txt")

    def test_file_fomart(self):
        """test it loads successfully"""

        # create two people
        output = ""
        output += "KENNETH KIPYEGONFELLOW Y\n"
        output += "NELSON MWAITA STAFF\n"

        # write to file
        files = open("/Users/Kipyegon/Desktop/Amity/storage/file/people.txt", "w")
        files.write(output)
        files.close()

        # test load people
        self.assertEqual(self.amity.load_people(), colored("✔ 1 people added", "green", attrs=["bold"]))
        os.remove("/Users/Kipyegon/Desktop/Amity/storage/file/people.txt")

    def test_file_no_contents(self):
        """test it has no contents"""

        # write to file
        files = open("/Users/Kipyegon/Desktop/Amity/storage/file/people.txt", "w")
        files.write("")
        files.close()

        # test empty contents
        self.assertEqual(self.amity.load_people(), "The file has no contents")
        os.remove("/Users/Kipyegon/Desktop/Amity/storage/file/people.txt")


    def test_error_in_contents(self):
        """test it has no contents"""

        # test empty contents
        if os.path.exists("storage/file/people.txt"):
            os.remove("storage/file/people.txt")

        self.assertEqual(self.amity.load_people(), colored("✘ Error in fetching file", "red", attrs=["bold"]))

class TestPrintRoom(unittest.TestCase):
    """class to test fxn print room"""

    def setUp(self):
        """instanciates amity"""

        self.amity = Amity()

    def test_print_room(self):
        """prints room"""

        self.assertEqual(self.amity.print_room("shire"), colored(" ✘ Room does not exist", "red", attrs=["bold"]))

class TestState(unittest.TestCase):
    """"checks whether the load test and save test are working"""

    def setUp(self):
        """instaciates the amity program"""
        self.amity = Amity()

    def load_non_existant_db(self):
        self.amity.load_state("1234")
        self.assertEqual(self.amity.load_people(), colored("✘ Database not found", "red", attrs=["bold"]))
    
    def test_contents(self):
        """test fxn to load people"""

        # create room and person
        self.amity.create_room("mordor", "living_space")
        self.amity.add_person("kenneth_kipyegon", "staff")
        self.amity.save_state("test")


        # load database
        self.amity.load_state("test")
        # assert content
        print(len(self.amity.all_people))
        self.assertEqual(1, len(self.amity.all_people))
        self.assertEqual(1, len(self.amity.all_rooms))
        
        self.assertEqual(self.amity.all_rooms[0].room_name, "mordor")
        self.assertEqual(self.amity.all_people[0].name, "kenneth_kipyegon")


if __name__ == '__main__':
    unittest.main()
