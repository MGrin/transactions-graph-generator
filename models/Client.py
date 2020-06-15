from mimesis import Person, Address
from random import random
from uuid import uuid4
from .Node import Node

class Client(Node):

	def __init__(self, _id: int):
		self.__type = 'Client'
		self.id = _id
