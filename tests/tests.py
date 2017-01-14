from app.amity import Amity
import unittest

class AddPersonTest(unittest.TestCase):

    def setup(self):
        self.amity = Amity()
        self.create_room("valhalla","office")
        self.create_room("php","living_space")

    def test_add_person(self):
        """fxn test add persons"""

        self.setup()
        self.assertEqual(len(self.amity.all_people),2,msg = "Two People should be added")

    def test_add_staff(self):
        """fxn test add staff"""

        self.setup()
        self.amity.add_person("oliver","Staff")
        staff = [staff for staff in self.amity.all_people if staff["job_type"] == "staff" ]
        self.assertEqual(len(staff),1)

    def test_add_fellow(self):
        """fxn test add staff"""

        self.setup()
        self.amity.add_person("hms","Fellow")
        fellow = [fellow for fellow in self.amity.all_people if fellow["job_type"] == "fellow" ]
        self.assertEqual(len(fellow),1)

    def test_check_job_type(self):
        """fxn to check job type argument"""

        self.setup()
