import sys
import os
import random

class Person(object):

	selected_office = ""

	def __init__(self,name,job_type):
		self.name = name
		self.job_type = job_type

				          
class Fellow(Person):
	""" class for fellows"""

	def __init__(self,name,job_type,accomodation):
		super().__init__(name,job_type)
		self.accomodation = accomodation

class Staff(Person):
	"""class for staff"""

	def __init__(self,name,job_type):
		super().__init__(name,job_type)
		self.accomodation = "N"
