from mimesis import Datetime, Numbers, Text, Business
from random import random
from numpy import random as npr
from math import ceil
from uuid import uuid4
from .Node import Node

class Transaction(Node):
	_datetime = Datetime()
	_numbers = Numbers()
	_text = Text()
	_business = Business()

	def __init__(self, sourceId, targetId):
		self.__type = 'Transaction'
		self.id = uuid4()
		self.source = sourceId
		self.target = targetId
		self.date = self._datetime.date(start=2015, end=2019)
		self.time = self._datetime.time()

		if random() < 0.05:
			self.amount = self._numbers.between(100000, 1000000)
		self.amount = npr.exponential(10)

		if random() < 0.15:
			self.currency = self._business.currency_iso_code()
		else:
			self.currency = None
