
class Room(object):

    def __init__(self,rm_name,rm_type):
    	self.room_name = rm_name
    	self.rm_type = rm_type

class Office(Room):
    """class for staff"""
    def __init__(self,rm_name):
        super().__init__(rm_name,"office")

class Living_space(Room):
    """class for staff"""
    def __init__(self,rm_name):
        super().__init__(rm_name,"living_space")            
    

    


        
