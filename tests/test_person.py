import unittest
from app.person import Person, Fellow, Staff

class  TestPerson(unittest.TestCase):
    """test Room class"""

    def test_fellow_inherits_person(self):
        """test office class"""

        fellow = Fellow("ken", "N")
        self.assertIsInstance(fellow, Person)

    def test_staff_inherits_person(self):
        """test living space """

        staff = Staff("jackson")
        self.assertIsInstance(staff, Person)
         