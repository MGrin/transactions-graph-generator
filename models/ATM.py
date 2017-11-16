from mimesis import Business, Address
from random import random
from uuid import uuid4
from .Node import Node

class ATM(Node):
	_address = Address()

	def __init__(self):
		self.__type = 'ATM'
		self.id = uuid4()
		self.latitude = self._address.latitude()
		self.longitude = self._address.longitude()
