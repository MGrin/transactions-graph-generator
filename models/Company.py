from mimesis import Business, Address
from random import random
from uuid import uuid4
from .Node import Node

class Company(Node):
	_business = Business()
	_address = Address()

	def __init__(self):
		self.__type = 'Company'
		self.id = uuid4()
		self.type = self._business.company_type()
		self.name = self._business.company()
		self.country = self._address.country()
