
"""class for Fellow and Satff instances"""
class Person(object):
    """super class person"""
    def __init__(self, name):
        self.name = name
        self.living_space = None
        self.office = None

class Staff(Person):
    """class for staff"""
    def __init__(self, name):
        super().__init__(name)
        self.job_type = "staff"
        self.accomodation = "N"

class Fellow(Person):
    """ class for fellows"""
    def __init__(self, name, accomodation):
        super().__init__(name)
        self.job_type = "fellow"
        self.accomodation = accomodation
