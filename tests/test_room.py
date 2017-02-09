import unittest
from app.room import Room, Office, LivingSpace

class  TestRoom(unittest.TestCase):
    """test Room class"""

    def test_office_inherits(self):
        """test office class"""

        office = Office("valhalla")
        self.assertIsInstance(office, Room)

    def test_living_space(self):
        """test living space """

        living_space = LivingSpace("haskel")
        self.assertIsInstance(living_space, Room)
         


