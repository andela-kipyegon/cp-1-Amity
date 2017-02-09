
class Room(object):

    def __init__(self, rm_name):
        """constructor"""
        self.room_name = rm_name
        self.occupants = 0

class Office(Room):
    """class for staff"""
    def __init__(self, rm_name):
        super().__init__(rm_name)
        self.max_occupants = 6
        self.rm_type = "office"

class LivingSpace(Room):
    """class for staff"""
    def __init__(self, rm_name):
        super().__init__(rm_name)
        self.max_occupants = 4
        self.rm_type = "living_space"
