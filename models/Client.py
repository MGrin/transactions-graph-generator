from mimesis import Person, Address
from random import random
from uuid import uuid4
from .Node import Node

class Client(Node):
	_person = Person()
	_adresss = Address()

	def __init__(self):
		self.__type = 'Client'
		self.id = uuid4()
		self.first_name = self._person.name()
		self.last_name = self._person.surname()
		self.age = self._person.age()
		self.email = self._person.email()
		self.occupation = self._person.occupation()
		self.political_views = self._person.political_views()
		self.nationality = self._person.nationality()
		self.university = self._person.university()

		if random() < 0.15:
			self.academic_degree = self._person.academic_degree()
		else:
			self.academic_degree = None

		self.address = self._adresss.address()
		self.postal_code = self._adresss.postal_code()
		self.country = self._adresss.country()
		self.city = self._adresss.city()
