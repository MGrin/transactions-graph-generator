from mimesis import Person, Address, Numeric
from random import random, choice
from uuid import uuid4
from .Node import Node

# Person.age() and Person.political_views() were dropped by mimesis in 6.0.0.
# Both are reproduced here so the generator keeps working on every mimesis >= 5.0:
# the age bounds and the value set are the ones mimesis itself used.
POLITICAL_VIEWS = ['Anarchism', 'Apathetic', 'Communist', 'Conservative', 'Liberal', 'Libertarian', 'Moderate', 'Socialist']

class Client(Node):
	_person = Person()
	_adresss = Address()
	_numbers = Numeric()

	def __init__(self):
		self.__type = 'Client'
		self.id = uuid4()
		self.first_name = self._person.name()
		self.last_name = self._person.surname()
		self.age = self._numbers.integer_number(16, 66)
		self.email = self._person.email()
		self.occupation = self._person.occupation()
		self.political_views = choice(POLITICAL_VIEWS)
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
